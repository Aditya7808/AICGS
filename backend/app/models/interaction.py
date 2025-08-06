from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Text, Boolean
from sqlalchemy.sql import func
from ..db.base import Base

class UserInteraction(Base):
    """Track user interactions for collaborative filtering"""
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    career_id = Column(Integer, nullable=True, index=True)
    
    # Interaction Types: view, bookmark, share, rate, apply
    interaction_type = Column(String(20), nullable=False)
    
    # For rating-based interactions (1-10 scale)
    rating = Column(Float, nullable=True)
    
    # Additional context data
    session_id = Column(String(100))
    context_data = Column(JSON)  # Store additional interaction context
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CareerOutcome(Base):
    """Store career outcomes from training data"""
    __tablename__ = "career_outcomes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Profile matching fields (from CSV)
    education_level = Column(String(50))
    course_of_study = Column(String(100))
    institution_type = Column(String(100))
    marks_type = Column(String(20))
    marks_value = Column(Float)
    residence_type = Column(String(20))
    family_background = Column(String(30))
    interests = Column(Text)  # Pipe-separated
    
    # Outcome fields
    next_path = Column(String(50))  # Job, Higher Education, Undecided
    company_name = Column(String(200), nullable=True)
    job_role = Column(String(100), nullable=True)
    placement_status = Column(String(30))
    next_course = Column(String(100), nullable=True)
    next_institution = Column(String(200), nullable=True)
    admission_status = Column(String(30), nullable=True)
    
    # Success indicators
    is_successful_outcome = Column(Boolean, default=True)
    outcome_satisfaction_score = Column(Float, nullable=True)
    
    # Metadata
    data_source = Column(String(50), default="training_csv")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RecommendationCache(Base):
    """Cache recommendations for performance"""
    __tablename__ = "recommendation_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    user_profile_hash = Column(String(64), nullable=False, index=True)
    
    # Cached recommendation data
    recommendations_json = Column(JSON)
    content_score = Column(Float)
    collaborative_score = Column(Float)
    hybrid_score = Column(Float)
    confidence_level = Column(Float)
    
    # Cache metadata
    algorithm_version = Column(String(20), default="v1.0")
    cache_expiry = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AssessmentHistory(Base):
    """Track assessment history for learning"""
    __tablename__ = "assessment_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Assessment data
    assessment_type = Column(String(50))  # career_assessment, skill_assessment, etc.
    responses = Column(JSON)  # Store all assessment responses
    scores = Column(JSON)  # Calculated scores per category
    
    # Results
    top_career_recommendations = Column(JSON)
    skill_gaps_identified = Column(JSON)
    learning_paths_suggested = Column(JSON)
    
    # Metadata
    completion_time_minutes = Column(Float)
    assessment_version = Column(String(20), default="v1.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserProgress(Base):
    """Track overall user progress and milestones"""
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True, unique=True)
    
    # Progress metrics
    total_assessments_completed = Column(Integer, default=0)
    last_assessment_date = Column(DateTime(timezone=True))
    career_goals_set = Column(Integer, default=0)
    skills_tracked = Column(Integer, default=0)
    
    # Achievement tracking
    milestones_achieved = Column(JSON)  # List of achievement IDs
    current_streak_days = Column(Integer, default=0)
    longest_streak_days = Column(Integer, default=0)
    
    # Progress scores (0.0 to 1.0)
    profile_completeness = Column(Float, default=0.0)
    skill_development_score = Column(Float, default=0.0)
    career_clarity_score = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SkillProgress(Base):
    """Track individual skill development over time"""
    __tablename__ = "skill_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    skill_name = Column(String(100), nullable=False)
    
    # Skill metrics
    current_level = Column(String(20))  # beginner, intermediate, advanced, expert
    proficiency_score = Column(Float, default=0.0)  # 0.0 to 1.0
    target_level = Column(String(20))
    target_date = Column(DateTime(timezone=True))
    
    # Learning tracking
    resources_completed = Column(JSON)  # List of completed learning resources
    time_invested_hours = Column(Float, default=0.0)
    last_practice_date = Column(DateTime(timezone=True))
    
    # Progress history
    progress_history = Column(JSON)  # [{"date": "2025-01-01", "score": 0.3}, ...]
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class CareerGoal(Base):
    """Track user's career goals and progress towards them"""
    __tablename__ = "career_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    career_id = Column(Integer, nullable=False)  # References Career table
    
    # Goal details
    goal_type = Column(String(50))  # primary, secondary, exploratory
    target_timeline = Column(String(50))  # 6_months, 1_year, 2_years, 5_years
    priority_level = Column(Integer, default=1)  # 1=highest, 5=lowest
    
    # Status tracking
    status = Column(String(20), default="active")  # active, paused, completed, dropped
    progress_percentage = Column(Float, default=0.0)  # 0.0 to 100.0
    
    # Requirements tracking
    required_skills = Column(JSON)  # Skills needed for this career
    completed_skills = Column(JSON)  # Skills user has acquired
    learning_plan = Column(JSON)  # Structured learning plan
    
    # Milestones and links
    milestones = Column(JSON)  # [{"name": "Complete Python", "completed": true, "date": "2025-01-01"}]
    links = Column(JSON)  # [{"title": "Python Course", "url": "https://...", "type": "course"}]
    next_action = Column(Text)  # What user should do next
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    target_completion_date = Column(DateTime(timezone=True))
