import os
from configs.app_configs import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from PIL import Image


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_image_to_vectors(opened_image, img_model):
    images = [opened_image]

    vectors = img_model.encode(images, convert_to_numpy=True, show_progress_bar=True)
    vectors = [list(vector) for vector in list(vectors)]

    return vectors[0]


def retrieve_image():
    folder_path = UPLOAD_FOLDER

    if not os.listdir(folder_path):
        return None

    for file_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, file_name)
        image = Image.open(image_path)
        return image


def form_query_parameters(text, image, img_model):
    query_parameters = {
        "fl": "id,name,price,information,rating,review,score,amazon_image_url,subjectivity,prediction",
        "q.op": "AND",
        "rows": 20,
    }

    query = ""
    if text == "" and image == None:
        query = "*:*"
    elif text == "" and image != None:
        image = retrieve_image()
        vectors = convert_image_to_vectors(image, img_model)
        query = (
            "{!knn f=vector topK=20}"
            + "["
            + ", ".join(str(float_value) for float_value in vectors)
            + "]"
        )
    elif text != "" and image == None:
        query = text
    elif text != "" and image != None:
        image = retrieve_image()
        vectors = convert_image_to_vectors(image,img_model)
        query = (
            "{!knn f=vector topK=20}"
            + "["
            + ", ".join(str(float_value) for float_value in vectors)
            + "]"
        )
        filter = "name:(" + text + ")"
        query_parameters["fq"] = filter

    query_parameters["q"] = query

    # print(query_parameters)

    return query_parameters


def remove_all_images_currently_stored():
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER + "/", f))
