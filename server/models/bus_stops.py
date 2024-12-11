# server/models/bus_stops.py

# SQLAlchemy classes for defining columns and their types
from sqlalchemy import Column, Integer, String, Float
from models.base import Base  # Base class for all database models


class BusStop(Base):
    """
    Model representing a bus stop.

    This table contains information about individual bus stops, including their location, line, direction,
    and geographic coordinates. Each record uniquely identifies a bus stop in the system.
    """
    __tablename__ = "bus_stops"  # Name of the table in the database

    # Primary key for the bus_stops table
    # Unique identifier for each bus stop
    id = Column(Integer, primary_key=True, index=True)

    # Bus stop details
    # Unique number assigned to the bus stop
    stop_number = Column(Integer, nullable=False)
    # Bus line that the stop belongs to (e.g., "Line 1")
    line = Column(String, nullable=False)
    # Direction of the bus route at this stop (e.g., "Northbound")
    direction = Column(String, nullable=False)
    # Name of the bus stop (e.g., "Main Street & 1st Ave")
    stop_name = Column(String, nullable=False)

    # Geographic coordinates and spatial data
    latitude = Column(Float, nullable=False)  # Latitude of the bus stop
    longitude = Column(Float, nullable=False)  # Longitude of the bus stop
    # Geometry data (e.g., WKT or GeoJSON format)
    geometry = Column(String, nullable=False)
