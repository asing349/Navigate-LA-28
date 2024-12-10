# server/schemas/place.py
from typing import Optional
from pydantic import BaseModel, Field


class PlaceBase(BaseModel):
    """
    Base schema for Place with shared fields.
    """

    name: str = Field(..., description="Name of the place.")
    description: Optional[str] = Field(
        None, description="Optional description of the place."
    )
    latitude: float = Field(..., description="Latitude of the place.")
    longitude: float = Field(..., description="Longitude of the place.")
    address: str = Field(..., description="Address of the place.")
    types: Optional[str] = Field(
        None, description="Comma-separated string of place categories/types."
    )


class PlaceCreate(PlaceBase):
    """
    Schema for creating a new place.
    """

    pass


class Place(PlaceBase):
    """
    Schema for returning Place details.
    """

    id: int = Field(..., description="Unique identifier for the place.")
    distance: float | None = Field(None, description="Distance to the place in meters.")

    class Config:
        orm_mode = True
