from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models.maintenance import Maintenance
from app.schemas.truck import TruckOut
from app.schemas.driver import DriverOut
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class MaintenanceCreate(BaseModel):
    scheduled_date: datetime
    description: str
    truck_id: int

class MaintenanceOut(BaseModel):
    id: int
    scheduled_date: datetime
    description: str
    completed: bool
    truck_id: int

    class Config:
        orm_mode = True

@router.get("/", response_model=List[MaintenanceOut], tags=["maintenance"])
def list_maintenances(db: Session = Depends(get_db)):
    return db.query(Maintenance).order_by(Maintenance.scheduled_date.desc()).all()

@router.post("/", response_model=MaintenanceOut, tags=["maintenance"])
def create_maintenance(payload: MaintenanceCreate, db: Session = Depends(get_db)):
    m = Maintenance(scheduled_date=payload.scheduled_date, description=payload.description, completed=False, truck_id=payload.truck_id)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.patch("/{maint_id}/complete", response_model=MaintenanceOut, tags=["maintenance"])
def complete_maintenance(maint_id: int, db: Session = Depends(get_db)):
    m = db.query(Maintenance).filter(Maintenance.id == maint_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    m.completed = True
    db.commit()
    db.refresh(m)
    return m

@router.delete("/{maint_id}", tags=["maintenance"])
def delete_maintenance(maint_id: int, db: Session = Depends(get_db)):
    m = db.query(Maintenance).filter(Maintenance.id == maint_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    db.delete(m)
    db.commit()
    return {"detail": "deleted"}
