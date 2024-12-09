# server/models/place.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from models.base import Base


class Place(Base):
    """
    SQLAlchemy model representing a place.

    Attributes:
        id (int): Primary key for the place.
        name (str): Name of the place.
        description (str): Optional description of the place.
        latitude (float): Geographical latitude of the place.
        longitude (float): Geographical longitude of the place.
        address (str): Physical address of the place.
        types (str): Comma-separated string of place categories/types.
    """
    __tablename__ = "places"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Place information
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=False)
    types = Column(String, nullable=True)

    # Relationships
    reviews = relationship(
        "Review", back_populates="place", cascade="all, delete-orphan"
    )
