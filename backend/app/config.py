from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    app_name: str = "TSPRTG Tag Manager"
    database_url: str = "sqlite:///./tsprtg.db"
    # Use environment variable or generate random token if not set
    admin_token: Optional[str] = os.getenv("ADMIN_TOKEN")
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"


settings = Settings()

# Warn if using default/missing admin token
if not settings.admin_token:
    import warnings
    warnings.warn(
        "ADMIN_TOKEN not set! Please set a secure token in your .env file for production.",
        UserWarning
    )
