from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.user import User
from app.utils.deps import require_roles

router = APIRouter()


@router.get("/doctors")
def get_doctors(
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin", "compounder"])),
):
    doctors = (
        db.query(User)
        .filter(
            User.role == "doctor",
            User.is_active.is_(True),
        )
        .order_by(User.name.asc())
        .all()
    )

    return [
        {
            "id": doctor.id,
            "name": doctor.name,
        }
        for doctor in doctors
    ]

