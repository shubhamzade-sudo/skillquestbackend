from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.db.snowflakedb import get_db
from app.models.snow_jd_master import JDMaster   # ✅ FIXED

router = APIRouter(
    prefix="/jd_master",
    tags=["jd_master"]
)

class JDIn(BaseModel):
    title: str
    description: Optional[str] = None
    required_skills: Optional[str] = None
    preferred_skills: Optional[str] = None
    experience_min: Optional[float] = None
    experience_max: Optional[float] = None
    location: Optional[str] = None
    status: Optional[str] = None
    model_status: Optional[str] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_jd(jd: JDIn, db: Session = Depends(get_db)):
    try:
        obj = JDMaster(**jd.dict())   # ✅
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return {"status": "ok", "jd_id": obj.jd_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk", status_code=status.HTTP_201_CREATED)
def bulk_insert(jds: List[JDIn], db: Session = Depends(get_db)):
    if not jds:
        raise HTTPException(status_code=400, detail="Empty list")
    try:
        objs = [JDMaster(**jd.dict()) for jd in jds]   # ✅
        db.bulk_save_objects(objs)
        db.commit()
        return {"status": "ok", "inserted": len(objs)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", name="List JDs")
def list_jds(
    limit: int = Query(50, ge=1, le=1000),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    try:
        items = (
            db.query(JDMaster)   # ✅
            .order_by(JDMaster.jd_id.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        result = []
        for i in items:
            result.append({
                "jd_id": i.jd_id,
                "title": i.title,
                "description": i.description,
                "required_skills": i.required_skills,
                "preferred_skills": i.preferred_skills,
                "experience_min": float(i.experience_min) if i.experience_min is not None else None,
                "experience_max": float(i.experience_max) if i.experience_max is not None else None,
                "location": i.location,
                "created_date": i.created_date.isoformat() if i.created_date else None,
                "status": i.status,
                "model_status": i.model_status
            })

        return {"count": len(result), "items": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
