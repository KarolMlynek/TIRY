from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./fleet.db"

    class Config:
        env_file = ".env"

settings = Settings()
