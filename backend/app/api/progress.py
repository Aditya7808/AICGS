from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from pydantic import BaseModel, Field, validator, constr
from typing import List, Dict, Any, Optional, Union, Literal
from datetime import datetime, timedelta
import logging
from ..db.progress_crud_supabase import progress_crud
from ..api.auth_supabase import get_current_user

logger = logging.getLogger(__name__)

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

# Utility functions for safe type conversion from Supabase data
def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary"""
    return data.get(key, default) if data else default

def safe_get_int(data: Dict[str, Any], key: str, default: int = 0) -> int:
    """Safely get integer value from dictionary"""
    value = safe_get(data, key, default)
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def safe_get_float(data: Dict[str, Any], key: str, default: float = 0.0) -> float:
    """Safely get float value from dictionary"""
    value = safe_get(data, key, default)
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def safe_get_str(data: Dict[str, Any], key: str, default: str = "") -> str:
    """Safely get string value from dictionary"""
    value = safe_get(data, key, default)
    return str(value) if value is not None else default

def safe_get_list(data: Dict[str, Any], key: str, default: Optional[List] = None) -> List:
    """Safely get list value from dictionary"""
    if default is None:
        default = []
    value = safe_get(data, key, default)
    return value if isinstance(value, list) else default

def validate_skill_level(level: str) -> str:
    """Validate skill level"""
    valid_levels = ['beginner', 'intermediate', 'advanced', 'expert']
    return level if level in valid_levels else 'beginner'

def validate_goal_type(goal_type: str) -> str:
    """Validate goal type"""
    valid_types = ['primary', 'secondary', 'exploratory', 'skill_development', 'certification', 'experience']
    return goal_type if goal_type in valid_types else 'primary'

def validate_timeline(timeline: str) -> str:
    """Validate timeline"""
    valid_timelines = ['3_months', '6_months', '1_year', '2_years', '5_years']
    return timeline if timeline in valid_timelines else '1_year'

def validate_status(status: str) -> str:
    """Validate status"""
    valid_statuses = ['active', 'completed', 'paused', 'cancelled']
    return status if status in valid_statuses else 'active'

def parse_datetime(date_str: Optional[str]) -> Optional[datetime]:
    """Parse datetime string safely"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        return None

def safe_convert_progress(progress: Dict[str, Any]) -> ProgressResponse:
    """Safely convert Supabase progress data to ProgressResponse"""
    if not progress:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Progress data not found"
        )
    
    return ProgressResponse(
        user_id=safe_get_int(progress, 'user_id', hash(progress.get('user_id', '')) % 2147483647),
        total_assessments_completed=safe_get_int(progress, 'total_assessments_completed'),
        last_assessment_date=parse_datetime(safe_get_str(progress, 'last_assessment_date')),
        career_goals_set=safe_get_int(progress, 'career_goals_set'),
        skills_tracked=safe_get_int(progress, 'skills_tracked'),
        current_streak_days=safe_get_int(progress, 'current_streak_days'),
        longest_streak_days=safe_get_int(progress, 'longest_streak_days'),
        profile_completeness=safe_get_float(progress, 'profile_completeness'),
        skill_development_score=safe_get_float(progress, 'skill_development_score'),
        career_clarity_score=safe_get_float(progress, 'career_clarity_score'),
        milestones_achieved=safe_get_list(progress, 'milestones_achieved')
    )

def safe_convert_skill(skill: Dict[str, Any]) -> SkillProgressResponse:
    """Safely convert Supabase skill data to SkillProgressResponse"""
    if not skill:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Skill progress not found"
        )
    
    current_level = validate_skill_level(safe_get_str(skill, 'current_level', 'beginner'))
    target_level = validate_skill_level(safe_get_str(skill, 'target_level', current_level))
    
    return SkillProgressResponse(
        id=safe_get_int(skill, 'id', hash(skill.get('skill_name', '')) % 2147483647),
        skill_name=safe_get_str(skill, 'skill_name'),
        current_level=current_level,
        proficiency_score=safe_get_float(skill, 'proficiency_score'),
        target_level=target_level,
        target_date=parse_datetime(safe_get_str(skill, 'target_date')),
        time_invested_hours=safe_get_float(skill, 'time_invested_hours'),
        last_practice_date=parse_datetime(safe_get_str(skill, 'last_practice_date')),
        progress_history=safe_get_list(skill, 'progress_history')
    )

def safe_convert_goal(goal: Dict[str, Any]) -> CareerGoalResponse:
    """Safely convert Supabase goal data to CareerGoalResponse"""
    if not goal:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Career goal not found"
        )
    
    goal_type = validate_goal_type(safe_get_str(goal, 'goal_type', 'primary'))
    timeline = validate_timeline(safe_get_str(goal, 'target_timeline', '1_year'))
    status_val = validate_status(safe_get_str(goal, 'status', 'active'))
    
    return CareerGoalResponse(
        id=safe_get_int(goal, 'id', hash(str(goal)) % 2147483647),
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
        links=[],  # Will handle link conversion separately if needed
        next_action=safe_get_str(goal, 'next_action'),
        target_completion_date=parse_datetime(safe_get_str(goal, 'target_completion_date')),
        created_at=parse_datetime(safe_get_str(goal, 'created_at')) or datetime.now()
    )

def safe_convert_assessment(assessment: Dict[str, Any]) -> AssessmentHistoryResponse:
    """Safely convert Supabase assessment data to AssessmentHistoryResponse"""
    if not assessment:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Assessment history not found"
        )
    
    return AssessmentHistoryResponse(
        id=safe_get_int(assessment, 'id', hash(str(assessment)) % 2147483647),
        assessment_type=safe_get_str(assessment, 'assessment_type'),
        scores=safe_get(assessment, 'detailed_results', {}),
        top_career_recommendations=safe_get_list(assessment, 'recommendations'),
        skill_gaps_identified=[],  # Can be extracted from detailed_results if needed
        learning_paths_suggested=[],  # Can be extracted from detailed_results if needed
        completion_time_minutes=safe_get_float(assessment, 'duration_minutes', 0.0),
        created_at=parse_datetime(safe_get_str(assessment, 'created_at')) or datetime.now()
    )

# Progress tracking endpoints
@router.get("/dashboard", response_model=ProgressResponse)
async def get_progress_dashboard(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get user's progress dashboard"""
    user_id = current_user.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in authentication token"
        )
    
    try:
        progress_data = await progress_crud.get_or_create_user_progress(str(user_id))
        return safe_convert_progress(progress_data)
    except Exception as e:
        logger.error(f"Error getting progress dashboard for user {user_id}: {e}")
        # Return default progress data if there's an error
        return ProgressResponse(
            user_id=hash(str(user_id)) % 2147483647,
            total_assessments_completed=0,
            last_assessment_date=None,
            career_goals_set=0,
            skills_tracked=0,
            current_streak_days=0,
            longest_streak_days=0,
            profile_completeness=0.1,
            skill_development_score=0.0,
            career_clarity_score=0.0,
            milestones_achieved=[]
        )

@router.get("/skills", response_model=List[SkillProgressResponse])
async def get_skill_progress(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get user's skill progress"""
    user_id = current_user.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in authentication token"
        )
    
    try:
        skills_data = await progress_crud.get_user_skill_progress(str(user_id))
        return [safe_convert_skill(skill) for skill in skills_data]
    except Exception as e:
        logger.error(f"Error getting skill progress for user {user_id}: {e}")
        return []

@router.post("/skills", response_model=SkillProgressResponse)
@router.post("/skills", response_model=SkillProgressResponse)
async def update_skill_progress(skill_data: SkillProgressRequest,
                              current_user: Dict[str, Any] = Depends(get_current_user)):
    """Update or create skill progress"""
    user_id = current_user.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in authentication token"
        )
    
    try:
        # Prepare skill data for Supabase
        supabase_skill_data = {
            "skill_name": skill_data.skill_name,
            "current_level": skill_data.current_level,
            "target_level": skill_data.target_level or skill_data.current_level,
            "proficiency_score": skill_data.proficiency_score,
            "time_invested_hours": skill_data.time_invested_hours,
        }
        
        skill_result = await progress_crud.create_or_update_skill_progress(str(user_id), supabase_skill_data)
        
        # Update activity streak
        await progress_crud.update_activity_streak(str(user_id))
        
        return safe_convert_skill(skill_result)
        
    except Exception as e:
        logger.error(f"Error updating skill progress for user {user_id}: {e}")
        # Return a basic response if there's an error
        return SkillProgressResponse(
            id=1,
            skill_name=skill_data.skill_name,
            current_level=skill_data.current_level,
            target_level=skill_data.target_level or skill_data.current_level,
            proficiency_score=skill_data.proficiency_score,
            time_invested_hours=skill_data.time_invested_hours,
            target_date=None,
            last_practice_date=None,
            progress_history=[]
        )

@router.get("/goals", response_model=List[CareerGoalResponse])
async def get_career_goals(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get user's career goals"""
    user_id = current_user.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in authentication token"
        )
    
    try:
        goals_data = await progress_crud.get_user_career_goals(str(user_id))
        return [safe_convert_goal(goal) for goal in goals_data]
    except Exception as e:
        logger.error(f"Error getting career goals for user {user_id}: {e}")
        return []

@router.post("/goals", response_model=CareerGoalResponse)
async def create_new_career_goal(goal_data: CareerGoalRequest,
                               current_user: Dict[str, Any] = Depends(get_current_user)):
    """Create a new career goal"""
    user_id = current_user.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in authentication token"
        )
    
    try:
        # Prepare goal data for Supabase
        supabase_goal_data = {
            "career_id": goal_data.career_id if hasattr(goal_data, 'career_id') else 1,
            "goal_type": goal_data.goal_type,
            "target_timeline": goal_data.target_timeline,
            "priority_level": goal_data.priority_level,
            "status": "active",
            "progress_percentage": 0.0,
            "required_skills": [],
            "completed_skills": [],
            "learning_plan": [],
            "milestones": [],
            "links": [link.dict() for link in goal_data.links] if hasattr(goal_data, 'links') and goal_data.links else [],
            "next_action": ""
        }
        
        goal_result = await progress_crud.create_career_goal(str(user_id), supabase_goal_data)
        
        # Update activity streak
        await progress_crud.update_activity_streak(str(user_id))
        
        return safe_convert_goal(goal_result)
        
    except Exception as e:
        logger.error(f"Error creating career goal for user {user_id}: {e}")
        # Return a basic response if there's an error
        return CareerGoalResponse(
            id=1,
            career_id=1,
            goal_type=goal_data.goal_type,
            target_timeline=goal_data.target_timeline,
            priority_level=goal_data.priority_level,
            progress_percentage=0.0,
            status="active",
            created_at=datetime.now(),
            target_completion_date=None,
            required_skills=[],
            completed_skills=[],
            learning_plan=[],
            milestones=[],
            next_action="",
            links=[]
        )

@router.put("/goals/{goal_id}", response_model=CareerGoalResponse)
async def update_goal_progress(goal_id: str, update_data: CareerGoalUpdateRequest,
                             current_user: Dict[str, Any] = Depends(get_current_user)):
    """Update career goal progress"""
    user_id = current_user.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in authentication token"
        )
    
    try:
        # Prepare update data for Supabase
        updates = {}
        
        if hasattr(update_data, 'progress_percentage') and update_data.progress_percentage is not None:
            updates["progress_percentage"] = update_data.progress_percentage
        
        if hasattr(update_data, 'completed_skills') and update_data.completed_skills is not None:
            updates["completed_skills"] = update_data.completed_skills
        
        if hasattr(update_data, 'next_action') and update_data.next_action is not None:
            updates["next_action"] = update_data.next_action
        
        if hasattr(update_data, 'links') and update_data.links is not None:
            updates["links"] = [link.dict() for link in update_data.links]
        
        goal_result = await progress_crud.update_career_goal(str(user_id), goal_id, updates)
        
        if not goal_result:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Career goal not found"
            )
        
        # Update activity streak
        await progress_crud.update_activity_streak(str(user_id))
        
        return safe_convert_goal(goal_result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating career goal {goal_id} for user {user_id}: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update career goal"
        )

@router.get("/history", response_model=List[AssessmentHistoryResponse])
async def get_assessment_history(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get user's assessment history"""
    user_id = current_user.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in authentication token"
        )
    
    try:
        history_data = await progress_crud.get_user_assessment_history(str(user_id))
        return [safe_convert_assessment(assessment) for assessment in history_data]
    except Exception as e:
        logger.error(f"Error getting assessment history for user {user_id}: {e}")
        return []

@router.get("/analytics")
async def get_progress_analytics(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get detailed progress analytics"""
    user_id = current_user.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in authentication token"
        )
    
    try:
        analytics_data = await progress_crud.get_progress_analytics(str(user_id))
        return analytics_data
    except Exception as e:
        logger.error(f"Error getting progress analytics for user {user_id}: {e}")
        # Return basic analytics if there's an error
        return {
            "overview": {
                "total_assessments": 0,
                "active_goals": 0,
                "completed_goals": 0,
                "skills_tracked": 0,
                "profile_completeness": 0.1,
                "current_streak": 0,
                "longest_streak": 0
            },
            "skill_distribution": {},
            "goal_progress": {
                "average_progress": 0,
                "goals_by_status": {
                    "active": 0,
                    "completed": 0,
                    "paused": 0,
                    "cancelled": 0
                }
            },
            "assessment_patterns": {
                "days_since_last_assessment": None,
                "recent_assessments": 0,
                "assessment_frequency": "irregular"
            },
            "progress_trends": [],
            "upcoming_milestones": [],
            "recommendations": []
        }
