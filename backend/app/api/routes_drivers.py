from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.driver import Driver
from app.schemas.driver import DriverCreate, DriverOut
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=list[DriverOut])
def list_drivers(db: Session = Depends(get_db)):
    return db.query(Driver).all()

@router.post("/", response_model=DriverOut)
def create_driver(payload: DriverCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    d = Driver(full_name=payload.full_name, license_number=payload.license_number, phone=payload.phone, company_id=payload.company_id)
    db.add(d)
    db.commit()
    db.refresh(d)
    return d
