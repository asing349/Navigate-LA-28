# server/schemas/place.py

from typing import Optional  # For optional fields
# BaseModel and Field for Pydantic schemas
from pydantic import BaseModel, Field


class PlaceBase(BaseModel):
    """
    Base schema for Place with shared fields.

    Attributes:
        name (str): The name of the place.
        description (str, optional): An optional description providing details about the place.
        latitude (float): The geographical latitude of the place.
        longitude (float): The geographical longitude of the place.
        address (str): The physical address of the place.
        types (str, optional): A comma-separated string of categories or types associated with the place.
    """
    name: str = Field(
        ...,  # Field is required
        description="Name of the place."  # Description for API documentation
    )
    description: Optional[str] = Field(
        None,  # Field is optional, defaults to None
        # Description for API documentation
        description="Optional description of the place."
    )
    latitude: float = Field(
        ...,  # Field is required
        description="Latitude of the place."  # Description for API documentation
    )
    longitude: float = Field(
        ...,  # Field is required
        description="Longitude of the place."  # Description for API documentation
    )
    address: str = Field(
        ...,  # Field is required
        description="Address of the place."  # Description for API documentation
    )
    types: Optional[str] = Field(
        None,  # Field is optional, defaults to None
        # Description for API documentation
        description="Comma-separated string of place categories/types."
    )


class PlaceCreate(PlaceBase):
    """
    Schema for creating a new place.

    Inherits all fields from PlaceBase.
    """
    pass  # No additional fields are required for creation


class Place(PlaceBase):
    """
    Schema for returning Place details.

    Attributes:
        id (int): Unique identifier for the place.
        distance (float, optional): Distance to the place in meters (optional field).
    """
    id: int = Field(
        ...,  # Field is required
        # Description for API documentation
        description="Unique identifier for the place."
    )
    distance: float | None = Field(
        None,  # Field is optional, defaults to None
        # Description for API documentation
        description="Distance to the place in meters."
    )

    class Config:
        """
        Pydantic configuration class.

        Attributes:
            orm_mode (bool): Enables Pydantic models to interact seamlessly with SQLAlchemy ORM objects.
        """
        orm_mode = True  # Enable compatibility with SQLAlchemy models
