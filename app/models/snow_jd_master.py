from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, func
from app.db.snowflakedb import Base

class JDMaster(Base):
    __tablename__ = "jd_master"
    __table_args__ = {"schema": "PUBLIC"}

    jd_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    required_skills = Column(Text)
    preferred_skills = Column(Text)
    experience_min = Column(Numeric)
    experience_max = Column(Numeric)
    location = Column(String(255))
    created_date = Column(DateTime, server_default=func.now())
    status = Column(String(20))
    model_status = Column(String(20))
