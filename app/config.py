from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Health Platform API"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True

settings = Settings()
