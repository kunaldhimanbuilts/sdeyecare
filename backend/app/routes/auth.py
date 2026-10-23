from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import LoginRequest
from app.utils.hash import verify_password
from app.utils.jwt import create_token

router = APIRouter()



@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    
    user = None

    if data.email:
        user = db.query(User).filter(User.email == data.email).first()
    elif data.phone:
        user = db.query(User).filter(User.phone == data.phone).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # if not verify_password(data.password, user.password):
    #     raise HTTPException(status_code=401, detail="Invalid password")

    # token = create_token({
    #     "user_id": user.id,
    #     "role": user.role
    # })

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid password",
        )

    # Prevent inactive accounts from logging in.
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Your account is deactivated. Contact an administrator.",
        )

    token = create_token({
        "user_id": user.id,
        "role": user.role,
    })

    return {
        "access_token": token,
        "role": user.role,
        "user": {
        "id": user.id,
        "name": user.name
        }
    }