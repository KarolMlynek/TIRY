from sqlalchemy.orm import Session, selectinload
from app.db.models.driver import Driver


def assign_truck(db: Session, driver_id: int, truck_id: int | None):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        return None
    driver.truck_id = truck_id
    db.commit()
    db.refresh(driver)
    return driver

def get_all(db: Session):
    return db.query(Driver).options(selectinload(Driver.truck)).all()