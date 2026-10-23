from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientCreate
from app.utils.patient_code import generate_patient_code
from app.utils.deps import require_role
from app.utils.deps import require_roles
from sqlalchemy import or_
router = APIRouter()



# ✅ Create Patient
@router.post("/")
def create_patient(data: PatientCreate, db: Session = Depends(get_db), user=Depends(require_role("compounder"))):

    last_patient = db.query(Patient).order_by(Patient.id.desc()).first()
    next_id = 1 if not last_patient else last_patient.id + 1

    patient_code = generate_patient_code(next_id)

    new_patient = Patient(
        patient_code=patient_code,
        **data.dict()
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@router.get("/search-list/{query}")
def search_patient_list(
    query: str,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["doctor", "compounder", "admin"]))
):

    patients = db.query(Patient).filter(
        or_(
            Patient.patient_code.ilike(f"%{query}%"),
            Patient.name.ilike(f"%{query}%"),
            Patient.phone.ilike(f"%{query}%"),
            Patient.address.ilike(f"%{query}%")
        )
    ).order_by(Patient.name).limit(20).all()

    return patients
