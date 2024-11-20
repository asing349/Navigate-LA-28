# server/schemas/review.py
from pydantic import BaseModel, Field
from typing import Optional

from schemas.base import BaseSchema

class ReviewBase(BaseSchema):
    """
    Shared fields between Review schemas.
    """
    rating: int = Field(..., ge=1, le=5, description="Rating between 1 and 5")
    comment: Optional[str] = Field(None, description="Optional comment about the place")

class ReviewCreate(ReviewBase):
    """
    Fields required for creating a new review.
    """
    place_id: int = Field(..., description="ID of the place being reviewed")
    user_id: int = Field(..., description="ID of the user submitting the review")

class ReviewUpdate(BaseModel):
    """
    Fields allowed for updating an existing review.
    """
    rating: Optional[int] = Field(None, ge=1, le=5, description="Updated rating between 1 and 5")
    comment: Optional[str] = Field(None, description="Updated comment about the place")

class Review(ReviewBase):
    """
    Response schema for Review, includes all database-specific fields.
    """
    id: int = Field(..., description="Unique identifier for the review")
    user_id: int = Field(..., description="ID of the user who submitted the review")
    place_id: int = Field(..., description="ID of the place being reviewed")

    class Config:
        orm_mode = True
