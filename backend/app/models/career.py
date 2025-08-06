from sqlalchemy import Column, Integer, String, Float, JSON, Text, Boolean
from ..db.base import Base

class Career(Base):
    __tablename__ = "careers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))  # Technology, Healthcare, Finance, etc.
    subcategory = Column(String(50))  # Software Development, Data Science, etc.
    
    # Descriptions
    description_en = Column(String(500), nullable=False)
    description_hi = Column(String(500), nullable=False)
    
    # Requirements
    required_skills = Column(Text)  # comma-separated
    interests = Column(Text)  # comma-separated
    min_education_level = Column(String(50))
    preferred_subjects = Column(String(200))
    
    # Additional fields that might be referenced
    title = Column(String(100))  # Alternative name field
    skills_required = Column(Text)  # Alternative to required_skills
    education_required = Column(Text)  # Education requirements
    experience_required = Column(Text)  # Experience requirements
    certifications = Column(Text)  # Required certifications
    
    # Academic requirements
    min_percentage_10th = Column(Float, default=0.0)
    min_percentage_12th = Column(Float, default=0.0)
    min_cgpa = Column(Float, default=0.0)
    
    # Market information
    local_demand = Column(String(20), default="Medium")  # High, Medium, Low
    average_salary_range = Column(String(50))  # "3-6 LPA", "10-15 LPA"
    growth_prospects = Column(String(20), default="Good")  # Excellent, Good, Average
    
    # Success metrics from training data
    placement_success_rate = Column(Float, default=0.0)
    peer_popularity_score = Column(Float, default=0.0)
    satisfaction_rating = Column(Float, default=0.0)
    
    # Industry information
    top_companies = Column(JSON)  # List of companies hiring for this role
    typical_job_roles = Column(JSON)  # List of typical job titles
    career_progression_path = Column(JSON)  # Career advancement steps
    
    # Educational pathways
    recommended_courses = Column(JSON)  # Degree programs, certifications
    skill_development_resources = Column(JSON)  # Learning resources
    
    # Location data
    geographic_demand = Column(JSON)  # Demand by region/state
    remote_work_feasibility = Column(String(20), default="Medium")
    
    # Metadata
    is_active = Column(Boolean, default=True)
    last_updated = Column(String(20))  # Data version timestamp
