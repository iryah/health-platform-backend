from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    tc_no = Column(String, unique=True, index=True)
    name = Column(String)
    surname = Column(String)
    birth_date = Column(DateTime)
    gender = Column(String)
    phone = Column(String)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    blood_type = Column(String, nullable=True)
