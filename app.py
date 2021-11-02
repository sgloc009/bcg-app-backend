from flask import Flask, request
from flask_restx import Resource, Api, apidoc
from routes.customer_route import customer_api
from utilities import insert_data
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(os.environ.get("APP_NAME"))
insert_data.insert_data()
api = Api(app, title="bcg app server", doc="/swag")
api.add_namespace(customer_api, path="/api/v1/customer")

api.init_app(app, add_specs=False)

@api.route('/server')
class Status(Resource):
    def get(self):
        return "server is up"

if __name__ == '__main__':
    app.run(os.environ.get("HOST"), int(os.environ.get("PORT")),\
         debug=not eval(os.environ["PROD"]))
