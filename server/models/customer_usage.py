# server/models/customer_usage.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from models.base import Base


class CustomerUsage(Base):
    __tablename__ = "customer_usage"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key linking to the users table
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # String field to store requests made
    request_made = Column(String, nullable=False)

    # Timestamp with a default value of the current UTC time
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship with the User model
    user = relationship("User", back_populates="usages")
