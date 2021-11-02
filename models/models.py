from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, VARCHAR, MetaData, create_engine
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os
from sqlalchemy.sql.schema import CheckConstraint

load_dotenv()
engine = create_engine(os.environ.get("DB_STRING"), echo=True)
Base = declarative_base()
meta = MetaData(engine)

class Insurance(Base):
    __tablename__ = "insurance"
    id = Column(Integer, primary_key=True)
    dop = Column(Date, default=func.now())
    premium = Column(Integer)
    bil = Column(Boolean, default=False)
    pip = Column(Boolean, default=False)
    pdl = Column(Boolean, default=False)
    collision = Column(Boolean, default=False)
    comprehensive = Column(Boolean, default=False)
    vehicle = relationship("Vehicle", back_populates="insurance")

    def __init__(self, premium, dop=None, bil=False, pip=False, pdl=False, collision=False, comprehensive=False, id=None):
        self.premium = premium
        self.id = id
        self.dop = dop
        self.bil = bil
        self.pip = pip
        self.pdl = pdl
        self.collision = collision
        self.comprehensive = comprehensive
    
    def to_dict(self):
        return {
            "id" : self.id,
            "premium": self.premium,
            "dop": self.dop,
            "bil": self.bil,
            "pip": self.pip,
            "pdl": self.pdl,
            "collision": self.collision,
            "comprehensive": self.comprehensive
        }
    
    def __repr__(self):
        return '<Insurance %r %r %r %r %r %r %r>' % (self.premium, self.dop, self.bil, self.pip, self.pdl, self.collision, self.comprehensive)

class Vehicle(Base):
    __tablename__ = "vehicle"
    __table_args__ = (CheckConstraint('fuel IN ("CNG","Petrol","Diesel")'),)
    id = Column(Integer, primary_key=True)
    insurance_id = Column(Integer, ForeignKey("insurance.id"))
    fuel = Column(VARCHAR(10))
    customer_id = Column(Integer, ForeignKey("customer.id"))
    segment = Column(String(1))
    insurance = relationship("Insurance", back_populates="vehicle", uselist=False )

    def __init__(self, fuel, segment, insurance):
        self.fuel = fuel
        self.segment = segment
        self.insurance = insurance
    
    def to_dict(self):
        return {
            "id": self.id,
            "fuel": self.fuel,
            "segment": self.segment,
            "insurance": self.insurance.to_dict()
        }

    def __repr__(self):
        return '<Vehicle %r %r %r>' % (self.fuel, self.segment, self.insurance)


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    gender = Column(VARCHAR(10))
    income_group = Column(VARCHAR(50))
    vehicle = relationship("Vehicle")
    region = Column(VARCHAR(100))
    marital_status = Column(Boolean, default=False)

    def __init__(self, gender, income_group, vehicle, region, marital_status, id=None):
        self.id = id
        self.gender = gender
        self.income_group = income_group
        self. vehicle = vehicle
        self.region = region
        self.marital_status = marital_status
    
    def to_dict(self):
        self.vehicle
        return {
            "id": self.id,
            "gender": self.gender,
            "income_group": self.income_group,
            "vehicle": list(map(lambda x: x.to_dict(), self.vehicle)),
            "region": self.region,
            "marital_status": self.marital_status
        }
    
    def __repr__(self):
        return '<Customer %r %r %r %r %r %r>' %(self.id, self.gender, self.income_group, self.region, self.marital_status, self.vehicle)

Base.metadata.create_all(engine)
