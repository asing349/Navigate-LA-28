# server/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from models.base import Base

class User(Base):
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Username field with a unique constraint and indexing
    username = Column(String, unique=True, nullable=False, index=True)

    # Password field (hashed)
    password = Column(String, nullable=False)

    # Date of birth
    dob = Column(DateTime, nullable=True)

    # Country field
    country = Column(String, nullable=True)

    # Relationships
    usages = relationship("CustomerUsage", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

    # Unique constraint for additional validation
    __table_args__ = (
        UniqueConstraint("username", name="unique_username_constraint"),
    )

