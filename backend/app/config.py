from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "TSPRTG Tag Manager"
    database_url: str = "sqlite:///./tsprtg.db"
    admin_token: Optional[str] = "your-secret-token-here"
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"


settings = Settings()
