# server/schemas/customer_usage.py
from datetime import datetime

from schemas.base import BaseSchema

class CustomerUsageBase(BaseSchema):
    request_made: str
    timestamp: datetime

class CustomerUsageCreate(CustomerUsageBase):
    pass

class CustomerUsage(CustomerUsageBase):
    id: int
    user_id: int
