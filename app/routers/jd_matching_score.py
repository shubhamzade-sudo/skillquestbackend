from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.jd_matching_score import JDMatchingScoreRead, JDMatchingScoreCreate
from app.crud import jd_matching_score as crud
from app.db.session import SessionLocal

router = APIRouter(prefix="/jd_matching_score", tags=["jd_matching_score"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[JDMatchingScoreRead])
def list_jd_matching_score(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return crud.get_all(db, skip=skip, limit=limit)

@router.get("/{jd_id}", response_model=List[JDMatchingScoreRead])
def read_jd_matching_score(jd_id: int, db: Session = Depends(get_db)):
    row = crud.get_by_id(db, jd_id)
    if not row:
        raise HTTPException(status_code=404, detail="Row not found")
    return row

@router.post("/", response_model=JDMatchingScoreRead, status_code=status.HTTP_201_CREATED)
def create_jd_matching_score(payload: JDMatchingScoreCreate, db: Session = Depends(get_db)):
    try:
        created = crud.create_jd_matching_score(db, payload)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except IntegrityError as ie:
        raise HTTPException(status_code=400, detail=f"Integrity error while inserting row: {ie}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))

    return created
