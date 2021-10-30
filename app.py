from flask import Flask, request
from flask_restx import Resource, Api, apidoc
from routes.policy_route import policy_api
from routes.customer_route import customer_api
import os

app = Flask(os.environ.get("APP_NAME"))
api = Api(app, title="bcg app server", doc="/swag")
api.add_namespace(policy_api, path="/api/v1/policy")
api.add_namespace(customer_api, path="/api/v1/customer")

api.init_app(app, add_specs=False)

# @apidoc.apidoc.add_app_template_global
# def swagger_static(filename):
#     return ""

@api.route('/server')
class Status(Resource):
    def get(self):
        return "server is up"

if __name__ == '__main__':
    app.run(debug=True)
