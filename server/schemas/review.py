# server/schemas/review.py

# BaseModel and Field for defining Pydantic schemas
from pydantic import BaseModel, Field
from typing import Optional  # For optional fields

# Base schema with shared configuration for Pydantic models
from schemas.base import BaseSchema


class ReviewBase(BaseSchema):
    """
    Shared fields between Review schemas.

    Attributes:
        rating (int): Rating for the review, constrained between 1 and 5.
        comment (str, optional): Optional textual comment about the place.
    """
    rating: int = Field(
        ...,  # Field is required
        ge=1,  # Minimum value for rating
        le=5,  # Maximum value for rating
        description="Rating between 1 and 5"  # Description for API documentation
    )
    comment: Optional[str] = Field(
        None,  # Field is optional, defaults to None
        # Description for API documentation
        description="Optional comment about the place"
    )


class ReviewCreate(ReviewBase):
    """
    Fields required for creating a new review.

    Attributes:
        place_id (int): ID of the place being reviewed.
        user_id (int): ID of the user submitting the review.
    """
    place_id: int = Field(
        ...,  # Field is required
        description="ID of the place being reviewed"  # Description for API documentation
    )
    user_id: int = Field(
        ...,  # Field is required
        # Description for API documentation
        description="ID of the user submitting the review"
    )


class ReviewUpdate(BaseModel):
    """
    Fields allowed for updating an existing review.

    Attributes:
        rating (int, optional): Updated rating for the review, constrained between 1 and 5.
        comment (str, optional): Updated textual comment about the place.
    """
    rating: Optional[int] = Field(
        None,  # Field is optional, defaults to None
        ge=1,  # Minimum value for rating
        le=5,  # Maximum value for rating
        description="Updated rating between 1 and 5"  # Description for API documentation
    )
    comment: Optional[str] = Field(
        None,  # Field is optional, defaults to None
        # Description for API documentation
        description="Updated comment about the place"
    )


class Review(ReviewBase):
    """
    Response schema for Review, includes all database-specific fields.

    Attributes:
        id (int): Unique identifier for the review.
        user_id (int): ID of the user who submitted the review.
        place_id (int): ID of the place being reviewed.
    """
    id: int = Field(
        ...,  # Field is required
        # Description for API documentation
        description="Unique identifier for the review"
    )
    user_id: int = Field(
        ...,  # Field is required
        # Description for API documentation
        description="ID of the user who submitted the review"
    )
    place_id: int = Field(
        ...,  # Field is required
        description="ID of the place being reviewed"  # Description for API documentation
    )

    class Config:
        """
        Pydantic configuration class.

        Attributes:
            orm_mode (bool): Enables Pydantic models to interact seamlessly with SQLAlchemy ORM objects.
        """
        orm_mode = True  # Enable compatibility with SQLAlchemy models
