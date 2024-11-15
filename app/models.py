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
    
    # İlişkiler
    blood_tests = relationship("BloodTest", back_populates="patient")
    complaints = relationship("Complaint", back_populates="patient")
    lab_reports = relationship("LabReport", back_populates="patient")
    ai_consultations = relationship("AIDoctorConsultation", back_populates="patient")

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

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String)  # Şikayet açıklaması
    symptoms = Column(String)     # Belirtiler
    duration = Column(String)     # Şikayet süresi
    severity = Column(Integer)    # Şiddet seviyesi (1-10 arası)
    ai_analysis = Column(String, nullable=True)  # AI analiz sonucu
    doctor_notes = Column(String, nullable=True) # Doktor notları
    status = Column(String, default="pending")   # pending, analyzed, referred
    
    # İlişkiler
    patient = relationship("Patient", back_populates="complaints")
    ai_consultations = relationship("AIDoctorConsultation", back_populates="complaint")

class LabReport(Base):
    __tablename__ = "lab_reports"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    upload_date = Column(DateTime, default=datetime.utcnow)
    report_date = Column(DateTime)
    file_path = Column(String)    # PDF dosyasının yolu
    report_type = Column(String)  # blood, urine, imaging vb.
    analysis_result = Column(String, nullable=True)  # OCR ve analiz sonucu
    ai_analysis = Column(String, nullable=True)      # AI yorumu
    status = Column(String, default="pending")       # pending, analyzed, reviewed
    
    # İlişkiler
    patient = relationship("Patient", back_populates="lab_reports")
    ai_consultations = relationship("AIDoctorConsultation", back_populates="lab_report")

class AIDoctorConsultation(Base):
    __tablename__ = "ai_consultations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=True)
    lab_report_id = Column(Integer, ForeignKey("lab_reports.id"), nullable=True)
    consultation_date = Column(DateTime, default=datetime.utcnow)
    patient_input = Column(String)       # Hastanın soruları/endişeleri
    ai_response = Column(String)         # AI'ın yanıtı
    recommendation = Column(String)      # Öneriler
    severity_level = Column(String)      # low, medium, high
    followup_needed = Column(Boolean, default=False)
    
    # İlişkiler
    patient = relationship("Patient", back_populates="ai_consultations")
    complaint = relationship("Complaint", back_populates="ai_consultations")
    lab_report = relationship("LabReport", back_populates="ai_consultations")
