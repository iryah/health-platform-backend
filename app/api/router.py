from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from ..database import get_db
from .. import models

router = APIRouter()

# ... (diğer model tanımlamaları aynı kalacak)

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

@router.post("/patients/{tc_no}/blood-tests/", response_model=BloodTest)
async def create_blood_test(tc_no: str, blood_test: BloodTestCreate, db: Session = Depends(get_db)):
    # Önce hastayı bul
    patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    
    # Analiz notlarını oluştur
    analysis_notes = []
    is_critical = False
    
    # Hemoglobin kontrolü
    if blood_test.hemoglobin < 12:
        is_critical = True
        analysis_notes.append("Düşük hemoglobin - Anemi riski")
    elif blood_test.hemoglobin > 16:
        is_critical = True
        analysis_notes.append("Yüksek hemoglobin")
    
    # WBC kontrolü
    if blood_test.wbc < 4.5:
        is_critical = True
        analysis_notes.append("Düşük WBC - Enfeksiyon riski")
    elif blood_test.wbc > 11:
        is_critical = True
        analysis_notes.append("Yüksek WBC - Enfeksiyon belirtisi")
    
    # Glucose kontrolü
    if blood_test.glucose < 70:
        is_critical = True
        analysis_notes.append("Düşük kan şekeri - Hipoglisemi")
    elif blood_test.glucose > 100:
        is_critical = True
        analysis_notes.append("Yüksek kan şekeri - Diyabet riski")

    # ALT kontrolü
    if blood_test.alt > 40:
        is_critical = True
        analysis_notes.append("Yüksek ALT - Karaciğer fonksiyon bozukluğu olabilir")

    # AST kontrolü
    if blood_test.ast > 40:
        is_critical = True
        analysis_notes.append("Yüksek AST - Karaciğer fonksiyon bozukluğu olabilir")
    
    # Kan tahlili kaydını oluştur
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
        analysis_notes=", ".join(analysis_notes) if analysis_notes else "Normal değerler",
        is_critical=is_critical
    )
    
    try:
        db.add(db_blood_test)
        db.commit()
        db.refresh(db_blood_test)
        return db_blood_test
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
