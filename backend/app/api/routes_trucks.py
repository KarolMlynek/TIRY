from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.crud import crud_truck
from backend.app.schemas.truck import TruckCreate, TruckOut
from backend.app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=list[TruckOut])
def list_trucks(db: Session = Depends(get_db)):
    return crud_truck.get_all_trucks(db)

@router.post("/", response_model=TruckOut)
def create_truck(payload: TruckCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    t = crud_truck.create_truck(db, vin=payload.vin, registration_number=payload.registration_number, brand=payload.brand)
    return t

@router.get("/{truck_id}", response_model=TruckOut)
def get_truck(truck_id: int, db: Session = Depends(get_db)):
    t = crud_truck.get_truck(db, truck_id)
    if not t:
        raise HTTPException(status_code=404, detail="Truck not found")
    return t
