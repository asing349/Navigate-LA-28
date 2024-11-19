# server/schemas/customer_usage.py
from .base import BaseSchema
from datetime import datetime

class CustomerUsageBase(BaseSchema):
    request_made: str
    timestamp: datetime

class CustomerUsageCreate(CustomerUsageBase):
    pass

class CustomerUsage(CustomerUsageBase):
    id: int
    user_id: int
