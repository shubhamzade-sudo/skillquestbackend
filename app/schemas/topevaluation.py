from pydantic import BaseModel
from typing import Optional

class TopevaluationCreate(BaseModel):
    workday_id: int
    weighted_score: Optional[int] = None
    recommendation: Optional[str] = None
    skills_gaps: Optional[str] = None
    recommended_training: Optional[str] = None
    jd_id: Optional[int] = None

class TopevaluationRead(BaseModel):
    workday_id: int
    weighted_score: Optional[int]
    recommendation: Optional[str]
    skills_gaps: Optional[str]
    recommended_training: Optional[str]
    jd_id: Optional[int]

    class Config:
        orm_mode = True
