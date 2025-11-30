from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.truck import Truck
from app.db.models.driver import Driver
from app.db.models.maintenance import Maintenance
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/", tags=["stats"])
def get_stats(db: Session = Depends(get_db)):
    """Proste statystyki dla dashboardu"""
    trucks_count = db.query(Truck).count()
    drivers_count = db.query(Driver).count()


    now = datetime.utcnow()
    soon = now + timedelta(days=7)
    upcoming_maint = db.query(Maintenance).filter(Maintenance.scheduled_date >= now, Maintenance.scheduled_date <= soon).count()


    overdue = db.query(Maintenance).filter(Maintenance.completed == False, Maintenance.scheduled_date < now).count()
    in_progress = db.query(Maintenance).filter(Maintenance.completed == False, Maintenance.scheduled_date >= now).count()

    return {
        "trucks_count": trucks_count,
        "drivers_count": drivers_count,
        "upcoming_maintenances_7d": upcoming_maint,
        "overdue_maintenances": overdue,
        "in_progress_maintenances": in_progress,
    }
