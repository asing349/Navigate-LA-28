# server/schemas/customer_usage.py
from datetime import datetime
from pydantic import BaseModel, Field

from schemas.base import BaseSchema


class CustomerUsageBase(BaseSchema):
    """
    Shared fields between CustomerUsage schemas.
    """
    request_made: str = Field(..., description="Details of the request made")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of the request")


class CustomerUsageCreate(CustomerUsageBase):
    """
    Fields required for creating a new CustomerUsage record.
    """
    pass


class CustomerUsage(CustomerUsageBase):
    """
    Response schema for CustomerUsage, including database-specific fields.
    """
    id: int = Field(...,
                    description="Unique identifier for the customer usage record")
    user_id: int = Field(...,
                         description="ID of the user associated with this usage record")

    class Config:
        orm_mode = True
