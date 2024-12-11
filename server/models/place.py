# server/models/place.py

# SQLAlchemy classes for defining columns and their types
from sqlalchemy import Column, Integer, String, Float
# For defining relationships between models
from sqlalchemy.orm import relationship
from models.base import Base  # Base class for all database models


class Place(Base):
    """
    SQLAlchemy model representing a place.

    This table stores information about various places, including their geographic
    coordinates, address, and categories. Each place can be associated with multiple
    reviews, defined through a relationship with the Review model.

    Attributes:
        id (int): Primary key for the place.
        name (str): Name of the place (required).
        description (str): Optional description providing details about the place.
        latitude (float): Geographical latitude of the place (required).
        longitude (float): Geographical longitude of the place (required).
        address (str): Physical address of the place (required).
        types (str): Comma-separated string of categories/types the place belongs to (optional).
    """
    __tablename__ = "places"  # Name of the table in the database

    # Primary key for the places table
    # Unique identifier for each place
    id = Column(Integer, primary_key=True, index=True)

    # Place details
    # Name of the place (e.g., "City Park")
    name = Column(String, nullable=False)
    # Optional description of the place
    description = Column(String, nullable=True)
    # Latitude coordinate of the place
    latitude = Column(Float, nullable=False)
    # Longitude coordinate of the place
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=False)  # Physical address of the place
    # Categories/types of the place (e.g., "Park, Outdoor")
    types = Column(String, nullable=True)

    # Relationships
    reviews = relationship(
        "Review",  # Target model for the relationship
        back_populates="place",  # Corresponding relationship in the Review model
        cascade="all, delete-orphan"  # Automatically handle related Review deletions
    )
