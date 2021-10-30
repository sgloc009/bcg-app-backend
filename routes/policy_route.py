from flask import request
from flask_restx import Resource, Namespace, Model, fields
from sqlalchemy.sql.sqltypes import Boolean

policy_api = Namespace(name="policy_app", version="1.0", description="Handling CRUD based operation for policy related queries")

policy_model = policy_api.model("PolicyModel",{
    "id": fields.Integer,
    "dop": fields.Date,
    "premium": fields.Boolean,
    "bil": fields.Boolean,
    "pip": fields.Boolean,
    "pdl": fields.Boolean,
    "collision": fields.Boolean,
    "comprehensive": fields.Boolean,
})

@policy_api.route("/")
class Policy(Resource):
    @policy_api.marshal_with(policy_model, envelope="resource")
    def get(self):
        return {"id": 12}
    @policy_api.marshal_with(policy_model, envelope="resource")
    def post(self):
        print(request.get_json())
        return "done"
    def delete(self):
        return "done"
