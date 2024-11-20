# server/models/review.py
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from models.base import Base

class Review(Base):
    __tablename__ = "reviews"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys linking to users and places tables
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    place_id = Column(Integer, ForeignKey('places.id', ondelete="CASCADE"), nullable=False)

    # Integer field for ratings with a constraint for valid ranges
    rating = Column(Integer, nullable=False)
    
    # String field for comments
    comment = Column(String, nullable=True)

    # Relationships with User and Place models
    user = relationship("User", back_populates="reviews")
    place = relationship("Place", back_populates="reviews")

    # Add constraints for rating values
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),
    )
