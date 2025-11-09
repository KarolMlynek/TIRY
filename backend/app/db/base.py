from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.db.models import user, company, truck, driver, route, maintenance, service_record, fuel_log, gps_device, alert  # noqa: F401
