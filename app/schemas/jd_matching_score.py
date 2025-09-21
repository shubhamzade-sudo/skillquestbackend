from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JDMatchingScoreCreate(BaseModel):
    workday_id: int
    weighted_score: Optional[int] = None
    recommendation: Optional[str] = None
    skills_gaps: Optional[str] = None
    recommended_training: Optional[str] = None
    jd_id: Optional[int] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    suggestions: Optional[str] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    model_version: Optional[str] = None
    match_score: Optional[float] = None


class JDMatchingScoreRead(BaseModel):
    workday_id: int
    weighted_score: Optional[int]
    recommendation: Optional[str]
    skills_gaps: Optional[str]
    recommended_training: Optional[str]
    jd_id: Optional[int]
    strengths: Optional[str]
    weaknesses: Optional[str]
    suggestions: Optional[str]
    created_date: Optional[datetime]
    updated_date: Optional[datetime]
    model_version: Optional[str]
    match_score: Optional[float]

    model_config = {"from_attributes": True}  # ✅ replaces orm_mode
