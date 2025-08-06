from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ..core.config import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    # Import all models to ensure they're registered
    from ..models.user import User, UserProfile
    from ..models.career import Career
    from ..models.interaction import (
        UserInteraction, CareerOutcome, RecommendationCache, 
        AssessmentHistory, UserProgress, SkillProgress, CareerGoal
    )
    from ..models.education import (
        EducationPathway, Course, Institution, InstitutionPathway, AdmissionProcess
    )
    
    # For development: drop all tables and recreate to ensure schema is up to date
    # In production, you would use proper database migrations (Alembic)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
