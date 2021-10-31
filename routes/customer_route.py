from flask import json, request
from flask.wrappers import Response
from flask_restx import Namespace, Resource, marshal
from sqlalchemy import func
from sqlalchemy.sql.expression import or_, select
from sqlalchemy.orm import Session
from models.models import Customer as Customer_Model,\
     Vehicle as Vehicle_Model,\
          Insurance as Insurance_Model, engine
from routes.marshal_models import vehicle_model
from datetime import datetime

customer_api = Namespace("customer_route",description="Route to handle CRUD operations for Customers")
policy_api = Namespace(name="policy_app", version="1.0", description="Handling CRUD based operation for policy related queries")
policy_model = policy_api.model("PolicyModel", vehicle_model)

@customer_api.route("/stats")
class CustomerStats(Resource):
    def get(self):
        chart_type = request.args.get("type")
        result = []
        response = Response(status=200, headers={"Content-Type": "application/json"})
        if(chart_type=="date"):
            with Session(engine) as s:
                try:
                    for row in s.query(func.count(Insurance_Model.id), Insurance_Model.dop).group_by(Insurance_Model.dop):
                        date_row = dict()
                        date_row["name"] = row["dop"]
                        date_row["value"] = row[0]
                        result.append(date_row)
                    response.response = json.dumps(result)
                except Exception as e:
                    print(e)
                    response.status = 500
                    response.response = "Error"
                finally:
                    s.close()
                    return response
        else:
            with Session(engine) as s:
                try:
                    for row in s.query(func.count(Insurance_Model.id).label("count"), func.strftime('%Y-%m',Insurance_Model.dop).label("dop")).group_by(func.strftime('%Y-%m', Insurance_Model.dop)):
                        date_row = dict()
                        date_row["name"] = datetime.strptime(row["dop"], '%Y-%m')
                        date_row["value"] = row["count"]
                        result.append(date_row)
                    response.response = json.dumps(result)
                except Exception as e:
                    response.status = 500
                    response.headers = {"Content-type": "plain/text"}
                    response.data = "Error"
                finally:
                    s.close()
                    return response
            



@customer_api.route("/")
class Customer(Resource):
    def get(self):
        customer_id = request.args.get("customer_id")
        insurance_id = request.args.get("insurance_id")
        print(customer_id, insurance_id)
        res = []
        response = Response(json.dumps({"items": res}), status=200,headers={"Content-Type": "application/json"})
        with Session(engine) as s:
            try:
                for i in s.query(Customer_Model).join(Customer_Model.vehicle).join(Vehicle_Model.insurance).filter(or_(Customer_Model.id == customer_id , Insurance_Model.id == insurance_id)):
                    res.append(i.to_dict())
                response.data = json.dumps({"items": res})
                return response
            except Exception:
                response.data = "error"
                response.headers = {"Content-Type": "plain/text"}
            finally:
                return response

    def post(self):
        data = request.get_json()
        data = marshal(data, vehicle_model)
        data["insurance"]["dop"] = datetime.strptime(data["insurance"]["dop"], '%Y-%m-%d')
        response = Response("Updated Successfully", status=200)
        with Session(engine) as s:
            try:
                insurance = s.query(Insurance_Model).filter(Insurance_Model.id==data["insurance"]["id"]).update(data["insurance"])
                data["insurance"] = insurance
                s.query(Vehicle_Model).filter(Vehicle_Model.id==data["id"]).update(data)
                s.commit()
            except Exception as e:
                print(e)
                s.rollback()
                response = Response("Error", 500)
            finally:
                s.close()
                return response