from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

# Hasta veri modeli
class Patient(BaseModel):
    id: Optional[int] = None
    tc_no: str
    name: str
    surname: str
    birth_date: datetime
    gender: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    blood_type: Optional[str] = None

# Geçici veri depolama (daha sonra veritabanına geçeceğiz)
patients_db = []

# Hasta ekleme
@router.post("/patients/")
async def create_patient(patient: Patient):
    patient.id = len(patients_db) + 1
    patients_db.append(patient)
    return {"status": "success", "message": f"{patient.name} {patient.surname} başarıyla kaydedildi"}

# Tüm hastaları listeleme
@router.get("/patients/")
async def list_patients():
    return {"patients": patients_db}

# TC no ile hasta arama
@router.get("/patients/{tc_no}")
async def get_patient(tc_no: str):
    patient = next((p for p in patients_db if p.tc_no == tc_no), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    return patient

# Hasta bilgilerini güncelleme
@router.put("/patients/{tc_no}")
async def update_patient(tc_no: str, updated_patient: Patient):
    for i, patient in enumerate(patients_db):
        if patient.tc_no == tc_no:
            updated_patient.id = patient.id
            patients_db[i] = updated_patient
            return {"status": "success", "message": "Hasta bilgileri güncellendi"}
    raise HTTPException(status_code=404, detail="Hasta bulunamadı")

# Hasta silme
@router.delete("/patients/{tc_no}")
async def delete_patient(tc_no: str):
    for i, patient in enumerate(patients_db):
        if patient.tc_no == tc_no:
            patients_db.pop(i)
            return {"status": "success", "message": "Hasta kaydı silindi"}
    raise HTTPException(status_code=404, detail="Hasta bulunamadı")
