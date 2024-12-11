# server/models/user.py

# SQLAlchemy classes for defining columns and constraints
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from models.base import Base  # Base class for all database models


class User(Base):
    """
    SQLAlchemy model representing a user.

    This table stores user information, including their username, hashed password,
    date of birth, and country. The `username` field is unique, ensuring that no
    two users can have the same username.

    Attributes:
        id (int): Primary key for the user.
        username (str): Unique username for the user (required).
        password (str): Hashed password for the user (required).
        dob (datetime): Optional date of birth for the user.
        country (str): Optional country of residence for the user.
    """
    __tablename__ = "users"  # Name of the table in the database

    # Primary key for the users table
    # Unique identifier for each user
    id = Column(Integer, primary_key=True, index=True)

    # Username field with unique constraint and indexing
    username = Column(
        String,  # Column type
        unique=True,  # Ensures usernames are unique across the table
        nullable=False,  # Field is required
        index=True  # Improves lookup performance
    )

    # Password field for storing hashed passwords
    password = Column(
        String,  # Column type
        nullable=False  # Field is required
    )

    # Date of birth field
    dob = Column(
        DateTime,  # Column type for storing dates and times
        nullable=True  # Field is optional
    )

    # Country field
    country = Column(
        String,  # Column type
        nullable=True  # Field is optional
    )

    # Unique constraint for additional validation
    __table_args__ = (
        UniqueConstraint(
            "username",  # Field to enforce uniqueness on
            name="unique_username_constraint"  # Name of the constraint
        ),
    )
