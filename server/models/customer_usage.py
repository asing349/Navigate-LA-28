# server/models/customer_usage.py

# SQLAlchemy classes for defining columns and relationships
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# For defining relationships between models
from sqlalchemy.orm import relationship
from datetime import datetime  # For working with date and time
from models.base import Base  # Base class for all database models


class CustomerUsage(Base):
    """
    Model representing customer usage logs.

    This table tracks the interactions made by users in the application, including
    the specific requests made and the timestamps of those requests.
    """
    __tablename__ = "customer_usage"  # Name of the table in the database

    # Primary key for the customer_usage table
    # Unique identifier for each record
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key linking to the 'users' table
    # ID of the user who made the request
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Field to store the request details
    # Description of the request made by the user
    request_made = Column(String, nullable=False)

    # Timestamp for when the request was made
    timestamp = Column(
        DateTime,  # Column type for storing date and time
        default=datetime.utcnow,  # Default value is the current UTC time
        nullable=False  # This field is required
    )

    # Relationship with the User model
    user = relationship(
        "User",  # Target model
        back_populates="usages"  # Corresponding relationship in the User model
    )
