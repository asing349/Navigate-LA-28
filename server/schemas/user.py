# server/schemas/user.py
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from schemas.base import BaseSchema
from schemas.review import Review
from schemas.customer_usage import CustomerUsage


class UserBase(BaseSchema):
    """
    Shared fields between User schemas.
    """
    username: str = Field(..., description="Unique username of the user")
    dob: Optional[datetime] = Field(None, description="Date of birth of the user")
    country: Optional[str] = Field(None, description="Country of residence")


class UserCreate(UserBase):
    """
    Schema for creating a new user, includes password.
    """
    password: str = Field(..., description="Password for the user account")


class User(UserBase):
    """
    Response schema for User, includes related reviews and usages.
    """
    id: int = Field(..., description="Unique identifier for the user")
    reviews: List[Review] = Field(default_factory=list, description="List of reviews submitted by the user")
    usages: List[CustomerUsage] = Field(default_factory=list, description="List of customer usage records")

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    """
    Schema for user authentication.
    """
    username: str = Field(..., description="Username for authentication")
    password: str = Field(..., description="Password for authentication")
