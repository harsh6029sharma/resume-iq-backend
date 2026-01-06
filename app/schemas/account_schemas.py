from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --- User Schemas ---

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    # Note: is_admin yahan nahi hona chahiye security ke liye

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    is_admin: bool=False
    created_at: datetime

    class Config:
        from_attributes = True

# --- Password & Auth Schemas ---

class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

# --- Analysis & Jobs (Optional but Helpful) ---

class JobBase(BaseModel):
    job_title: str
    description: str

class AnalysisOut(BaseModel):
    id: int
    score: float
    full_feedback: dict
    created_at: datetime

    class Config:
        from_attributes = True