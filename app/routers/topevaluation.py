from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.topevaluation import TopevaluationRead, TopevaluationCreate
from app.crud import topevaluation as crud
from app.db.session import SessionLocal

router = APIRouter(prefix="/topevaluation", tags=["topevaluation"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[TopevaluationRead])
def list_topevaluation(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return crud.get_all(db, skip=skip, limit=limit)

@router.get("/{jd_id}", response_model=List[TopevaluationRead])
def read_topevaluation(jd_id: int, db: Session = Depends(get_db)):
    row = crud.get_by_id(db, jd_id)
    if not row:
        raise HTTPException(status_code=404, detail="Row not found")
    return row

@router.post("/", response_model=TopevaluationRead, status_code=status.HTTP_201_CREATED)
def create_topevaluation(payload: TopevaluationCreate, db: Session = Depends(get_db)):
    # duplicate PK check

    try:
        created = crud.create_topevaluation(db, payload)
    except ValueError as ve:
        # custom validation (fk missing)
        raise HTTPException(status_code=400, detail=str(ve))
    except IntegrityError as ie:
        # return DB error message for debugging (ok for dev)
        try:
            orig = str(ie.orig)
        except Exception:
            orig = str(ie)
        raise HTTPException(status_code=400, detail=f"Integrity error while inserting row: {orig}")
    except Exception as e:
        # fallback
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))

    return created
