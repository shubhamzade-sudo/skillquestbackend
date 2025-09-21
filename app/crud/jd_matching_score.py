from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.jd_matching_score import JDMatchingScore
from app.models.jd_master import JDMaster
from app.schemas.jd_matching_score import JDMatchingScoreCreate

def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[JDMatchingScore]:
    return db.query(JDMatchingScore).offset(skip).limit(limit).all()

def get_by_id(db: Session, jd_id: int) -> List[JDMatchingScore]:
    return db.query(JDMatchingScore).filter(JDMatchingScore.jd_id == jd_id).all()

def create_jd_matching_score(db: Session, obj_in: JDMatchingScoreCreate) -> JDMatchingScore:
    if obj_in.jd_id is not None:
        found = db.query(JDMaster).filter(JDMaster.jd_id == obj_in.jd_id).first()
        if not found:
            raise ValueError(f"jd_id {obj_in.jd_id} does not exist in jd_master")

    db_obj = JDMatchingScore(
        workday_id=obj_in.workday_id,
        weighted_score=obj_in.weighted_score,
        recommendation=obj_in.recommendation,
        skills_gaps=obj_in.skills_gaps,
        recommended_training=obj_in.recommended_training,
        jd_id=obj_in.jd_id,
        strengths=obj_in.strengths,
        weaknesses=obj_in.weaknesses,
        suggestions=obj_in.suggestions,
        created_date=obj_in.created_date,
        updated_date=obj_in.updated_date,
        model_version=obj_in.model_version,
        match_score=obj_in.match_score,
    )
    db.add(db_obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(db_obj)
    return db_obj
