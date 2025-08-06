from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel, Field, validator, constr
from typing import List, Dict, Any, Optional, Union, Literal
from datetime import datetime, timedelta
from ..db.base import get_db
from ..db.crud import (
    create_or_update_user_progress, get_user_progress,
    create_or_update_skill_progress, get_user_skill_progress,
    create_career_goal, get_user_career_goals, update_career_goal_progress,
    get_user_assessment_history, save_assessment_history
)
from ..db.crud_improved import (
    safe_create_or_update_user_progress, safe_create_or_update_skill_progress,
    safe_update_career_goal_progress, safe_update_skill_time_invested,
    validate_skill_level, validate_goal_type, validate_timeline, validate_status,
    safe_get_int, safe_get_float, safe_get_str, safe_get_list
)
from ..api.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/progress", tags=["progress"])

# Link model for career goals
class GoalLink(BaseModel):
    title: str = Field(max_length=200, description="Title of the link")
    url: str = Field(max_length=500, description="URL of the link")
    type: Literal["resource", "course", "article", "tool", "other"] = Field(default="resource", description="Type of link")

# Pydantic models for requests/responses with enhanced validation
class ProgressResponse(BaseModel):
    user_id: int
    total_assessments_completed: int = Field(ge=0, description="Number of assessments completed")
    last_assessment_date: Optional[datetime] = Field(None, description="Date of last assessment")
    career_goals_set: int = Field(ge=0, description="Number of career goals set")
    skills_tracked: int = Field(ge=0, description="Number of skills being tracked")
    current_streak_days: int = Field(ge=0, description="Current consecutive days of activity")
    longest_streak_days: int = Field(ge=0, description="Longest streak of consecutive days")
    profile_completeness: float = Field(ge=0.0, le=1.0, description="Profile completion percentage (0.0-1.0)")
    skill_development_score: float = Field(ge=0.0, le=1.0, description="Overall skill development score")
    career_clarity_score: float = Field(ge=0.0, le=1.0, description="Career clarity score")
    milestones_achieved: List[str] = Field(default_factory=list, description="List of achieved milestones")
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class SkillProgressResponse(BaseModel):
    id: int
    skill_name: str = Field(min_length=1, max_length=100, description="Name of the skill")
    current_level: str = Field(description="Current skill level")
    proficiency_score: float = Field(ge=0.0, le=1.0, description="Proficiency score (0.0-1.0)")
    target_level: str = Field(description="Target skill level")
    target_date: Optional[datetime] = Field(None, description="Target achievement date")
    time_invested_hours: float = Field(ge=0.0, description="Hours invested in learning this skill")
    last_practice_date: Optional[datetime] = Field(None, description="Last practice date")
    progress_history: List[Dict[str, Any]] = Field(default_factory=list, description="Historical progress data")
    
    @validator('current_level', 'target_level')
    def validate_skill_levels(cls, v):
        valid_levels = ['beginner', 'intermediate', 'advanced', 'expert']
        if v not in valid_levels:
            return 'beginner'  # Default to beginner if invalid
        return v
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class CareerGoalResponse(BaseModel):
    id: int
    career_id: int
    goal_type: str = Field(description="Type of career goal")
    target_timeline: str = Field(description="Target timeline")
    priority_level: int = Field(ge=1, le=5, description="Priority level (1=highest, 5=lowest)")
    status: str = Field(description="Goal status")
    progress_percentage: float = Field(ge=0.0, le=100.0, description="Progress percentage (0.0-100.0)")
    required_skills: List[str] = Field(default_factory=list, description="Skills required for this career")
    completed_skills: List[str] = Field(default_factory=list, description="Skills already acquired")
    learning_plan: List[Dict[str, Any]] = Field(default_factory=list, description="Structured learning plan")
    milestones: List[Dict[str, Any]] = Field(default_factory=list, description="Goal milestones")
    links: List[GoalLink] = Field(default_factory=list, description="Helpful links for this goal")
    next_action: Optional[str] = Field(None, max_length=500, description="Next recommended action")
    target_completion_date: Optional[datetime] = Field(None, description="Target completion date")
    created_at: datetime
    
    @validator('goal_type')
    def validate_goal_type(cls, v):
        valid_types = ['primary', 'secondary', 'exploratory']
        return v if v in valid_types else 'primary'
    
    @validator('target_timeline')
    def validate_timeline(cls, v):
        valid_timelines = ['6_months', '1_year', '2_years', '5_years']
        return v if v in valid_timelines else '1_year'
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['active', 'paused', 'completed', 'dropped']
        return v if v in valid_statuses else 'active'
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class AssessmentHistoryResponse(BaseModel):
    id: int
    assessment_type: str = Field(min_length=1, max_length=50, description="Type of assessment")
    scores: Dict[str, Any] = Field(default_factory=dict, description="Assessment scores")
    top_career_recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Top career recommendations")
    skill_gaps_identified: List[Dict[str, Any]] = Field(default_factory=list, description="Identified skill gaps")
    learning_paths_suggested: List[Dict[str, Any]] = Field(default_factory=list, description="Suggested learning paths")
    completion_time_minutes: float = Field(ge=0.0, description="Time taken to complete assessment")
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class SkillProgressRequest(BaseModel):
    skill_name: str = Field(min_length=1, max_length=100, description="Name of the skill")
    current_level: Literal["beginner", "intermediate", "advanced", "expert"] = Field(description="Current skill level")
    proficiency_score: float = Field(ge=0.0, le=1.0, description="Proficiency score (0.0-1.0)")
    target_level: Optional[Literal["beginner", "intermediate", "advanced", "expert"]] = Field(None, description="Target skill level")
    time_invested_hours: float = Field(ge=0.0, default=0.0, description="Hours invested in learning")
    
    @validator('target_level', always=True)
    def validate_target_level(cls, v, values):
        if v is None:
            return values.get('current_level', 'beginner')
        return v

class CareerGoalRequest(BaseModel):
    career_id: int = Field(gt=0, description="ID of the career")
    goal_type: Literal["primary", "secondary", "exploratory"] = Field(default="primary", description="Type of career goal")
    target_timeline: Literal["6_months", "1_year", "2_years", "5_years"] = Field(default="1_year", description="Target timeline")
    priority_level: int = Field(default=1, ge=1, le=5, description="Priority level (1=highest, 5=lowest)")
    links: Optional[List[GoalLink]] = Field(None, description="Helpful links for this goal")

class CareerGoalUpdateRequest(BaseModel):
    progress_percentage: float = Field(ge=0.0, le=100.0, description="Progress percentage (0.0-100.0)")
    completed_skills: Optional[List[str]] = Field(None, description="List of completed skills")
    next_action: Optional[str] = Field(None, max_length=500, description="Next recommended action")
    links: Optional[List[GoalLink]] = Field(None, description="Helpful links for this goal")

# Utility functions for safe type conversion from SQLAlchemy models
def safe_convert_progress(progress) -> ProgressResponse:
    """Safely convert SQLAlchemy UserProgress to ProgressResponse"""
    if not progress:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Progress data not found"
        )
    
    return ProgressResponse(
        user_id=safe_get_int(progress, 'user_id'),
        total_assessments_completed=safe_get_int(progress, 'total_assessments_completed'),
        last_assessment_date=getattr(progress, 'last_assessment_date', None),
        career_goals_set=safe_get_int(progress, 'career_goals_set'),
        skills_tracked=safe_get_int(progress, 'skills_tracked'),
        current_streak_days=safe_get_int(progress, 'current_streak_days'),
        longest_streak_days=safe_get_int(progress, 'longest_streak_days'),
        profile_completeness=safe_get_float(progress, 'profile_completeness'),
        skill_development_score=safe_get_float(progress, 'skill_development_score'),
        career_clarity_score=safe_get_float(progress, 'career_clarity_score'),
        milestones_achieved=safe_get_list(progress, 'milestones_achieved')
    )

def safe_convert_skill(skill) -> SkillProgressResponse:
    """Safely convert SQLAlchemy SkillProgress to SkillProgressResponse"""
    if not skill:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Skill progress not found"
        )
    
    current_level = validate_skill_level(safe_get_str(skill, 'current_level', 'beginner'))
    target_level = validate_skill_level(safe_get_str(skill, 'target_level', current_level))
    
    return SkillProgressResponse(
        id=safe_get_int(skill, 'id'),
        skill_name=safe_get_str(skill, 'skill_name'),
        current_level=current_level,
        proficiency_score=safe_get_float(skill, 'proficiency_score'),
        target_level=target_level,
        target_date=getattr(skill, 'target_date', None),
        time_invested_hours=safe_get_float(skill, 'time_invested_hours'),
        last_practice_date=getattr(skill, 'last_practice_date', None),
        progress_history=safe_get_list(skill, 'progress_history')
    )

def safe_convert_goal(goal) -> CareerGoalResponse:
    """Safely convert SQLAlchemy CareerGoal to CareerGoalResponse"""
    if not goal:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Career goal not found"
        )
    
    goal_type = validate_goal_type(safe_get_str(goal, 'goal_type', 'primary'))
    timeline = validate_timeline(safe_get_str(goal, 'target_timeline', '1_year'))
    status_val = validate_status(safe_get_str(goal, 'status', 'active'))
    
    return CareerGoalResponse(
        id=safe_get_int(goal, 'id'),
        career_id=safe_get_int(goal, 'career_id'),
        goal_type=goal_type,
        target_timeline=timeline,
        priority_level=safe_get_int(goal, 'priority_level', 1),
        status=status_val,
        progress_percentage=safe_get_float(goal, 'progress_percentage'),
        required_skills=safe_get_list(goal, 'required_skills'),
        completed_skills=safe_get_list(goal, 'completed_skills'),
        learning_plan=safe_get_list(goal, 'learning_plan'),
        milestones=safe_get_list(goal, 'milestones'),
        links=[GoalLink(**link) for link in safe_get_list(goal, 'links')],
        next_action=getattr(goal, 'next_action', None),
        target_completion_date=getattr(goal, 'target_completion_date', None),
        created_at=getattr(goal, 'created_at', datetime.utcnow())
    )

def safe_convert_assessment(assessment) -> AssessmentHistoryResponse:
    """Safely convert SQLAlchemy AssessmentHistory to AssessmentHistoryResponse"""
    if not assessment:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Assessment history not found"
        )
    
    # Handle scores which might be stored as dict or list
    scores_data = getattr(assessment, 'scores', {})
    if isinstance(scores_data, list):
        scores_dict = {}
    elif isinstance(scores_data, dict):
        scores_dict = scores_data
    else:
        scores_dict = {}
    
    return AssessmentHistoryResponse(
        id=safe_get_int(assessment, 'id'),
        assessment_type=safe_get_str(assessment, 'assessment_type'),
        scores=scores_dict,
        top_career_recommendations=safe_get_list(assessment, 'top_career_recommendations'),
        skill_gaps_identified=safe_get_list(assessment, 'skill_gaps_identified'),
        learning_paths_suggested=safe_get_list(assessment, 'learning_paths_suggested'),
        completion_time_minutes=safe_get_float(assessment, 'completion_time_minutes'),
        created_at=getattr(assessment, 'created_at', datetime.utcnow())
    )

# Progress tracking endpoints
@router.get("/dashboard", response_model=ProgressResponse)
async def get_progress_dashboard(current_user: User = Depends(get_current_user), 
                               db: Session = Depends(get_db)):
    """Get user's progress dashboard"""
    # Extract user ID safely - current_user is an instance, not a class
    user_id: int = getattr(current_user, 'id')
    progress = safe_create_or_update_user_progress(db, user_id)
    
    return safe_convert_progress(progress)

@router.get("/skills", response_model=List[SkillProgressResponse])
async def get_skill_progress(current_user: User = Depends(get_current_user), 
                           db: Session = Depends(get_db)):
    """Get user's skill progress"""
    user_id: int = getattr(current_user, 'id')
    skills = get_user_skill_progress(db, user_id)
    return [safe_convert_skill(skill) for skill in skills]

@router.post("/skills", response_model=SkillProgressResponse)
async def update_skill_progress(skill_data: SkillProgressRequest,
                              current_user: User = Depends(get_current_user), 
                              db: Session = Depends(get_db)):
    """Update or create skill progress"""
    user_id: int = getattr(current_user, 'id')
    
    # Validate inputs
    validated_current_level = validate_skill_level(skill_data.current_level)
    validated_target_level = validate_skill_level(skill_data.target_level or skill_data.current_level)
    
    skill = safe_create_or_update_skill_progress(
        db, user_id, skill_data.skill_name,
        validated_current_level, skill_data.proficiency_score,
        validated_target_level
    )
    
    # Update time invested if provided
    if skill_data.time_invested_hours > 0:
        skill = safe_update_skill_time_invested(
            db, safe_get_int(skill, 'id'), skill_data.time_invested_hours
        )
    
    return safe_convert_skill(skill)

@router.get("/goals", response_model=List[CareerGoalResponse])
async def get_career_goals(current_user: User = Depends(get_current_user), 
                         db: Session = Depends(get_db)):
    """Get user's career goals"""
    user_id: int = getattr(current_user, 'id')
    goals = get_user_career_goals(db, user_id)
    return [safe_convert_goal(goal) for goal in goals]

@router.post("/goals", response_model=CareerGoalResponse)
async def create_new_career_goal(goal_data: CareerGoalRequest,
                               current_user: User = Depends(get_current_user), 
                               db: Session = Depends(get_db)):
    """Create a new career goal"""
    user_id: int = getattr(current_user, 'id')
    
    goal = create_career_goal(
        db, user_id, goal_data.career_id,
        goal_data.goal_type, goal_data.target_timeline, goal_data.priority_level,
        links=[link.dict() for link in goal_data.links] if goal_data.links else []
    )
    
    return safe_convert_goal(goal)

@router.put("/goals/{goal_id}", response_model=CareerGoalResponse)
async def update_goal_progress(goal_id: int, update_data: CareerGoalUpdateRequest,
                             current_user: User = Depends(get_current_user), 
                             db: Session = Depends(get_db)):
    """Update career goal progress"""
    goal = safe_update_career_goal_progress(
        db, goal_id, update_data.progress_percentage,
        update_data.completed_skills, 
        update_data.next_action,
        [link.dict() for link in update_data.links] if update_data.links else None
    )
    
    if not goal:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Career goal not found"
        )
    
    return safe_convert_goal(goal)

@router.get("/history", response_model=List[AssessmentHistoryResponse])
async def get_assessment_history(current_user: User = Depends(get_current_user), 
                               db: Session = Depends(get_db)):
    """Get user's assessment history"""
    user_id: int = getattr(current_user, 'id')
    history = get_user_assessment_history(db, user_id)
    return [safe_convert_assessment(assessment) for assessment in history]

@router.get("/analytics")
async def get_progress_analytics(current_user: User = Depends(get_current_user), 
                               db: Session = Depends(get_db)):
    """Get detailed progress analytics"""
    user_id: int = getattr(current_user, 'id')
    
    progress = get_user_progress(db, user_id)
    skills = get_user_skill_progress(db, user_id)
    goals = get_user_career_goals(db, user_id)
    history = get_user_assessment_history(db, user_id)
    
    # Calculate analytics - use getattr for safe attribute access
    active_goals = [g for g in goals if getattr(g, 'status', 'active') == "active"]
    completed_goals = [g for g in goals if getattr(g, 'status', 'active') == "completed"]
    
    skill_levels = {}
    for skill in skills:
        level = getattr(skill, 'current_level', 'beginner')
        skill_levels[level] = skill_levels.get(level, 0) + 1
    
    # Assessment frequency
    if history:
        latest_assessment = history[0]
        last_created_at = getattr(latest_assessment, 'created_at', datetime.utcnow())
        days_since_last = (datetime.utcnow() - last_created_at).days
        
        avg_time_between_assessments = None
        if len(history) > 1:
            oldest_assessment = history[-1]
            oldest_created_at = getattr(oldest_assessment, 'created_at', datetime.utcnow())
            total_days = (last_created_at - oldest_created_at).days
            avg_time_between_assessments = total_days / (len(history) - 1) if len(history) > 1 else 0
    else:
        days_since_last = None
        avg_time_between_assessments = None
    
    profile_completeness = getattr(progress, 'profile_completeness', 0.0) if progress else 0.0
    
    return {
        "overview": {
            "total_assessments": len(history),
            "active_goals": len(active_goals),
            "completed_goals": len(completed_goals),
            "skills_tracked": len(skills),
            "profile_completeness": float(profile_completeness or 0.0)
        },
        "skill_distribution": skill_levels,
        "goal_progress": {
            "average_progress": sum(float(getattr(g, 'progress_percentage', 0) or 0) for g in goals) / len(goals) if goals else 0,
            "goals_by_status": {
                "active": len(active_goals),
                "completed": len(completed_goals),
                "paused": len([g for g in goals if getattr(g, 'status', 'active') == "paused"])
            }
        },
        "assessment_patterns": {
            "days_since_last_assessment": days_since_last,
            "average_days_between_assessments": avg_time_between_assessments,
            "assessment_count_by_month": {}  # Could implement month-wise grouping
        }
    }
