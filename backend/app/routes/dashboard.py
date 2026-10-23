from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.user import User
router = APIRouter()


# ✅ Dashboard Stats API
@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    total_patients = db.query(Patient).count()

    today_appointments = db.query(Appointment).filter(
        Appointment.date == date.today()
    ).count()

    active_doctors = db.query(User).filter(
        User.role == "doctor",
        User.is_active.is_(True)
    ).count()

    return {
        "total_patients": total_patients,
        "today_appointments": today_appointments,
        "active_doctors": active_doctors
    }
