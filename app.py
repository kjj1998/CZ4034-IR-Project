from flask import Flask, flash, redirect, request, render_template, make_response
from flask_restx import Resource, Api, fields, reqparse
import os

from sentence_transformers import SentenceTransformer
from PIL import Image
from werkzeug.utils import secure_filename

from clients.solr_client import SolrClient
from configs.solr_configs import SOLR_CORE_NAME
from configs.app_configs import UPLOAD_FOLDER
from configs.app_configs import IMAGE_CONTENT_LENGTH

from utils import allowed_file

# UPLOAD_FOLDER = "./images"

app = Flask(__name__)
app.secret_key = "secretKey"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = IMAGE_CONTENT_LENGTH

# ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


# def allowed_file(filename):
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_image():
    for f in os.listdir("images/"):
        os.remove(os.path.join("images/", f))
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        # print('upload_image filename: ' + filename)
        flash("Image successfully uploaded")
        return render_template("index.html", filename=filename)
    else:
        flash("Allowed image types are - png, jpg, jpeg, gif")
        return redirect(request.url)


api = Api(app, doc="/docs/")


@api.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


search_result_model = api.model(
    "Search Result Model",
    {
        "id": fields.String,
        "name": fields.String,
        "price": fields.Float,
        "information": fields.String,
        "rating": fields.Float,
        "review": fields.String,
    },
)

parser = reqparse.RequestParser()
parser.add_argument("query", type=str, help="term to query for in Solr")


@api.route("/search")
class SearchSolr(Resource):
    # @api.marshal_list_with(search_result_model, envelope='resource')
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        solr = SolrClient(core_name=SOLR_CORE_NAME)

        # print("hello")
        # print(args) # print out arguments from frontend for debugging
        # print("hello")

        # query = "*:*" if args['query'] == None else args['query']

        query_parameters = form_query_parameters(args["query"], retrieve_image())

        # query_parameters = {
        #     "q": query,
        #     "fl": "id,name,price,information,rating,review,score,amazon_image_url",
        #     "q.op": "AND",
        #     "rows": 20,
        #     "indent": "on",
        # }

        res = solr.search_query(query_parameters)
        res_json = res.json()
        query_data = res_json["response"]
        docs_data = query_data["docs"]
        headers = {"Content-Type": "text/html"}

        remove_all_images_currently_stored()

        return make_response(
            render_template("search.html", results=docs_data), 200, headers
        )


def convert_image_to_vectors(opened_image):
    img_model = SentenceTransformer("clip-ViT-B-32")
    images = [opened_image]

    vectors = img_model.encode(images, convert_to_numpy=True, show_progress_bar=True)
    vectors = [list(vector) for vector in list(vectors)]

    return vectors[0]


def remove_all_images_currently_stored():
    for f in os.listdir("images/"):
        os.remove(os.path.join("images/", f))


def retrieve_image():
    folder_path = "./images"

    if not os.listdir(folder_path):
        return None

    for file_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, file_name)
        image = Image.open(image_path)
        return image


def form_query_parameters(text, image):
    query_parameters = {
        "fl": "id,name,price,information,rating,review,score,amazon_image_url",
        "q.op": "AND",
        "rows": 20,
    }

    query = ""
    if text == "" and image == None:
        query = "*:*"
    elif text == "" and image != None:
        image = retrieve_image()
        vectors = convert_image_to_vectors(image)
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
        vectors = convert_image_to_vectors(image)
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


if __name__ == "__main__":
    app.run(debug=True)
