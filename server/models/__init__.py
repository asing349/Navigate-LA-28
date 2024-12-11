# server/models/__init__.py

# Import necessary modules and base class for defining SQLAlchemy models
# For defining relationships between models
from sqlalchemy.orm import relationship

# Import all model definitions
from models.base import Base  # Base model class to define the database schema
from models.user import User  # User model representing application users
# Model for tracking customer usage data
from models.customer_usage import CustomerUsage
from models.review import Review  # Model for storing user reviews
# Model for logging bus route usage
from models.bus_route_usage import BusRouteUsage
from models.bus_stops import BusStop  # Model for representing bus stops
from models.place import Place  # Model for geographic places or locations

# Function to initialize relationships between models


def init_models():
    """
    Initialize relationships between models.

    This function defines relationships and back-populates fields for models after
    all models are imported. This ensures that all dependencies are resolved before
    relationships are initialized.

    Relationships:
        - User to CustomerUsage: A user can have multiple usage records.
        - User to Review: A user can write multiple reviews.
        - User to BusRouteUsage: A user can log multiple bus route usage entries.
    """
    # Define relationship between User and CustomerUsage
    User.usages = relationship(
        "CustomerUsage",  # Target model
        back_populates="user",  # Corresponding field in CustomerUsage
        cascade="all, delete-orphan",  # Automatically handle deletions
        lazy="dynamic",  # Load data lazily when accessed

    )

    # Define relationship between User and Review
    User.reviews = relationship(
        "Review",  # Target model
        back_populates="user",  # Corresponding field in Review
        cascade="all, delete-orphan",  # Automatically handle deletions
        lazy="dynamic",  # Load data lazily when accessed

    )

    # Define relationship between User and BusRouteUsage
    User.bus_route_usages = relationship(
        "BusRouteUsage",  # Target model
        back_populates="user",  # Corresponding field in BusRouteUsage
        cascade="all, delete-orphan",  # Automatically handle deletions
        lazy="dynamic",  # Load data lazily when accessed

    )


# Call init_models to initialize relationships after all model imports
init_models()

# Exported symbols for easier imports
# Allows models to be imported directly from the `models` package
__all__ = [
    "Base",  # Base class for defining all models
    "User",  # User model
    "CustomerUsage",  # CustomerUsage model
    "Review",  # Review model
    "BusRouteUsage",  # BusRouteUsage model
    "BusStop",  # BusStop model
    "Place",  # Place model
]
