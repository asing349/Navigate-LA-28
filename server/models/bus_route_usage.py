# server/models/bus_route_usage.py

# SQLAlchemy classes for defining columns and foreign keys
from sqlalchemy import Column, Integer, String, ForeignKey
# SQLAlchemy function for defining relationships between tables
from sqlalchemy.orm import relationship
from models.base import Base  # Base class for all database models


class BusRouteUsage(Base):
    """
    Model representing a bus route usage record.

    This table tracks information about a user's bus route usage, including the user who used the route,
    the origin bus stop, and the destination bus stop.
    """
    __tablename__ = "bus_route_usage"  # Name of the table in the database

    # Primary key for the bus_route_usage table
    # Unique identifier for each record
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key linking to the 'users' table
    # ID of the user who used the bus route
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Foreign key linking to the origin bus stop in the 'bus_stops' table
    origin_stop_id = Column(Integer, ForeignKey(
        "bus_stops.id"), nullable=False)  # ID of the origin bus stop

    # Foreign key linking to the destination bus stop in the 'bus_stops' table
    destination_stop_id = Column(Integer, ForeignKey(
        "bus_stops.id"), nullable=False)  # ID of the destination bus stop

    # Relationships
    user = relationship(
        "User",  # Target model
        back_populates="bus_route_usages"  # Corresponding relationship in the User model
    )
    origin_stop = relationship(
        "BusStop",  # Target model
        # Specify the foreign key for the origin bus stop
        foreign_keys=[origin_stop_id]
    )
    destination_stop = relationship(
        "BusStop",  # Target model
        # Specify the foreign key for the destination bus stop
        foreign_keys=[destination_stop_id]
    )
