# server/schemas/review.py
from .base import BaseSchema
from typing import Optional

class ReviewBase(BaseSchema):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    place_id: int

class Review(ReviewBase):
    id: int
    user_id: int
    place_id: int
