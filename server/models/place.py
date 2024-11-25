from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from models.base import Base


class Place(Base):
    __tablename__ = "places"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    reviews = relationship(
        "Review", back_populates="place", cascade="all, delete-orphan"
    )
