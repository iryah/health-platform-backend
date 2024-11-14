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

# Kan tahlili ekleme
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

# Hastanın tüm kan tahlillerini listeleme
@router.get("/patients/{tc_no}/blood-tests/", response_model=List[BloodTest])
async def list_blood_tests(tc_no: str, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.tc_no == tc_no).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    return patient.blood_tests

# Belirli bir kan tahlilini görüntüleme
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
