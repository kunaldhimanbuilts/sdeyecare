from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# =========================
# LOGIN
# =========================

class LoginRequest(BaseModel):
    email: str | None = None
    phone: str | None = None
    password: str

