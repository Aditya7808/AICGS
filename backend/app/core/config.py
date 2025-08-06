from pydantic import BaseModel

class Settings(BaseModel):
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./careerbuddy.db"

settings = Settings()
