from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Text
from sqlalchemy.sql import func
from ..db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Academic Information
    education_level = Column(String(50))  # High School, Undergraduate, Postgraduate, etc.
    current_course = Column(String(100))  # B.Tech (Computer Science), 12th Grade, etc.
    current_institution = Column(String(200))  # School/College name
    institution_type = Column(String(50))  # Government, Private, IIT, etc.
    
    # Academic Scores
    tenth_percentage = Column(Float)
    twelfth_percentage = Column(Float)
    current_cgpa = Column(Float)
    current_marks_type = Column(String(20))  # Percentage, CGPA
    current_marks_value = Column(Float)
    
    # Geographic & Background
    place_of_residence = Column(String(100))
    residence_type = Column(String(20))  # Rural, Urban, Semi-Urban, Metro
    family_background = Column(String(30))  # Lower Income, Middle Income, Upper Income
    
    # Interests & Skills
    interests = Column(Text)  # Pipe-separated like "Coding|AI|Gaming"
    skills = Column(Text)  # Pipe-separated skills
    career_goals = Column(Text)  # Primary career aspirations
    
    # Assessment Data
    assessment_responses = Column(JSON)  # Store detailed assessment responses
    preferred_work_environment = Column(String(50))
    financial_considerations = Column(String(50))
    location_preferences = Column(Text)
    
    # Metadata
    profile_completion_percentage = Column(Float, default=0.0)
    last_assessment_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
