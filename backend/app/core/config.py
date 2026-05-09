from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "Northscale AI Terminal"
    API_V1_STR: str = "/api/v1"
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # AI
    GROQ_API_KEY: str
    PRIMARY_MODEL: str = "llama-3.3-70b-versatile"
    
    # Security
    SECRET_KEY: str = "DEV_SECRET_REPLACE_IN_PROD"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()
