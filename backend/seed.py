from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.company import Company
from app.db.models.truck import Truck
from app.db.models.driver import Driver
from app.core.security import get_password_hash


def create_seed_data():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == 'admin@example.com').first():
            admin = User(email='admin@example.com', full_name='Admin', hashed_password=get_password_hash('adminpass'), role='admin')
            db.add(admin)
        if not db.query(Company).filter(Company.name == 'Demo Fleet').first():
            company = Company(name='Demo Fleet', address='Demo Street 1')
            db.add(company)
            db.flush()  # ensure company.id is available
            truck = Truck(vin='VIN1234567890', registration_number='ABC1234', brand='Volvo', company_id=company.id)
            db.add(truck)
            driver = Driver(full_name='Jan Kowalski', license_number='DL12345', phone='+48123456789', company_id=company.id)
            db.add(driver)
        db.commit()
    finally:
        db.close()
