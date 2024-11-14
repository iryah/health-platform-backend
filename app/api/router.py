from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from ..database import get_db
from .. import models

router = APIRouter()

# Hasta veri modeli (Pydantic)
class PatientBase(BaseModel):
    tc_no: str
    name: str
    surname: str
    birth_date: datetime
    gender: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    blood_type: Optional[str] = None

    class Config:
        from_attributes = True

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True

# Kan tahlili veri modeli
class BloodTestBase(BaseModel):
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
    analysis_notes: Optional[str] = None

    class Config:
        from_attributes = True

class BloodTestCreate(BloodTestBase):
    pass

class BloodTest(BloodTestBase):
    id: int
    patient_id: int
    test_date: datetime
    is_critical: bool

    class Config:
        from_attributes = True

# Hasta işlemleri
@router.post("/patients/", response_model=Patient)
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.tc_no == patient.tc_no).first()
    if db_patient:
        raise HTTPException(status_code=400, detail="Bu TC kimlik numarası zaten kayıtlı")
    
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/patients/", response_model=List[Patient])
async def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients

@router.get("/patients/{tc_no}", response_model=Patient)
async def get_patient(tc_no: str, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    return patient

@router.put("/patients/{tc_no}", response_model=Patient)
async def update_patient(tc_no: str, patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    
    for var, value in vars(patient).items():
        setattr(db_patient, var, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.delete("/patients/{tc_no}")
async def delete_patient(tc_no: str, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    
    db.delete(patient)
    db.commit()
    return {"status": "success", "message": "Hasta kaydı silindi"}

# Kan tahlili işlemleri
@router.post("/patients/{tc_no}/blood-tests/", response_model=BloodTest)
async def create_blood_test(tc_no: str, blood_test: BloodTestCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    
    is_critical = False
    analysis_notes = []
    
    if blood_test.hemoglobin < 12:
        is_critical = True
        analysis_notes.append("Düşük hemoglobin - Anemi olabilir")
    elif blood_test.hemoglobin > 16:
        is_critical = True
        analysis_notes.append("Yüksek hemoglobin")
    
    if blood_test.wbc < 4.5:
        is_critical = True
        analysis_notes.append("Düşük WBC - Enfeksiyon riski")
    elif blood_test.wbc > 11:
        is_critical = True
        analysis_notes.append("Yüksek WBC - Enfeksiyon göstergesi")
    
    if blood_test.glucose < 70:
        is_critical = True
        analysis_notes.append("Düşük kan şekeri - Hipoglisemi")
    elif blood_test.glucose > 100:
        is_critical = True
        analysis_notes.append("Yüksek kan şekeri - Diyabet riski")
    
    db_blood_test = models.BloodTest(
        **blood_test.dict(),
        patient_id=patient.id,
        is_critical=is_critical,
        analysis_notes=", ".join(analysis_notes) if analysis_notes else "Normal değerler"
    )
    
    db.add(db_blood_test)
    db.commit()
    db.refresh(db_blood_test)
    return db_blood_test

@router.get("/patients/{tc_no}/blood-tests/", response_model=List[BloodTest])
async def list_blood_tests(tc_no: str, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    return patient.blood_tests

@router.get("/patients/{tc_no}/blood-tests/{test_id}", response_model=BloodTest)
async def get_blood_test(tc_no: str, test_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    
    blood_test = db.query(models.BloodTest).filter(
        models.BloodTest.id == test_id,
        models.BloodTest.patient_id == patient.id
    ).first()
    
    if not blood_test:
        raise HTTPException(status_code=404, detail="Kan tahlili bulunamadı")
    
    return blood_test
