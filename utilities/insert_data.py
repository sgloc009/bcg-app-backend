from models.models import Customer, Insurance, Vehicle, engine
from sqlalchemy.orm import Session
from datetime import datetime
import pandas as pd

def insert_data():
    data = pd.read_csv("data/Data Set - Insurance Client.csv")
    print(data.columns)
    insurance_columns = ["Policy_id", "Date of Purchase", "Premium", "bodily injury liability", " personal injury protection", " property damage liability", " collision", " comprehensive"]
    customer_columns = ["Customer_id", "Customer_Gender", "Customer_Income group", "Customer_Region", "Customer_Marital_status"]
    vehicle_columns = ["Fuel", "VEHICLE_SEGMENT"]

    insurance_columns_map = {
        "id": "Policy_id",
        "dop": "Date of Purchase",
        "premium": "Premium",
        "bil": "bodily injury liability",
        "pip": " personal injury protection",
        "pdl": " property damage liability",
        "collision": " collision",
        "comprehensive": " comprehensive"
    }

    customer_columns_map = {
        "id": "Customer_id",
        "gender": "Customer_Gender",
        "income_group": "Customer_Income group",
        "region": "Customer_Region",
        "marital_status": "Customer_Marital_status"
    }

    vehicle_columns_map = {
        "fuel": "Fuel",
        "segment": "VEHICLE_SEGMENT"
    }

    """ Remove customer inconsistencies
        (420, 'Male', '$25-$70K', 'North', 0),
        (420, 'Male', '$25-$70K', 'North', 1),
        (840, 'Male', '$25-$70K', 'South', 0),
        (840, 'Male', '$25-$70K', 'South', 1),
        (840, 'Male',    '>$70K', 'South', 0),
        (840, 'Male',    '>$70K', 'South', 1),
    """
    customer_objects = []
    customer_data_grouped = data.groupby([*customer_columns])
    count_series =  customer_data_grouped.size()
    print(count_series[count_series>1].index)
    data[["Customer_Marital_status","Customer_Income group"]] = data.groupby("Customer_id")[["Customer_Marital_status","Customer_Income group"]].transform("last")

    """
    Restructure data
    """
    data = data.set_index([*customer_columns])
    count_series =  customer_data_grouped.size()
    print(count_series[count_series>1].index)
    customer_data_grouped = data.groupby([*customer_columns])
    # print(customer_data_grouped.groups)
    all_vehicles = []
    for group in customer_data_grouped.groups:
        vehicle = []
        for idx, row in data.loc[group][[*vehicle_columns, *insurance_columns]].iterrows():
            vehicle.append(Vehicle(row[vehicle_columns_map["fuel"]],row[vehicle_columns_map["segment"]],
                insurance=Insurance(row[insurance_columns_map["premium"]], datetime.strptime(row[insurance_columns_map["dop"]], '%m/%d/%Y'), row[insurance_columns_map["bil"]],\
                    row[insurance_columns_map["pip"]], row[insurance_columns_map["pdl"]], row[insurance_columns_map["collision"]], row[insurance_columns_map["comprehensive"]], row[insurance_columns_map["id"]])))
        all_vehicles.extend(vehicle)
        customer_objects.append(Customer(group[1], group[2], vehicle, group[3], group[4], group[0]))
        

    with Session(engine) as s:
        try:
            s.add_all(customer_objects)
            s.commit()
        except Exception as e:
            s.rollback()