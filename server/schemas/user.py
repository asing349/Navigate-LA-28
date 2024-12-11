# server/schemas/user.py

from typing import List, Optional  # For optional fields and list type annotations
from datetime import datetime  # For date and time fields
# BaseModel and Field for defining Pydantic schemas
from pydantic import BaseModel, Field

# Base schema with shared configuration for Pydantic models
from schemas.base import BaseSchema


class UserBase(BaseSchema):
    """
    Base schema for User with shared fields.

    Attributes:
        username (str): Unique username of the user.
        dob (datetime, optional): Date of birth of the user.
        country (str, optional): Country of residence for the user.
    """
    username: str = Field(
        ...,  # Field is required
        description="Unique username of the user"  # Description for API documentation
    )
    dob: Optional[datetime] = Field(
        None,  # Field is optional, defaults to None
        description="Date of birth of the user"  # Description for API documentation
    )
    country: Optional[str] = Field(
        None,  # Field is optional, defaults to None
        description="Country of residence"  # Description for API documentation
    )


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Attributes:
        password (str): Password for the user account.
    """
    password: str = Field(
        ...,  # Field is required
        description="Password for the user account"  # Description for API documentation
    )


class User(UserBase):
    """
    Schema for returning User details, including related data.

    Attributes:
        id (int): Unique identifier for the user.
        reviews (List[dict]): List of reviews created by the user.
        usages (List[dict]): List of customer usage records associated with the user.
    """
    id: int = Field(
        ...,  # Field is required
        description="Unique identifier for the user"  # Description for API documentation
    )
    reviews: List[dict] = Field(
        default_factory=list,  # Default to an empty list
        description="List of reviews"  # Description for API documentation
    )
    usages: List[dict] = Field(
        default_factory=list,  # Default to an empty list
        description="List of customer usage records"  # Description for API documentation
    )

    class Config:
        """
        Pydantic configuration class.

        Attributes:
            orm_mode (bool): Enables Pydantic models to interact seamlessly with SQLAlchemy ORM objects.
        """
        orm_mode = True  # Enable compatibility with SQLAlchemy models


class UserAuth(BaseModel):
    """
    Schema for user authentication.

    Attributes:
        username (str): Username for authentication.
        password (str): Password for authentication.
    """
    username: str = Field(
        ...,  # Field is required
        description="Username for authentication"  # Description for API documentation
    )
    password: str = Field(
        ...,  # Field is required
        description="Password for authentication"  # Description for API documentation
    )
