# server/schemas/user.py
from .base import BaseSchema
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

# Forward declarations for Review and CustomerUsage to be used in type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .review import Review
    from .customer_usage import CustomerUsage

class UserBase(BaseSchema):
    username: str
    dob: Optional[datetime] = None
    country: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    reviews: List['Review'] = []  # Use 'Review' as a string to denote forward reference
    usages: List['CustomerUsage'] = []  # Use 'CustomerUsage' as a string to denote forward reference

class UserAuth(BaseModel):
    username: str
    password: str
