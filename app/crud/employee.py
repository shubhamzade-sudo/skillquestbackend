from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.employee import Employee

def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
    return db.query(Employee).offset(skip).limit(limit).all()

def get_by_id(db: Session, workday_id: int) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.Workday_ID == workday_id).first()
