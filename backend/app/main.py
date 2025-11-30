# backend/app/main.py
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes_auth, routes_trucks, routes_drivers
from app.db.session import engine
from app.db.base import Base
from seed import create_seed_data
from app.core.config import settings

logger = logging.getLogger("fleet_app")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fleet Management - API",
        version="0.1.0",
        description="API do zarządzania flotą ciągników siodłowych (demo)"
    )

    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(routes_trucks.router, prefix="/api/v1/trucks", tags=["trucks"])
    app.include_router(routes_drivers.router, prefix="/api/v1/drivers", tags=["drivers"])
    app.include_router(routes_stats.router, prefix="/api/v1/stats", tags=["stats"])
    app.include_router(routes_maintenance.router, prefix="/api/v1/maintenance", tags=["maintenance"])


    @app.get("/healthz", tags=["health"])
    def healthz():
        return {"status": "ok"}

    return app


app = create_app()


@app.on_event("startup")
def on_startup():
    try:
        logger.info("Tworzę tabelę/strukturę bazy (jeśli potrzebne)...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tabela(y) utworzone / zweryfikowane.")
    except Exception as e:
        logger.exception("Błąd przy tworzeniu tabel: %s", e)

    try:
        logger.info("Uruchamiam seed-data (demo)...")
        create_seed_data()
        logger.info("Seed-data wykonane.")
    except Exception as e:
        logger.exception("Błąd przy seed-data: %s", e)

    yield


app = FastAPI(
    title="Fleet Management - API",
    version="0.1.0",
    description="API do zarządzania flotą ciągników siodłowych (demo)",
    lifespan=lifespan
)

# CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(routes_trucks.router, prefix="/api/v1/trucks", tags=["trucks"])
app.include_router(routes_drivers.router, prefix="/api/v1/drivers", tags=["drivers"])

@app.get("/healthz", tags=["health"])
def healthz():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=5137, reload=True)
