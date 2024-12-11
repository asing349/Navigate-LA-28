from sqlalchemy import Column, Integer, String, Float
from models.base import Base


class BusStop(Base):
    __tablename__ = "bus_stops"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Bus stop information
    stop_number = Column(Integer, nullable=False)
    line = Column(String, nullable=False)
    direction = Column(String, nullable=False)
    stop_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    geometry = Column(String, nullable=False)
