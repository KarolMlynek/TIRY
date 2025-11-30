from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=True)
    quantity = Column(Integer, default=0)
    min_qty = Column(Integer, default=0)
    unit_price = Column(Float, default=0.0)
