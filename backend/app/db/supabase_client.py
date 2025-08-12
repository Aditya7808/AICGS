"""
Supabase client configuration for CareerBuddy
"""

from supabase import create_client, Client
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
import logging
import os

from ..core.config import settings

logger = logging.getLogger(__name__)

class SupabaseManager:
    """Manages Supabase connection and client"""
    
    def __init__(self):
        self.supabase_client: Optional[Client] = None
        self._engine = None
        self._session_local = None
        self._base = declarative_base()
    
    def initialize(self):
        """Initialize Supabase client and SQLAlchemy engine"""
        if not settings.supabase_url or not settings.supabase_anon_key:
            raise ValueError("Supabase URL and anon key must be provided")
        
        # Create Supabase client
        self.supabase_client = create_client(
            settings.supabase_url,
            settings.supabase_anon_key
        )
        
        # Create SQLAlchemy engine for direct database operations
        if settings.database_url:
            self._engine = create_engine(
                settings.database_url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                echo=False  # Set to True for SQL debugging
            )
            self._session_local = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=self._engine
            )
            logger.info("Supabase database connection established")
        
    @property
    def client(self) -> Client:
        """Get Supabase client"""
        if not self.supabase_client:
            self.initialize()
        return self.supabase_client
    
    @property
    def engine(self):
        """Get SQLAlchemy engine"""
        if not self._engine:
            self.initialize()
        return self._engine
    
    @property
    def SessionLocal(self):
        """Get SQLAlchemy session maker"""
        if not self._session_local:
            self.initialize()
        return self._session_local
    
    @property
    def Base(self):
        """Get SQLAlchemy base"""
        return self._base
    
    def get_db(self):
        """Database dependency for FastAPI"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def create_tables(self):
        """Create database tables"""
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
        
        # Create all tables
        self.Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created successfully")

# Global instance
supabase_manager = SupabaseManager()

# Initialize on module import
try:
    if all([settings.supabase_url, settings.supabase_anon_key, settings.database_url]):
        supabase_manager.initialize()
        logger.info("Supabase manager initialized successfully")
    else:
        logger.warning("Supabase credentials not provided, initialization skipped")
except Exception as e:
    logger.error(f"Failed to initialize Supabase manager: {e}")

# Convenience exports
def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    return supabase_manager.client

def get_supabase_service_client() -> Client:
    """Get Supabase service client with service role key (bypasses RLS)"""
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise ValueError("Supabase URL and service role key must be provided")
    
    return create_client(
        settings.supabase_url,
        settings.supabase_service_role_key
    )

def get_db():
    """Database session dependency"""
    return supabase_manager.get_db()

def create_tables():
    """Create database tables"""
    return supabase_manager.create_tables()

# SQLAlchemy exports for compatibility
def get_engine():
    """Get SQLAlchemy engine"""
    return supabase_manager.engine

def get_session_local():
    """Get SessionLocal"""
    return supabase_manager.SessionLocal
