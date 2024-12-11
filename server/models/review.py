# server/models/review.py

# SQLAlchemy classes for defining columns, constraints, and relationships
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
# For defining relationships between models
from sqlalchemy.orm import relationship

from models.base import Base  # Base class for all database models
from models.place import Place  # Place model to link reviews to places
from models.user import User  # User model to link reviews to users


class Review(Base):
    """
    SQLAlchemy model representing a review.

    This table stores reviews submitted by users for specific places, including the rating,
    comment, and the user who submitted the review. Reviews are linked to the `User` and
    `Place` tables through foreign key relationships.

    Attributes:
        id (int): Primary key for the review.
        user_id (int): Foreign key linking the review to a specific user.
        place_id (int): Foreign key linking the review to a specific place.
        rating (int): Rating given in the review (required, range 1–5).
        comment (str): Optional textual comment provided by the user.
    """
    __tablename__ = "reviews"  # Name of the table in the database

    # Primary key for the reviews table
    # Unique identifier for each review
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key linking to the 'users' table
    user_id = Column(
        # Deletes reviews when a user is deleted
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Foreign key linking to the 'places' table
    place_id = Column(
        # Deletes reviews when a place is deleted
        Integer, ForeignKey("places.id", ondelete="CASCADE"), nullable=False
    )

    # Integer field for ratings with a constraint to allow only valid ranges (1–5)
    rating = Column(
        Integer, nullable=False  # Required field
    )

    # String field for optional textual comments
    comment = Column(String, nullable=True)  # Optional field for user comments

    # Relationships with User and Place models
    user = relationship(
        "User",  # Target model for the relationship
        back_populates="reviews"  # Corresponding relationship in the User model
    )
    place = relationship(
        "Place",  # Target model for the relationship
        back_populates="reviews"  # Corresponding relationship in the Place model
    )

    # Table constraints
    __table_args__ = (
        CheckConstraint(
            "rating >= 1 AND rating <= 5",  # Ensure rating is between 1 and 5
            name="check_rating_range"  # Name of the constraint
        ),
    )
