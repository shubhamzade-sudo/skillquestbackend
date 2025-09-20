from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.topevaluation import Topevaluation
from app.models.jd_master import JDMaster
from app.schemas.topevaluation import TopevaluationCreate

def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Topevaluation]:
    return db.query(Topevaluation).offset(skip).limit(limit).all()

def get_by_id(db: Session, jd_id: int) -> List[Topevaluation]:
    return db.query(Topevaluation).filter(Topevaluation.jd_id == jd_id).all()

def create_topevaluation(db: Session, obj_in: TopevaluationCreate) -> Topevaluation:
    # validate foreign key jd_id exists (if provided)
    if obj_in.jd_id is not None:
        found = db.query(JDMaster).filter(JDMaster.jd_id == obj_in.jd_id).first()
        if not found:
            # raise a ValueError so router returns 400 with clear message
            raise ValueError(f"jd_id {obj_in.jd_id} does not exist in jd_master")

    db_obj = Topevaluation(
        workday_id=obj_in.workday_id,
        weighted_score=obj_in.weighted_score,
        recommendation=obj_in.recommendation,
        skills_gaps=obj_in.skills_gaps,
        recommended_training=obj_in.recommended_training,
        jd_id=obj_in.jd_id,
    )
    db.add(db_obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # re-raise for router to inspect and return helpful error
        raise
    db.refresh(db_obj)
    return db_obj
