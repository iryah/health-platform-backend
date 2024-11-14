from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
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
    
    # Hasta ile kan tahlilleri arasında ilişki
    blood_tests = relationship("BloodTest", back_populates="patient")

class BloodTest(Base):
    __tablename__ = "blood_tests"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    test_date = Column(DateTime, default=datetime.utcnow)
    
    # Hemogram değerleri
    hemoglobin = Column(Float)  # g/dL
    hematocrit = Column(Float)  # %
    wbc = Column(Float)        # 10^3/µL (Beyaz kan hücresi)
    rbc = Column(Float)        # 10^6/µL (Kırmızı kan hücresi)
    platelets = Column(Float)  # 10^3/µL (Trombosit)
    
    # Biyokimya değerleri
    glucose = Column(Float)    # mg/dL (Kan şekeri)
    urea = Column(Float)       # mg/dL (Üre)
    creatinine = Column(Float) # mg/dL (Kreatinin)
    alt = Column(Float)        # U/L (Alanin aminotransferaz)
    ast = Column(Float)        # U/L (Aspartat aminotransferaz)
    
    # Analiz sonucu ve yorumlar
    analysis_notes = Column(String, nullable=True)
    is_critical = Column(Boolean, default=False)
    
    # İlişki
    patient = relationship("Patient", back_populates="blood_tests")
