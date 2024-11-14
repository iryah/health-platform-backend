# app/config.py
from pydantic import BaseModel

class Settings(BaseModel):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Health Platform API"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./health_platform.db"
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]

    class Config:
        from_attributes = True

settings = Settings()
