# server/routes/review_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.review import ReviewCreate, Review, ReviewUpdate
from services.review_service import create_review, get_review, update_review, delete_review
from config.database import get_db

router = APIRouter()

@router.post("/reviews/", response_model=Review, status_code=201)
def create_review_route(review: ReviewCreate, db: Session = Depends(get_db)):
    return create_review(db, review)

@router.get("/reviews/{review_id}", response_model=Review)
def read_review_route(review_id: int, db: Session = Depends(get_db)):
    review = get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/reviews/{review_id}", response_model=Review)
def update_review_route(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)):
    updated_review = update_review(db, review_id, review)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review

@router.delete("/reviews/{review_id}", status_code=204)
def delete_review_route(review_id: int, db: Session = Depends(get_db)):
    if not delete_review(db, review_id):
        raise HTTPException(status_code=404, detail="Review not found")
