from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

# Ensure we're using Supabase PostgreSQL
if not settings.database_url:
    raise ValueError("DATABASE_URL environment variable is required for Supabase connection")

if "sqlite" in settings.database_url.lower():
    raise ValueError("SQLite is not supported. Please use Supabase PostgreSQL DATABASE_URL")

# Create engine with Supabase PostgreSQL
engine = create_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False  # Set to True for SQL debugging
)

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
    from ..models.supabase_models import (
        Profile, UserProfile as SupabaseUserProfile, CareerPreferences,
        UserSkillsInterests, CareerOpportunity, RecommendationFeedback
    )
    
    # Create all tables (don't drop in production)
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully with Supabase PostgreSQL")
