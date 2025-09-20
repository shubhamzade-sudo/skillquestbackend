# app/crud/jd_master.py
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.jd_master import JDMaster

def get_all_jobs(db: Session, skip: int = 0, limit: int = 100) -> List[JDMaster]:
    return db.query(JDMaster).offset(skip).limit(limit).all()

def get_job_by_id(db: Session, jd_id: int) -> Optional[JDMaster]:
    return db.query(JDMaster).filter(JDMaster.jd_id == jd_id).first()

def create_job(db: Session, job_data: dict) -> JDMaster:
    job = JDMaster(**job_data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def update_job(db: Session, jd_id: int, updates: Dict[str, Any]) -> Optional[JDMaster]:
    """
    updates: dict of column_name -> new value (use model attribute names, e.g. 'title', 'status')
    Returns updated object or None if not found.
    """
    job = get_job_by_id(db, jd_id)
    if not job:
        return None
    # apply updates only for existing attributes
    for key, value in updates.items():
        if hasattr(job, key) and value is not None:
            setattr(job, key, value)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def delete_job(db: Session, jd_id: int) -> bool:
    job = get_job_by_id(db, jd_id)
    if not job:
        return False
    db.delete(job)
    db.commit()
    return True
