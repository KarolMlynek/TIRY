from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    truck_id = Column(Integer, ForeignKey("trucks.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    origin = Column(String)
    destination = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    distance_km = Column(Float, default=0.0)

    truck = relationship("Truck")
    driver = relationship("Driver")
