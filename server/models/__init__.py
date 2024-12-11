# server/models/__init__.py
from sqlalchemy.orm import relationship

from models.base import Base
from models.user import User
from models.customer_usage import CustomerUsage
from models.review import Review
from models.bus_route_usage import BusRouteUsage
from models.bus_stops import BusStop
from models.place import Place


# Initialize relationships after all models are defined
def init_models():
    User.usages = relationship(
        "CustomerUsage",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
    User.reviews = relationship(
        "Review", back_populates="user", cascade="all, delete-orphan", lazy="dynamic"
    )
    User.bus_route_usages = relationship(
        "BusRouteUsage",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )


# Call init_models after all models are imported
init_models()

__all__ = [
    "Base",
    "User",
    "CustomerUsage",
    "Review",
    "BusRouteUsage",
    "BusStop",
    "Place",
]
