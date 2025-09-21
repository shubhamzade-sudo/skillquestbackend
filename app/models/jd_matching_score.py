# app/models/jd_matching_score.py
from sqlalchemy import Column, Integer, Text, TIMESTAMP, Float, String
from app.db.base import Base

class JDMatchingScore(Base):
    __tablename__ = "jd_matching_score"
    __table_args__ = {"schema": "public"}

    workday_id = Column("Workday_ID", Integer, primary_key=True, index=True)
    weighted_score = Column("weighted_score", Integer, nullable=True)
    recommendation = Column("Recommendation", Text, nullable=True)
    skills_gaps = Column("Skills_Gaps", Text, nullable=True)
    recommended_training = Column("Recommended_Training", Text, nullable=True)
    jd_id = Column("jd_id", Integer, nullable=True, index=True)

    strengths = Column("strengths", Text, nullable=True)
    weaknesses = Column("weaknesses", Text, nullable=True)
    suggestions = Column("suggestions", Text, nullable=True)
    created_date = Column("created_date", TIMESTAMP, nullable=True)
    updated_date = Column("updated_date", TIMESTAMP, nullable=True)
    model_version = Column("model_version", String, nullable=True)
    match_score = Column("match_score", Float, nullable=True)
