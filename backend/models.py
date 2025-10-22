from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Creamos las tablas de la base de datos usando SQLAlchemy ORM

class Route(Base): 
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    waypoints = relationship("Waypoint", cascade="all, delete-orphan", back_populates="route", order_by="Waypoint.order_index")


class Waypoint(Base):
    __tablename__ = "waypoints"
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    order_index = Column(Integer, nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    route = relationship("Route", back_populates="waypoints")