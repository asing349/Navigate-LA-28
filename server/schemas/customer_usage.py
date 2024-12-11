# server/schemas/customer_usage.py

from datetime import datetime  # For managing timestamp fields
# Base class and field customization for Pydantic schemas
from pydantic import BaseModel, Field

# Base schema with shared configuration for Pydantic models
from schemas.base import BaseSchema


class CustomerUsageBase(BaseSchema):
    """
    Shared fields between CustomerUsage schemas.

    Attributes:
        request_made (str): Details of the request made by the user.
        timestamp (datetime): Timestamp indicating when the request was made. Defaults to the current UTC time.
    """
    request_made: str = Field(
        ...,  # Field is required
        description="Details of the request made"  # Description for API documentation
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,  # Automatically set to the current UTC time
        description="Timestamp of the request"  # Description for API documentation
    )


class CustomerUsageCreate(CustomerUsageBase):
    """
    Fields required for creating a new CustomerUsage record.

    Inherits all shared fields from CustomerUsageBase.
    """
    pass  # No additional fields are required for creation


class CustomerUsage(CustomerUsageBase):
    """
    Response schema for CustomerUsage, including database-specific fields.

    Attributes:
        id (int): Unique identifier for the customer usage record.
        user_id (int): ID of the user associated with this usage record.
    """
    id: int = Field(
        ...,  # Field is required
        # Description for API documentation
        description="Unique identifier for the customer usage record"
    )
    user_id: int = Field(
        ...,  # Field is required
        # Description for API documentation
        description="ID of the user associated with this usage record"
    )

    class Config:
        """
        Pydantic configuration class.

        Attributes:
            orm_mode (bool): Enables Pydantic models to interact seamlessly with SQLAlchemy ORM objects.
        """
        orm_mode = True  # Enable compatibility with SQLAlchemy models
