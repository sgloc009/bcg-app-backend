from flask import json, request
from flask_restx import Namespace, Resource, fields
from routes.policy_route import policy_model

customer_api = Namespace("customer_route",description="Route to handle CRUD operations for Customers")

vehicle_model = customer_api.model("VehicleModel",{
    "id": fields.Integer,
    "fuel": fields.String,
    "segment": fields.String
}) 

customer_model = customer_api.model("CustomerModel",{
    "id": fields.Integer,
    "gender": fields.String,
    "income_group": fields.String,
    "vehicle": fields.List(fields.Nested(vehicle_model)),
    "insurance": fields.List(fields.Nested(policy_model)),
    "region": fields.String,
    "marital_status": fields.Boolean,
})

@customer_api.route("/")
class Customer(Resource):
    @customer_api.marshal_with(customer_model)
    def get(self):
        return "done"
    def post(self):
        return "done"
    def delete(self):
        return "done"