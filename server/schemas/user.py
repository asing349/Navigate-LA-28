# server/schemas/user.py
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from schemas.base import BaseSchema


class UserBase(BaseSchema):
    username: str = Field(..., description="Unique username of the user")
    dob: Optional[datetime] = Field(
        None, description="Date of birth of the user")
    country: Optional[str] = Field(None, description="Country of residence")


class UserCreate(UserBase):
    password: str = Field(..., description="Password for the user account")


class User(UserBase):
    id: int = Field(..., description="Unique identifier for the user")
    reviews: List[dict] = Field(
        default_factory=list, description="List of reviews")
    usages: List[dict] = Field(
        default_factory=list, description="List of customer usage records")

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    username: str = Field(..., description="Username for authentication")
    password: str = Field(..., description="Password for authentication")
