from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import routes_trucks, routes_drivers, routes_auth
from app.db.session import engine, Base
from app.seed import create_seed_data

# Create DB tables and seed minimal data for demo
Base.metadata.create_all(bind=engine)
create_seed_data()

app = FastAPI(title="Fleet Management - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(routes_trucks.router, prefix="/api/v1/trucks", tags=["trucks"])
app.include_router(routes_drivers.router, prefix="/api/v1/drivers", tags=["drivers"])


@app.get("/")
def root():
    return {"message": "Fleet Management API"}
