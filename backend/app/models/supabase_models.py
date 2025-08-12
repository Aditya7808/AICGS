"""
Supabase-compatible models for CareerBuddy
These models work with Supabase auth.users and PostgreSQL UUIDs
"""

from sqlalchemy import Column, String, DateTime, Float, JSON, Text, Boolean, Integer, DECIMAL, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..db.base import Base

class Profile(Base):
    """User profile linked to Supabase auth.users"""
    __tablename__ = "profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

class UserProfile(Base):
    """Multi-dimensional user profile for MARE system"""
    __tablename__ = "user_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True, unique=True)
    
    # Personal dimensions
    age = Column(Integer)
    education_level = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    
    # Cultural dimensions
    cultural_context = Column(String(100), nullable=False)
    family_background = Column(String(100), nullable=False)
    language_preference = Column(String(10), default='en')
    
    # Economic dimensions
    economic_context = Column(String(100), nullable=False)
    financial_constraints = Column(Text)
    
    # Geographic dimensions
    geographic_constraints = Column(String(200), nullable=False)
    urban_rural_type = Column(String(20), default='urban')
    infrastructure_level = Column(String(20), default='good')
    
    # Social dimensions
    family_expectations = Column(String(200), nullable=False)
    peer_influence_score = Column(DECIMAL(3,2), default=0.5)
    community_values = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class CareerPreferences(Base):
    """Career preferences and goals"""
    __tablename__ = "career_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True, unique=True)
    
    # Career aspirations
    career_goals = Column(Text, default='')
    preferred_industries = Column(ARRAY(String), default=[])
    work_environment_preference = Column(String(20), default='office')
    salary_expectations = Column(String(100), default='')
    work_life_balance_priority = Column(Integer, default=5)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class UserSkillsInterests(Base):
    """Skills and interests with weights"""
    __tablename__ = "user_skills_interests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True, unique=True)
    
    # Skills and interests data
    skills = Column(ARRAY(String), default=[])
    interests = Column(ARRAY(String), default=[])
    skill_weights = Column(JSON, default={})
    interest_weights = Column(JSON, default={})
    
    # Calculated skill category scores (0.0 to 1.0)
    technical_skills_score = Column(DECIMAL(3,2), default=0.0)
    creative_skills_score = Column(DECIMAL(3,2), default=0.0)
    analytical_skills_score = Column(DECIMAL(3,2), default=0.0)
    communication_skills_score = Column(DECIMAL(3,2), default=0.0)
    leadership_skills_score = Column(DECIMAL(3,2), default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class CareerOpportunity(Base):
    """Career opportunities database"""
    __tablename__ = "career_opportunities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic career information
    title = Column(String(200), nullable=False)
    industry = Column(String(100), nullable=False)
    description = Column(Text, default='')
    required_skills = Column(ARRAY(String), default=[])
    preferred_skills = Column(ARRAY(String), default=[])
    
    # Career characteristics
    experience_level = Column(String(20), default='entry')
    salary_range_min = Column(Integer, default=0)
    salary_range_max = Column(Integer, default=0)
    currency = Column(String(10), default='INR')
    
    # Location and availability
    location = Column(String(200), default='')
    remote_available = Column(Boolean, default=False)
    urban_rural_suitability = Column(String(20), default='both')
    
    # MARE-specific fields
    traditional_modern_spectrum = Column(String(20), default='balanced')
    cultural_adaptability_score = Column(DECIMAL(3,2), default=0.5)
    economic_accessibility_score = Column(DECIMAL(3,2), default=0.5)
    geographic_flexibility_score = Column(DECIMAL(3,2), default=0.5)
    family_acceptance_score = Column(DECIMAL(3,2), default=0.5)
    
    # Future outlook
    growth_potential_score = Column(DECIMAL(3,2), default=0.5)
    job_security_score = Column(DECIMAL(3,2), default=0.5)
    automation_risk_score = Column(DECIMAL(3,2), default=0.5)
    future_outlook = Column(String(20), default='stable')
    
    # AI/ML Integration
    mare_compatibility_score = Column(DECIMAL(3,2), default=0.0)
    recommendation_count = Column(Integer, default=0)
    positive_feedback_rate = Column(DECIMAL(3,2), default=0.0)
    
    # Status and metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class RecommendationFeedback(Base):
    """Feedback and learning data for MARE"""
    __tablename__ = "recommendation_feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    career_opportunity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Recommendation context
    recommendation_score = Column(DECIMAL(4,3), nullable=False)
    
    # User feedback
    user_rating = Column(Integer)
    user_feedback = Column(Text)
    selected = Column(Boolean, default=False)
    time_spent_viewing = Column(Integer, default=0)  # seconds
    
    # Context for learning
    context_snapshot = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Add unique constraint in the model
    __table_args__ = (
        {'sqlite_autoincrement': True}
    )
