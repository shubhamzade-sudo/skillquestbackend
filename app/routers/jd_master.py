# app/routers/jd_master.py
from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.schemas.jd_master import JDMasterRead, JDMasterBase, JDMasterUpdate
from app.crud import jd_master as crud
from app.db.session import SessionLocal

router = APIRouter(prefix="/jobs", tags=["jobs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[JDMasterRead])
def list_jobs(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=1000), db: Session = Depends(get_db)):
    return crud.get_all_jobs(db, skip=skip, limit=limit)

@router.get("/{jd_id}", response_model=JDMasterRead)
def get_job(jd_id: int, db: Session = Depends(get_db)):
    job = crud.get_job_by_id(db, jd_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/", response_model=JDMasterRead, status_code=201)
def create_job(job_in: JDMasterBase, db: Session = Depends(get_db)):
    job_data = job_in.dict()
    new_job = crud.create_job(db, job_data)
    return new_job

# --------------------
# Update (PUT) - full replace semantics
# --------------------
@router.put("/{jd_id}", response_model=JDMasterRead)
def update_job(jd_id: int, job_in: JDMasterBase, db: Session = Depends(get_db)):
    # For PUT we expect a full representation; convert to dict and pass to update
    updates = job_in.dict()
    updated = crud.update_job(db, jd_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Job not found")
    return updated

# --------------------
# Patch (PATCH) - partial update
# --------------------
@router.patch("/{jd_id}", response_model=JDMasterRead)
def patch_job(jd_id: int, job_in: JDMasterUpdate, db: Session = Depends(get_db)):
    updates = job_in.dict(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    updated = crud.update_job(db, jd_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Job not found")
    return updated

# --------------------
# Delete
# --------------------
@router.delete("/{jd_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(jd_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_job(db, jd_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Job not found")
    # returns 204 No Content on success
    return
