from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    app_name: str = "TSPRTG Tag Manager"
    database_url: str = "sqlite:///./tsprtg.db"
    # Use environment variable or generate random token if not set
    admin_token: Optional[str] = os.getenv("ADMIN_TOKEN")
    cors_origins: str = "*"  # String instead of list for env parsing
    
    class Config:
        env_file = ".env"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()

# Warn if using default/missing admin token
if not settings.admin_token:
    import warnings
    warnings.warn(
        "ADMIN_TOKEN not set! Please set a secure token in your .env file for production.",
        UserWarning
    )
