# app/schemas/jd_master.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

# Optional: re-declare enums if you used them previously
class Status(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    DRAFT = "DRAFT"

class ModelStatus(str, Enum):
    DONE = "DONE"
    IN_PROGRESS = "IN-Progress"
    FAILED = "Failed"

class JDMasterBase(BaseModel):
    jd_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    required_skills: Optional[str] = None
    preferred_skills: Optional[str] = None
    experience_min: Optional[Decimal] = None
    experience_max: Optional[Decimal] = None
    location: Optional[str] = None
    status: Optional[Status] = None
    model_status: Optional[ModelStatus] = None

class JDMasterUpdate(BaseModel):
    # All fields optional for partial updates
    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[str] = None
    preferred_skills: Optional[str] = None
    experience_min: Optional[Decimal] = None
    experience_max: Optional[Decimal] = None
    location: Optional[str] = None
    status: Optional[Status] = None
    model_status: Optional[ModelStatus] = None

class JDMasterRead(JDMasterBase):
    jd_id: int
    created_date: Optional[datetime] = None

    class Config:
        orm_mode = True
