from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from .database import get_db
from . import models

router = APIRouter()

# Temel kan tahlili modeli
class BloodTestCreate(BaseModel):
    hemoglobin: float
    hematocrit: float
    wbc: float
    rbc: float
    platelets: float
    glucose: float
    urea: float
    creatinine: float
    alt: float
    ast: float

    class Config:
        from_attributes = True

# Kan tahlili oluşturma endpoint'i
@router.post("/patients/{tc_no}/blood-tests/")
async def create_blood_test(tc_no: str, blood_test: BloodTestCreate, db: Session = Depends(get_db)):
    # Hastayı bul
    patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    
    # Analiz notları
    analysis_notes = []
    is_critical = False
    
    # Değerleri kontrol et
    if blood_test.hemoglobin < 12:
        is_critical = True
        analysis_notes.append("Düşük hemoglobin - Anemi riski")
    
    if blood_test.wbc > 11:
        is_critical = True
        analysis_notes.append("Yüksek WBC - Enfeksiyon belirtisi")
    
    if blood_test.glucose > 100:
        is_critical = True
        analysis_notes.append("Yüksek kan şekeri - Diyabet riski")
    
    # Yeni kan tahlili kaydı oluştur
    db_blood_test = models.BloodTest(
        patient_id=patient.id,
        hemoglobin=blood_test.hemoglobin,
        hematocrit=blood_test.hematocrit,
        wbc=blood_test.wbc,
        rbc=blood_test.rbc,
        platelets=blood_test.platelets,
        glucose=blood_test.glucose,
        urea=blood_test.urea,
        creatinine=blood_test.creatinine,
        alt=blood_test.alt,
        ast=blood_test.ast,
        is_critical=is_critical,
        analysis_notes=", ".join(analysis_notes) if analysis_notes else "Normal değerler"
    )
    
    db.add(db_blood_test)
    db.commit()
    db.refresh(db_blood_test)
    
    return {
        "message": "Kan tahlili başarıyla kaydedildi",
        "blood_test": db_blood_test,
        "analysis_notes": db_blood_test.analysis_notes,
        "is_critical": db_blood_test.is_critical
    }

# Hasta listeleme endpoint'i
@router.get("/patients/")
async def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients

# Hasta detay endpoint'i
@router.get("/patients/{tc_no}")
async def get_patient(tc_no: str, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    return patient
