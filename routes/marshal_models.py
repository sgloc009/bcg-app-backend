from flask_restx import fields

policy_model = {
    "id": fields.Integer,
    "dop": fields.Date,
    "premium": fields.Integer,
    "bil": fields.Boolean,
    "pip": fields.Boolean,
    "pdl": fields.Boolean,
    "collision": fields.Boolean,
    "comprehensive": fields.Boolean,
}

vehicle_model = {
    "id": fields.Integer,
    "fuel": fields.String,
    "segment": fields.String,
    "insurance": fields.Nested(policy_model),
}

customer_model = {
    "id": fields.Integer,
    "gender": fields.String,
    "income_group": fields.String,
    "vehicle": fields.List(fields.Nested(vehicle_model)),
    "region": fields.String,
    "marital_status": fields.Boolean,
}

customers_model = {
    "items": fields.List(fields.Nested(customer_model))
}