from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    license_number = Column(String, unique=True)
    phone = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="drivers")
    routes = relationship("Route", back_populates="driver")
    fuel_logs = relationship("FuelLog", back_populates="driver")
    truck_id = Column(Integer, ForeignKey("trucks.id"), nullable=True)
    truck = relationship("Truck", back_populates="drivers")
