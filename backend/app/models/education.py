"""
Education pathway models for comprehensive educational guidance
"""
from sqlalchemy import Column, Integer, String, Float, JSON, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base import Base

class EducationPathway(Base):
    """
    Comprehensive education pathway information for careers
    """
    __tablename__ = "education_pathways"
    
    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("careers.id"), nullable=False)
    pathway_name = Column(String(200), nullable=False)  # "BTech Computer Science", "Data Science Bootcamp"
    pathway_type = Column(String(50), nullable=False)  # "degree", "certification", "bootcamp", "diploma"
    
    # Basic information
    description = Column(Text)
    duration_months = Column(Integer)  # Total duration in months
    difficulty_level = Column(String(20))  # "Beginner", "Intermediate", "Advanced"
    
    # Prerequisites
    min_education_level = Column(String(50))  # "10th", "12th", "Graduate"
    required_subjects = Column(JSON)  # ["Physics", "Chemistry", "Mathematics"]
    min_percentage = Column(Float)  # Minimum percentage required
    entrance_exams = Column(JSON)  # List of entrance exams
    
    # Cost information
    estimated_cost_min = Column(Float)  # Minimum cost in INR
    estimated_cost_max = Column(Float)  # Maximum cost in INR
    financial_aid_available = Column(Boolean, default=False)
    scholarship_opportunities = Column(JSON)  # List of scholarship programs
    
    # Outcome information
    average_placement_rate = Column(Float)  # Percentage
    average_starting_salary = Column(Float)  # Starting salary in INR
    top_recruiting_companies = Column(JSON)  # List of companies
    
    # Metadata
    popularity_score = Column(Float, default=0.0)  # Based on user selections
    success_rate = Column(Float, default=0.0)  # Career success after this pathway
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Course(Base):
    """
    Specific courses within education pathways
    """
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    pathway_id = Column(Integer, ForeignKey("education_pathways.id"))
    
    # Course details
    name = Column(String(200), nullable=False)
    code = Column(String(50))  # Course code like "CS101"
    credits = Column(Integer)
    semester = Column(Integer)  # Which semester/year
    
    # Content
    description = Column(Text)
    topics_covered = Column(JSON)  # List of topics
    skills_gained = Column(JSON)  # Skills acquired from this course
    
    # Delivery
    course_type = Column(String(50))  # "theory", "practical", "project"
    delivery_mode = Column(String(50))  # "online", "offline", "hybrid"
    
    # Assessment
    assessment_methods = Column(JSON)  # ["exam", "project", "assignment"]
    pass_criteria = Column(String(100))
    
    # Prerequisites
    prerequisite_courses = Column(JSON)  # List of prerequisite course IDs
    recommended_preparation = Column(Text)

class Institution(Base):
    """
    Educational institutions offering pathways
    """
    __tablename__ = "institutions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic information
    name = Column(String(200), nullable=False)
    short_name = Column(String(50))  # "IIT Delhi", "BITS Pilani"
    institution_type = Column(String(50))  # "university", "college", "institute"
    category = Column(String(50))  # "government", "private", "deemed"
    
    # Location
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100), default="India")
    location_coordinates = Column(JSON)  # {"lat": 28.6139, "lng": 77.2090}
    
    # Contact information
    website = Column(String(200))
    contact_email = Column(String(100))
    contact_phone = Column(String(20))
    address = Column(Text)
    
    # Reputation metrics
    ranking_national = Column(Integer)  # National ranking
    ranking_global = Column(Integer)  # Global ranking
    accreditation = Column(JSON)  # List of accreditations
    
    # Infrastructure
    facilities = Column(JSON)  # ["library", "labs", "hostel", "sports"]
    campus_size_acres = Column(Float)
    student_strength = Column(Integer)
    faculty_count = Column(Integer)
    
    # Admission information
    application_deadlines = Column(JSON)  # Different deadlines for different programs
    selection_process = Column(JSON)  # Steps in selection process
    acceptance_rate = Column(Float)  # Percentage of applicants accepted

class InstitutionPathway(Base):
    """
    Junction table linking institutions to education pathways
    """
    __tablename__ = "institution_pathways"
    
    id = Column(Integer, primary_key=True, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    pathway_id = Column(Integer, ForeignKey("education_pathways.id"), nullable=False)
    
    # Specific details for this institution's offering
    program_name = Column(String(200))  # Institution-specific program name
    fees_per_year = Column(Float)  # Annual fees in INR
    duration_years = Column(Float)  # Duration at this specific institution
    
    # Admission specifics
    entrance_exams_accepted = Column(JSON)  # ["JEE", "BITSAT", "Institution Specific"]
    cutoff_scores = Column(JSON)  # Historical cutoff data
    seats_available = Column(Integer)
    reservation_policy = Column(JSON)  # Reservation categories and percentages
    
    # Outcomes specific to this institution
    placement_statistics = Column(JSON)  # Detailed placement data
    alumni_network_strength = Column(Float)  # Alumni network score
    industry_partnerships = Column(JSON)  # List of industry partners
    
    # Application information
    application_fee = Column(Float)
    application_process = Column(JSON)  # Step-by-step application process
    required_documents = Column(JSON)  # List of required documents
    
    # Status
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())

class AdmissionProcess(Base):
    """
    Detailed admission process information
    """
    __tablename__ = "admission_processes"
    
    id = Column(Integer, primary_key=True, index=True)
    institution_pathway_id = Column(Integer, ForeignKey("institution_pathways.id"), nullable=False)
    
    # Process details
    process_name = Column(String(100))  # "JEE Main + JEE Advanced"
    process_type = Column(String(50))  # "entrance_exam", "merit_based", "interview"
    
    # Timeline
    application_start_date = Column(String(50))  # "January 2025"
    application_end_date = Column(String(50))
    exam_dates = Column(JSON)  # List of exam dates
    result_declaration_date = Column(String(50))
    counseling_dates = Column(JSON)
    
    # Requirements
    eligibility_criteria = Column(JSON)  # Detailed eligibility requirements
    required_documents = Column(JSON)
    exam_pattern = Column(JSON)  # Detailed exam pattern
    syllabus = Column(JSON)  # Exam syllabus topics
    
    # Preparation guidance
    recommended_preparation_time = Column(Integer)  # Months needed for preparation
    preparation_resources = Column(JSON)  # Books, online courses, coaching
    previous_year_papers = Column(JSON)  # Links to previous year papers
    
    # Success metrics
    difficulty_level = Column(String(20))  # "Easy", "Moderate", "Difficult"
    success_tips = Column(JSON)  # Tips for success in this process
