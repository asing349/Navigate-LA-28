# server/schemas/review.py
from pydantic import BaseModel
from typing import Optional
from .base import BaseSchema

class ReviewBase(BaseSchema):
    rating: int
    comment: Optional[str] = None

# Inherits ReviewBase for creating a new review, requires place_id and user_id
class ReviewCreate(ReviewBase):
    place_id: int
    user_id: int

# Used for updates, allows optional updates to rating and comment
class ReviewUpdate(BaseModel):
    rating: Optional[int]
    comment: Optional[str]

# Full Review schema used for reading data, includes ID, and integrates ORM mode
class Review(ReviewBase):
    id: int
    user_id: int
    place_id: int

    class Config:
        orm_mode = True
