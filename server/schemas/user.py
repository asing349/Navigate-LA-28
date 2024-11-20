# server/schemas/user.py
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from schemas.base import BaseSchema
from schemas.review import Review  # Import the actual Review class
from schemas.customer_usage import (
    CustomerUsage,
)  # Import the actual CustomerUsage class


class UserBase(BaseSchema):
    username: str
    dob: Optional[datetime] = None
    country: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    reviews: List[Review] = []
    usages: List[CustomerUsage] = []


class UserAuth(BaseModel):
    username: str
    password: str
