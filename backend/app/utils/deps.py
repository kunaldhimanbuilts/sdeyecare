import os

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User


security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")


def get_current_user(
    token=Depends(security),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=["HS256"],
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    # Always check the current database record.
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User account not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Your account is deactivated.",
        )

    # Return the current database identity and role.
    return {
        "user_id": user.id,
        "role": user.role,
    }


def require_role(role: str):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] != role:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

        return user

    return role_checker


def require_roles(roles: list):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

        return user

    return role_checker
