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
        orm_mode = True

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

# Hasta ekleme
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

# Tüm hastaları listeleme
@router.get("/patients/", response_model=List[Patient])
async def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients

# TC no ile hasta arama
@router.get("/patients/{tc_no}", response_model=Patient)
async def get_patient(tc_no: str, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    return patient

# Hasta bilgilerini güncelleme
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

# Hasta silme
@router.delete("/patients/{tc_no}")
async def delete_patient(tc_no: str, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    
    db.delete(patient)
    db.commit()
    return {"status": "success", "message": "Hasta kaydı silindi"}
