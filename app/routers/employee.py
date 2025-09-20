from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.schemas.employee import EmployeeRead
from app.crud import employee as crud
from app.db.session import SessionLocal

router = APIRouter(prefix="/employee", tags=["employee"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[EmployeeRead])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return crud.get_all(db, skip=skip, limit=limit)

@router.get("/{workday_id}", response_model=EmployeeRead)
def read_employee(workday_id: int, db: Session = Depends(get_db)):
    row = crud.get_by_id(db, workday_id)
    if not row:
        raise HTTPException(status_code=404, detail="Employee not found")
    return row
