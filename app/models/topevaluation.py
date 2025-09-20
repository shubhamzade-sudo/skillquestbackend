from sqlalchemy import Column, Integer, Text
from app.db.base import Base

class Topevaluation(Base):
    __tablename__ = "topevaluation"
    __table_args__ = {"schema": "public"}

    # Workday_ID is the PK according to your screenshots
    workday_id = Column("Workday_ID", Integer, primary_key=True, index=True)
    weighted_score = Column("weighted_score", Integer, nullable=True)
    recommendation = Column("Recommendation", Text, nullable=True)
    skills_gaps = Column("Skills_Gaps", Text, nullable=True)
    recommended_training = Column("Recommended_Training", Text, nullable=True)
    jd_id = Column("jd_id", Integer, nullable=True, index=True)
