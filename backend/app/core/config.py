from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Supabase Configuration (Required)
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""  # Add JWT secret for token verification
    database_url: str = ""
    
    # Frontend Configuration
    frontend_url: str = "http://localhost:3000"
    
    # Application Configuration
    api_version: str = "v2.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Recommendation Engine Settings
    content_filter_weight: float = 0.6
    collaborative_filter_weight: float = 0.4
    recommendation_cache_ttl: int = 24
    
    # SVM Model Configuration
    svm_min_training_samples: int = 10
    svm_confidence_threshold: float = 0.7
    
    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields from environment

settings = Settings()

def get_settings() -> Settings:
    """Get application settings instance"""
    return settings
