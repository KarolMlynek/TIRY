from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Truck(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True, nullable=False)
    registration_number = Column(String, unique=True, nullable=False)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    mileage = Column(Float, default=0.0)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="trucks")
    gps_device = relationship("GPSDevice", back_populates="truck", uselist=False)
    routes = relationship("Route", back_populates="truck")
    maintenances = relationship("Maintenance", back_populates="truck")
    fuel_logs = relationship("FuelLog", back_populates="truck")
    alerts = relationship("Alert", back_populates="truck")
    drivers = relationship("Driver", back_populates="truck")
