# app/models/jd_master.py
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class JDMaster(Base):
    __tablename__ = "jd_master"          # lowercase table name
    __table_args__ = {"schema": "public"}  # remove if not in public schema

    # column names are lowercase to match your DB
    jd_id = Column("jd_id", Integer, primary_key=True, autoincrement=True, index=True)
    title = Column("title", String(255), nullable=False)
    description = Column("description", Text)
    required_skills = Column("required_skills", Text)
    preferred_skills = Column("preferred_skills", Text)
    experience_min = Column("experience_min", Numeric)
    experience_max = Column("experience_max", Numeric)
    location = Column("location", String(255))
    created_date = Column("created_date", DateTime(timezone=False), server_default=func.now())
    status = Column("status", String(20))
    model_status = Column("model_status", String(20))
