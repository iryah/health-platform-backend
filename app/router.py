from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from .database import get_db
from . import models
import logging

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        # Hastayı bul
        logger.info(f"Hasta aranıyor: {tc_no}")
        patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
        if not patient:
            logger.error(f"Hasta bulunamadı: {tc_no}")
            raise HTTPException(status_code=404, detail="Hasta bulunamadı")
        
        logger.info(f"Hasta bulundu: {patient.id}")
        
        # Analiz notları
        analysis_notes = []
        is_critical = False
        
        # Değerleri kontrol et
        logger.info("Kan değerleri analiz ediliyor...")
        if blood_test.hemoglobin < 12:
            is_critical = True
            analysis_notes.append("Düşük hemoglobin - Anemi riski")
        
        if blood_test.wbc > 11:
            is_critical = True
            analysis_notes.append("Yüksek WBC - Enfeksiyon belirtisi")
        
        if blood_test.glucose > 100:
            is_critical = True
            analysis_notes.append("Yüksek kan şekeri - Diyabet riski")
        
        try:
            # Yeni kan tahlili kaydı oluştur
            logger.info("Kan tahlili kaydı oluşturuluyor...")
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
            
            logger.info("Veritabanına kayıt ekleniyor...")
            db.add(db_blood_test)
            db.commit()
            db.refresh(db_blood_test)
            logger.info("Kan tahlili başarıyla kaydedildi")
            
            return {
                "message": "Kan tahlili başarıyla kaydedildi",
                "blood_test": {
                    "id": db_blood_test.id,
                    "patient_id": db_blood_test.patient_id,
                    "hemoglobin": db_blood_test.hemoglobin,
                    "hematocrit": db_blood_test.hematocrit,
                    "wbc": db_blood_test.wbc,
                    "rbc": db_blood_test.rbc,
                    "platelets": db_blood_test.platelets,
                    "glucose": db_blood_test.glucose,
                    "urea": db_blood_test.urea,
                    "creatinine": db_blood_test.creatinine,
                    "alt": db_blood_test.alt,
                    "ast": db_blood_test.ast,
                },
                "analysis_notes": db_blood_test.analysis_notes,
                "is_critical": db_blood_test.is_critical
            }
            
        except Exception as e:
            logger.error(f"Veritabanı hatası: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Veritabanı hatası: {str(e)}")
            
    except Exception as e:
        logger.error(f"Genel hata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bir hata oluştu: {str(e)}")
