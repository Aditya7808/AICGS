"""
Improved CRUD operations with better type safety and security
"""
from sqlalchemy.orm import Session
from sqlalchemy import update
from ..models.user import User, UserProfile
from ..models.career import Career
from ..models.interaction import (
    UserInteraction, CareerOutcome, RecommendationCache, 
    AssessmentHistory, UserProgress, SkillProgress, CareerGoal
)
from ..models.education import EducationPathway, Institution, InstitutionPathway, Course
from ..core.security import get_password_hash
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

def safe_create_or_update_user_progress(db: Session, user_id: int) -> Optional[UserProgress]:
    """
    Safely create or update user progress tracking using proper ORM operations
    """
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
    
    if not progress:
        progress = UserProgress(user_id=user_id)
        db.add(progress)
        db.flush()  # Get the ID before updating
    
    # Count assessments
    assessment_count = db.query(AssessmentHistory).filter(
        AssessmentHistory.user_id == user_id
    ).count()
    
    # Get latest assessment date
    latest_assessment = db.query(AssessmentHistory).filter(
        AssessmentHistory.user_id == user_id
    ).order_by(AssessmentHistory.created_at.desc()).first()
    
    # Calculate profile completeness
    from .crud import get_user_profile, calculate_profile_completion
    user_profile = get_user_profile(db, user_id)
    profile_completeness = 0.0
    if user_profile:
        profile_completeness = calculate_profile_completion(user_profile) / 100.0
    
    # Count career goals and skills
    career_goals_count = db.query(CareerGoal).filter(CareerGoal.user_id == user_id).count()
    skills_count = db.query(SkillProgress).filter(SkillProgress.user_id == user_id).count()
    
    # Update using ORM methods (safe from SQL injection)
    progress.total_assessments_completed = assessment_count
    progress.career_goals_set = career_goals_count
    progress.skills_tracked = skills_count
    progress.profile_completeness = profile_completeness
    progress.last_assessment_date = latest_assessment.created_at if latest_assessment else None
    
    try:
        db.commit()
        db.refresh(progress)
        return progress
    except Exception as e:
        db.rollback()
        raise e

def safe_create_or_update_skill_progress(
    db: Session, 
    user_id: int, 
    skill_name: str, 
    current_level: str, 
    proficiency_score: float,
    target_level: Optional[str] = None
) -> Optional[SkillProgress]:
    """
    Safely create or update skill progress using proper ORM operations
    """
    skill_progress = db.query(SkillProgress).filter(
        SkillProgress.user_id == user_id,
        SkillProgress.skill_name == skill_name
    ).first()
    
    if not skill_progress:
        skill_progress = SkillProgress(
            user_id=user_id,
            skill_name=skill_name,
            current_level=current_level,
            proficiency_score=proficiency_score,
            target_level=target_level or current_level,
            progress_history=[],
            time_invested_hours=0.0
        )
        db.add(skill_progress)
    else:
        # Update existing skill progress using ORM
        old_score = skill_progress.proficiency_score
        skill_progress.current_level = current_level
        skill_progress.proficiency_score = proficiency_score
        if target_level:
            skill_progress.target_level = target_level
        
        # Add to progress history
        if skill_progress.progress_history is None:
            skill_progress.progress_history = []
        
        skill_progress.progress_history.append({
            "date": datetime.utcnow().isoformat(),
            "score": proficiency_score,
            "level": current_level
        })
        
        skill_progress.last_practice_date = datetime.utcnow()
    
    try:
        db.commit()
        db.refresh(skill_progress)
        return skill_progress
    except Exception as e:
        db.rollback()
        raise e

def safe_update_career_goal_progress(
    db: Session, 
    goal_id: int, 
    progress_percentage: float,
    completed_skills: Optional[List[str]] = None, 
    next_action: Optional[str] = None,
    links: Optional[List[dict]] = None
) -> Optional[CareerGoal]:
    """
    Safely update career goal progress using proper ORM operations
    """
    goal = db.query(CareerGoal).filter(CareerGoal.id == goal_id).first()
    if not goal:
        return None
    
    # Determine status based on progress
    status = "completed" if progress_percentage >= 100.0 else "active"
    
    # Update using ORM methods (safe from SQL injection)
    goal.progress_percentage = min(progress_percentage, 100.0)
    goal.status = status
    
    if completed_skills is not None:
        goal.completed_skills = completed_skills
    
    if next_action is not None:
        goal.next_action = next_action
    
    if links is not None:
        goal.links = links
    
    try:
        db.commit()
        db.refresh(goal)
        return goal
    except Exception as e:
        db.rollback()
        raise e

def safe_update_skill_time_invested(
    db: Session, 
    skill_id: int, 
    additional_hours: float
) -> Optional[SkillProgress]:
    """
    Safely update time invested in a skill
    """
    skill = db.query(SkillProgress).filter(SkillProgress.id == skill_id).first()
    if not skill:
        return None
    
    current_time = skill.time_invested_hours or 0.0
    skill.time_invested_hours = current_time + additional_hours
    skill.last_practice_date = datetime.utcnow()
    
    try:
        db.commit()
        db.refresh(skill)
        return skill
    except Exception as e:
        db.rollback()
        raise e

# Enhanced validation functions
def validate_skill_level(level: str) -> str:
    """Validate and normalize skill level"""
    valid_levels = ['beginner', 'intermediate', 'advanced', 'expert']
    normalized_level = level.lower().strip()
    return normalized_level if normalized_level in valid_levels else 'beginner'

def validate_goal_type(goal_type: str) -> str:
    """Validate and normalize goal type"""
    valid_types = ['primary', 'secondary', 'exploratory']
    normalized_type = goal_type.lower().strip()
    return normalized_type if normalized_type in valid_types else 'primary'

def validate_timeline(timeline: str) -> str:
    """Validate and normalize timeline"""
    valid_timelines = ['6_months', '1_year', '2_years', '5_years']
    return timeline if timeline in valid_timelines else '1_year'

def validate_status(status: str) -> str:
    """Validate and normalize status"""
    valid_statuses = ['active', 'paused', 'completed', 'dropped']
    normalized_status = status.lower().strip()
    return normalized_status if normalized_status in valid_statuses else 'active'

# Type-safe getters for model attributes
def safe_get_int(obj: Any, attr: str, default: int = 0) -> int:
    """Safely get integer attribute from SQLAlchemy model"""
    try:
        value = getattr(obj, attr, default)
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def safe_get_float(obj: Any, attr: str, default: float = 0.0) -> float:
    """Safely get float attribute from SQLAlchemy model"""
    try:
        value = getattr(obj, attr, default)
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def safe_get_str(obj: Any, attr: str, default: str = "") -> str:
    """Safely get string attribute from SQLAlchemy model"""
    try:
        value = getattr(obj, attr, default)
        return str(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def safe_get_list(obj: Any, attr: str, default: Optional[List] = None) -> List:
    """Safely get list attribute from SQLAlchemy model"""
    if default is None:
        default = []
    try:
        value = getattr(obj, attr, default)
        return list(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def create_sample_education_pathways(db: Session) -> None:
    """
    Create sample education pathways for demonstration
    """
    from ..models.education import EducationPathway, Institution, InstitutionPathway, Course
    
    # Check if sample data already exists
    existing_pathway = db.query(EducationPathway).first()
    if existing_pathway:
        return
    
    # Sample education pathways for Software Engineering (career_id = 1)
    pathways_data = [
        {
            "career_id": 1,
            "pathway_name": "BTech Computer Science Engineering",
            "pathway_type": "degree",
            "description": "4-year undergraduate degree program focusing on computer science fundamentals, programming, algorithms, and software development.",
            "duration_months": 48,
            "difficulty_level": "Intermediate",
            "min_education_level": "12th",
            "required_subjects": ["Physics", "Chemistry", "Mathematics"],
            "min_percentage": 75.0,
            "entrance_exams": ["JEE Main", "JEE Advanced", "BITSAT"],
            "estimated_cost_min": 200000.0,
            "estimated_cost_max": 1500000.0,
            "financial_aid_available": True,
            "scholarship_opportunities": ["Merit scholarships", "Need-based aid", "Government schemes"],
            "average_placement_rate": 85.0,
            "average_starting_salary": 600000.0,
            "top_recruiting_companies": ["Google", "Microsoft", "Amazon", "TCS", "Infosys"],
            "popularity_score": 9.2,
            "success_rate": 8.8
        },
        {
            "career_id": 1,
            "pathway_name": "Data Science Bootcamp",
            "pathway_type": "bootcamp",
            "description": "Intensive 6-month program covering data analysis, machine learning, and programming skills for immediate industry readiness.",
            "duration_months": 6,
            "difficulty_level": "Beginner",
            "min_education_level": "Graduate",
            "required_subjects": ["Mathematics", "Statistics"],
            "min_percentage": 60.0,
            "entrance_exams": [],
            "estimated_cost_min": 50000.0,
            "estimated_cost_max": 300000.0,
            "financial_aid_available": True,
            "scholarship_opportunities": ["Income share agreements", "Scholarship programs"],
            "average_placement_rate": 78.0,
            "average_starting_salary": 500000.0,
            "top_recruiting_companies": ["Flipkart", "Zomato", "PhonePe", "Startups"],
            "popularity_score": 8.5,
            "success_rate": 8.2
        },
        {
            "career_id": 2,  # Data Science
            "pathway_name": "MSc Data Science",
            "pathway_type": "degree",
            "description": "2-year postgraduate program specializing in advanced data analytics, machine learning, and statistical modeling.",
            "duration_months": 24,
            "difficulty_level": "Advanced",
            "min_education_level": "Graduate",
            "required_subjects": ["Mathematics", "Statistics", "Computer Science"],
            "min_percentage": 70.0,
            "entrance_exams": ["GATE", "Institution Specific"],
            "estimated_cost_min": 150000.0,
            "estimated_cost_max": 800000.0,
            "financial_aid_available": True,
            "scholarship_opportunities": ["Research assistantships", "Merit scholarships"],
            "average_placement_rate": 90.0,
            "average_starting_salary": 800000.0,
            "top_recruiting_companies": ["Google", "Facebook", "Netflix", "Uber"],
            "popularity_score": 8.8,
            "success_rate": 9.1
        }
    ]
    
    # Create pathways
    for pathway_data in pathways_data:
        pathway = EducationPathway(**pathway_data)
        db.add(pathway)
    
    db.flush()  # Get pathway IDs
    
    # Sample institutions
    institutions_data = [
        {
            "name": "Indian Institute of Technology Delhi",
            "short_name": "IIT Delhi",
            "institution_type": "university",
            "category": "government",
            "city": "New Delhi",
            "state": "Delhi",
            "website": "https://home.iitd.ac.in/",
            "ranking_national": 2,
            "ranking_global": 185,
            "facilities": ["Library", "Labs", "Hostel", "Sports", "Research Centers"],
            "student_strength": 11000,
            "faculty_count": 500
        },
        {
            "name": "Birla Institute of Technology and Science",
            "short_name": "BITS Pilani",
            "institution_type": "university", 
            "category": "deemed",
            "city": "Pilani",
            "state": "Rajasthan",
            "website": "https://www.bits-pilani.ac.in/",
            "ranking_national": 25,
            "ranking_global": 800,
            "facilities": ["Library", "Labs", "Hostel", "Sports", "Industry Partnerships"],
            "student_strength": 15000,
            "faculty_count": 800
        },
        {
            "name": "Scaler Academy",
            "short_name": "Scaler",
            "institution_type": "institute",
            "category": "private",
            "city": "Bangalore",
            "state": "Karnataka", 
            "website": "https://www.scaler.com/",
            "ranking_national": None,
            "ranking_global": None,
            "facilities": ["Online Platform", "Mentorship", "Career Services"],
            "student_strength": 5000,
            "faculty_count": 100
        }
    ]
    
    for inst_data in institutions_data:
        institution = Institution(**inst_data)
        db.add(institution)
    
    db.flush()  # Get institution IDs
    
    # Link institutions to pathways
    institution_pathway_mappings = [
        {
            "institution_id": 1,  # IIT Delhi
            "pathway_id": 1,      # BTech CSE
            "program_name": "BTech Computer Science and Engineering",
            "fees_per_year": 250000.0,
            "duration_years": 4.0,
            "entrance_exams_accepted": ["JEE Advanced"],
            "cutoff_scores": {"JEE_Advanced_Rank": 500},
            "seats_available": 120,
            "placement_statistics": {"placement_rate": 95, "highest_package": 1800000, "average_package": 1200000},
            "application_fee": 2800.0
        },
        {
            "institution_id": 2,  # BITS Pilani
            "pathway_id": 1,      # BTech CSE
            "program_name": "BE Computer Science",
            "fees_per_year": 450000.0,
            "duration_years": 4.0,
            "entrance_exams_accepted": ["BITSAT"],
            "cutoff_scores": {"BITSAT_Score": 350},
            "seats_available": 150,
            "placement_statistics": {"placement_rate": 90, "highest_package": 1500000, "average_package": 900000},
            "application_fee": 3000.0
        },
        {
            "institution_id": 3,  # Scaler
            "pathway_id": 2,      # Data Science Bootcamp
            "program_name": "Data Science & Machine Learning",
            "fees_per_year": 250000.0,
            "duration_years": 0.5,
            "entrance_exams_accepted": [],
            "cutoff_scores": {},
            "seats_available": 100,
            "placement_statistics": {"placement_rate": 80, "highest_package": 800000, "average_package": 600000},
            "application_fee": 1000.0
        }
    ]
    
    for mapping in institution_pathway_mappings:
        inst_pathway = InstitutionPathway(**mapping)
        db.add(inst_pathway)
    
    # Sample courses for BTech CSE pathway
    courses_data = [
        {
            "pathway_id": 1,
            "name": "Programming Fundamentals",
            "code": "CS101",
            "credits": 4,
            "semester": 1,
            "description": "Introduction to programming concepts using C/C++",
            "topics_covered": ["Variables", "Control Structures", "Functions", "Arrays", "Pointers"],
            "skills_gained": ["Programming Logic", "Problem Solving", "Debugging"],
            "course_type": "theory_practical",
            "delivery_mode": "offline"
        },
        {
            "pathway_id": 1,
            "name": "Data Structures and Algorithms",
            "code": "CS201",
            "credits": 4,
            "semester": 3,
            "description": "Study of fundamental data structures and algorithms",
            "topics_covered": ["Arrays", "Linked Lists", "Trees", "Graphs", "Sorting", "Searching"],
            "skills_gained": ["Algorithm Design", "Complexity Analysis", "Optimization"],
            "course_type": "theory_practical", 
            "delivery_mode": "offline"
        },
        {
            "pathway_id": 1,
            "name": "Database Management Systems",
            "code": "CS301",
            "credits": 3,
            "semester": 5,
            "description": "Principles of database design and management",
            "topics_covered": ["ER Modeling", "SQL", "Normalization", "Transactions", "Indexing"],
            "skills_gained": ["Database Design", "SQL Programming", "Data Modeling"],
            "course_type": "theory_practical",
            "delivery_mode": "offline"
        }
    ]
    
    for course_data in courses_data:
        course = Course(**course_data)
        db.add(course)
    
    try:
        db.commit()
        logger.info("Sample education pathways created successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating sample education pathways: {e}")

def get_education_pathways_for_career(db: Session, career_id: int, filters: Optional[Dict[str, Any]] = None) -> List[EducationPathway]:
    """
    Get education pathways for a specific career with optional filters
    """
    from ..models.education import EducationPathway
    
    query = db.query(EducationPathway).filter(EducationPathway.career_id == career_id)
    
    if filters:
        if filters.get("education_level"):
            query = query.filter(EducationPathway.min_education_level == filters["education_level"])
        if filters.get("budget_max"):
            query = query.filter(EducationPathway.estimated_cost_max <= filters["budget_max"])
        if filters.get("pathway_type"):
            query = query.filter(EducationPathway.pathway_type == filters["pathway_type"])
    
    return query.order_by(
        EducationPathway.success_rate.desc(),
        EducationPathway.popularity_score.desc()
    ).all()

def get_institutions_for_pathway(db: Session, pathway_id: int, filters: Optional[Dict[str, Any]] = None) -> List[InstitutionPathway]:
    """
    Get institutions offering a specific education pathway
    """
    from ..models.education import InstitutionPathway, Institution
    
    query = db.query(InstitutionPathway).filter(
        InstitutionPathway.pathway_id == pathway_id,
        InstitutionPathway.is_active == True
    ).join(Institution)
    
    if filters:
        if filters.get("location"):
            query = query.filter(Institution.state.ilike(f"%{filters['location']}%"))
        if filters.get("ranking_max"):
            query = query.filter(Institution.ranking_national <= filters["ranking_max"])
        if filters.get("fees_max"):
            query = query.filter(InstitutionPathway.fees_per_year <= filters["fees_max"])
    
    return query.order_by(Institution.ranking_national.asc()).all()
