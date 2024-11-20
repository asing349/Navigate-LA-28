# server/services/review_service.py
from sqlalchemy.orm import Session

from models.review import Review as ReviewModel
from schemas.review import ReviewCreate, ReviewUpdate

def create_review(db: Session, review: ReviewCreate) -> ReviewModel:
    db_review = ReviewModel(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: int) -> ReviewModel:
    return db.query(ReviewModel).filter(ReviewModel.id == review_id).first()

def update_review(db: Session, review_id: int, review: ReviewUpdate) -> ReviewModel:
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if db_review:
        update_data = review.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
        return db_review
    return None

def delete_review(db: Session, review_id: int) -> bool:
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
        return True
    return False
