from pydantic import BaseModel
from typing import Optional
from app.schemas.truck import TruckOut


class DriverCreate(BaseModel):
    full_name: str
    license_number: Optional[str]
    phone: Optional[str]
    company_id: Optional[int]
    truck_id: Optional[int] = None


class DriverOut(BaseModel):
    id: int
    full_name: str
    license_number: str | None
    phone: str | None
    company_id: int | None
    truck_id: int | None
    truck: TruckOut | None

    class Config:
        orm_mode = True
