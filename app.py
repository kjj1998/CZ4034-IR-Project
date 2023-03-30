from flask import Flask, flash, redirect, request, render_template, make_response
from flask_restx import Resource, Api, fields, reqparse
import os

from werkzeug.utils import secure_filename

from clients.solr_client import SolrClient
from configs.solr_configs import SOLR_CORE_NAME
from configs.app_configs import UPLOAD_FOLDER
from configs.app_configs import IMAGE_CONTENT_LENGTH

from utils import (
    allowed_file,
    form_query_parameters,
    remove_all_images_currently_stored,
    retrieve_image,
)

app = Flask(__name__)
app.secret_key = "secretKey"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = IMAGE_CONTENT_LENGTH


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

        query_parameters = form_query_parameters(args["query"], retrieve_image())

        res = solr.search_query(query_parameters)
        res_json = res.json()
        query_data = res_json["response"]
        docs_data = query_data["docs"]
        headers = {"Content-Type": "text/html"}

        remove_all_images_currently_stored()

        return make_response(
            render_template("search.html", results=docs_data, query=args["query"]), 200, headers
        )


if __name__ == "__main__":
    app.run(debug=True)
