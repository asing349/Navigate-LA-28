from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class BusRouteUsage(Base):
    __tablename__ = "bus_route_usage"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key linking to the users table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Foreign key linking to the origin bus stop
    origin_stop_id = Column(Integer, ForeignKey("bus_stops.id"), nullable=False)

    # Foreign key linking to the destination bus stop
    destination_stop_id = Column(Integer, ForeignKey("bus_stops.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="bus_route_usages")
    origin_stop = relationship("BusStop", foreign_keys=[origin_stop_id])
    destination_stop = relationship("BusStop", foreign_keys=[destination_stop_id])
