from sqlalchemy.orm import Session
from ..models.user import User, UserProfile
from ..models.career import Career
from ..models.interaction import UserInteraction, CareerOutcome, RecommendationCache, AssessmentHistory, UserProgress, SkillProgress, CareerGoal
from ..core.security import get_password_hash
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

def create_user(db: Session, username: str, email: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_careers(db: Session):
    return db.query(Career).all()

def create_sample_careers(db: Session):
    careers = [
        Career(
            name="UI/UX Designer",
            description_en="Creates user-friendly and appealing designs for websites and applications.",
            description_hi="वेबसाइट और एप्लिकेशन के लिए उपयोगकर्ता-अनुकूल और आकर्षक डिज़ाइन बनाता है।",
            required_skills="Design,Creativity,User Research,Prototyping",
            interests="Design,Technology,Art",
            local_demand="High"
        ),
        Career(
            name="Software Developer",
            description_en="Develops software applications and systems using various programming languages.",
            description_hi="विभिन्न प्रोग्रामिंग भाषाओं का उपयोग करके सॉफ्टवेयर एप्लिकेशन और सिस्टम विकसित करता है।",
            required_skills="Coding,Problem Solving,Programming,Logic",
            interests="Technology,Coding,Innovation",
            local_demand="High"
        ),
        Career(
            name="Digital Marketing Specialist",
            description_en="Manages online marketing campaigns and social media presence for businesses.",
            description_hi="व्यवसायों के लिए ऑनलाइन मार्केटिंग अभियान और सोशल मीडिया उपस्थिति का प्रबंधन करता है।",
            required_skills="Marketing,Communication,Analytics,Social Media",
            interests="Marketing,Communication,Business",
            local_demand="Medium"
        ),
        Career(
            name="Data Analyst",
            description_en="Analyzes data to help businesses make informed decisions.",
            description_hi="व्यवसायों को सूचित निर्णय लेने में मदद करने के लिए डेटा का विश्लेषण करता है।",
            required_skills="Analytics,Statistics,Excel,Data Visualization",
            interests="Technology,Analysis,Research",
            local_demand="High"
        )
    ]
    
    # Check if careers already exist
    existing_careers = db.query(Career).first()
    if not existing_careers:
        for career in careers:
            db.add(career)
        db.commit()

# User Profile CRUD operations
def create_user_profile(db: Session, user_id: int, profile_data: Dict[str, Any]) -> UserProfile:
    """Create or update user profile"""
    # Check if profile exists
    existing_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    if existing_profile:
        # Update existing profile
        for key, value in profile_data.items():
            if hasattr(existing_profile, key):
                setattr(existing_profile, key, value)
        profile = existing_profile
    else:
        # Create new profile
        profile = UserProfile(user_id=user_id, **profile_data)
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    return profile

def get_user_profile(db: Session, user_id: int) -> Optional[UserProfile]:
    """Get user profile by user ID"""
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

def calculate_profile_completion(profile: UserProfile) -> float:
    """Calculate profile completion percentage"""
    required_fields = [
        'education_level', 'current_course', 'current_institution',
        'current_marks_value', 'place_of_residence', 'interests'
    ]
    completed_fields = sum(1 for field in required_fields if getattr(profile, field, None))
    return (completed_fields / len(required_fields)) * 100

# User Interaction CRUD operations
def log_user_interaction(db: Session, user_id: int, career_id: Optional[int], 
                        interaction_type: str, rating: Optional[float] = None,
                        context_data: Optional[Dict] = None) -> UserInteraction:
    """Log user interaction for collaborative filtering"""
    interaction = UserInteraction(
        user_id=user_id,
        career_id=career_id,
        interaction_type=interaction_type,
        rating=rating,
        context_data=context_data or {}
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction

def get_user_interactions(db: Session, user_id: int, limit: int = 100) -> List[UserInteraction]:
    """Get user interaction history"""
    return db.query(UserInteraction).filter(
        UserInteraction.user_id == user_id
    ).order_by(UserInteraction.created_at.desc()).limit(limit).all()

def get_similar_users_by_interactions(db: Session, user_id: int, limit: int = 50) -> List[int]:
    """Find users with similar interaction patterns"""
    # Get careers this user has interacted with
    user_career_ids = [row[0] for row in db.query(UserInteraction.career_id).filter(
        UserInteraction.user_id == user_id,
        UserInteraction.career_id.isnot(None)
    ).distinct().all()]
    
    if not user_career_ids:
        return []
    
    # Find other users who interacted with same careers
    similar_users = db.query(UserInteraction.user_id).filter(
        UserInteraction.career_id.in_(user_career_ids),
        UserInteraction.user_id != user_id
    ).distinct().limit(limit).all()
    
    return [user[0] for user in similar_users]

# Career Outcome CRUD operations
def get_career_outcomes_by_profile(db: Session, education_level: str, 
                                 residence_type: str, family_background: str,
                                 min_marks: float = 0) -> List[CareerOutcome]:
    """Get career outcomes for similar profiles"""
    return db.query(CareerOutcome).filter(
        CareerOutcome.education_level == education_level,
        CareerOutcome.residence_type == residence_type,
        CareerOutcome.family_background == family_background,
        CareerOutcome.marks_value >= min_marks
    ).all()

def get_successful_career_paths(db: Session, interests: str) -> List[CareerOutcome]:
    """Get successful career paths for given interests"""
    interest_list = [i.strip().lower() for i in interests.split('|') if i.strip()]
    
    successful_outcomes = db.query(CareerOutcome).filter(
        CareerOutcome.is_successful_outcome == True,
        CareerOutcome.next_path == 'Job'
    ).all()
    
    # Filter by interest overlap
    matching_outcomes = []
    for outcome in successful_outcomes:
        outcome_interests = [i.strip().lower() for i in (outcome.interests or '').split('|')]
        if any(interest in outcome_interests for interest in interest_list):
            matching_outcomes.append(outcome)
    
    return matching_outcomes

# Recommendation Cache CRUD operations
def get_cached_recommendations(db: Session, profile_hash: str) -> Optional[RecommendationCache]:
    """Get cached recommendations if available and not expired"""
    cache = db.query(RecommendationCache).filter(
        RecommendationCache.user_profile_hash == profile_hash,
        RecommendationCache.cache_expiry > datetime.utcnow()
    ).first()
    return cache

def cache_recommendations(db: Session, profile_hash: str, recommendations: Dict[str, Any],
                         scores: Dict[str, float], expiry_hours: int = 24) -> RecommendationCache:
    """Cache recommendation results"""
    expiry_time = datetime.utcnow() + timedelta(hours=expiry_hours)
    
    cache = RecommendationCache(
        user_profile_hash=profile_hash,
        recommendations_json=recommendations,
        content_score=scores.get('content_score', 0.0),
        collaborative_score=scores.get('collaborative_score', 0.0),
        hybrid_score=scores.get('hybrid_score', 0.0),
        confidence_level=scores.get('confidence_level', 0.0),
        cache_expiry=expiry_time
    )
    
    db.add(cache)
    db.commit()
    db.refresh(cache)
    return cache

# Assessment History CRUD operations
def save_assessment_history(db: Session, user_id: int, assessment_type: str,
                           responses: Dict[str, Any], results: Dict[str, Any],
                           completion_time: float) -> AssessmentHistory:
    """Save assessment history"""
    assessment = AssessmentHistory(
        user_id=user_id,
        assessment_type=assessment_type,
        responses=responses,
        scores=results.get('scores', {}),
        top_career_recommendations=results.get('recommendations', []),
        skill_gaps_identified=results.get('skill_gaps', []),
        learning_paths_suggested=results.get('learning_paths', []),
        completion_time_minutes=completion_time
    )
    
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment

def get_user_assessment_history(db: Session, user_id: int) -> List[AssessmentHistory]:
    """Get user's assessment history"""
    return db.query(AssessmentHistory).filter(
        AssessmentHistory.user_id == user_id
    ).order_by(AssessmentHistory.created_at.desc()).all()

# Progress Tracking CRUD operations
def create_or_update_user_progress(db: Session, user_id: int):
    """Create or update user progress tracking"""
    from ..models.interaction import UserProgress, CareerGoal, SkillProgress
    from sqlalchemy import text
    
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
    user_profile = get_user_profile(db, user_id)
    profile_completeness = 0.0
    if user_profile:
        profile_completeness = calculate_profile_completion(user_profile) / 100.0
    
    # Count career goals and skills
    career_goals_count = db.query(CareerGoal).filter(CareerGoal.user_id == user_id).count()
    skills_count = db.query(SkillProgress).filter(SkillProgress.user_id == user_id).count()
    
    # Use proper SQLAlchemy text() for raw SQL
    last_assessment_str = 'NULL' if not latest_assessment else f"'{latest_assessment.created_at}'"
    
    db.execute(
        text(f"""UPDATE user_progress SET 
            total_assessments_completed = {assessment_count},
            career_goals_set = {career_goals_count},
            skills_tracked = {skills_count},
            profile_completeness = {profile_completeness},
            last_assessment_date = {last_assessment_str}
            WHERE user_id = {user_id}""")
    )
    
    db.commit()
    return db.query(UserProgress).filter(UserProgress.user_id == user_id).first()

def get_user_progress(db: Session, user_id: int):
    """Get user progress"""
    from ..models.interaction import UserProgress
    return db.query(UserProgress).filter(UserProgress.user_id == user_id).first()

def create_or_update_skill_progress(db: Session, user_id: int, skill_name: str, 
                                   current_level: str, proficiency_score: float,
                                   target_level: str = None):
    """Create or update skill progress"""
    from ..models.interaction import SkillProgress
    from sqlalchemy import text
    from datetime import datetime
    
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
        db.commit()
        return skill_progress
    else:
        # Update existing skill progress using raw SQL to avoid column assignment issues
        target = target_level or current_level
        
        db.execute(
            text(f"""UPDATE skill_progress SET 
                current_level = '{current_level}',
                proficiency_score = {proficiency_score},
                target_level = '{target}',
                last_practice_date = '{datetime.utcnow()}'
                WHERE user_id = {user_id} AND skill_name = '{skill_name}'""")
        )
        db.commit()
        return db.query(SkillProgress).filter(
            SkillProgress.user_id == user_id,
            SkillProgress.skill_name == skill_name
        ).first()
    """Create or update skill progress"""
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
            progress_history=[]
        )
        db.add(skill_progress)
    else:
        # Update existing skill progress
        old_score = skill_progress.proficiency_score
        skill_progress.current_level = current_level
        skill_progress.proficiency_score = proficiency_score
        if target_level:
            skill_progress.target_level = target_level
        
        # Add to progress history
        if skill_progress.progress_history is None:
            skill_progress.progress_history = []
        
        from datetime import datetime
        skill_progress.progress_history.append({
            "date": datetime.utcnow().isoformat(),
            "score": proficiency_score,
            "level": current_level
        })
        
        skill_progress.last_practice_date = datetime.utcnow()
    
    db.commit()
    db.refresh(skill_progress)
    return skill_progress

def get_user_skill_progress(db: Session, user_id: int) -> List[SkillProgress]:
    """Get all skill progress for a user"""
    from ..models.interaction import SkillProgress
    return db.query(SkillProgress).filter(SkillProgress.user_id == user_id).all()

def create_career_goal(db: Session, user_id: int, career_id: int, goal_type: str = "primary",
                      timeline: str = "1_year", priority: int = 1, links: Optional[list] = None) -> CareerGoal:
    """Create a new career goal"""
    goal = CareerGoal(
        user_id=user_id,
        career_id=career_id,
        goal_type=goal_type,
        target_timeline=timeline,
        priority_level=priority,
        required_skills=[],
        completed_skills=[],
        learning_plan=[],
        milestones=[],
        links=links or []
    )
    
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

def get_user_career_goals(db: Session, user_id: int) -> List[CareerGoal]:
    """Get user's career goals"""
    from ..models.interaction import CareerGoal
    return db.query(CareerGoal).filter(CareerGoal.user_id == user_id).all()

def update_career_goal_progress(db: Session, goal_id: int, progress_percentage: float,
                               completed_skills: Optional[List[str]] = None, next_action: Optional[str] = None, 
                               links: Optional[list] = None):
    """Update career goal progress"""
    from ..models.interaction import CareerGoal
    from sqlalchemy import text
    import json
    
    goal = db.query(CareerGoal).filter(CareerGoal.id == goal_id).first()
    if not goal:
        return None
    
    # Determine status based on progress
    status = "completed" if progress_percentage >= 100.0 else "active" if progress_percentage > 0 else "active"
    
    # Prepare update values
    update_values = f"progress_percentage = {min(progress_percentage, 100.0)}, status = '{status}'"
    
    if completed_skills is not None:
        skills_json = json.dumps(completed_skills).replace("'", "''")  # Escape single quotes
        update_values += f", completed_skills = '{skills_json}'"
    
    if next_action:
        escaped_action = next_action.replace("'", "''")  # Escape single quotes
        update_values += f", next_action = '{escaped_action}'"
    
    if links is not None:
        links_json = json.dumps(links).replace("'", "''")  # Escape single quotes
        update_values += f", links = '{links_json}'"
    
    # Update using raw SQL
    db.execute(
        text(f"UPDATE career_goals SET {update_values} WHERE id = {goal_id}")
    )
    
    db.commit()
    return db.query(CareerGoal).filter(CareerGoal.id == goal_id).first()

def get_career_outcomes(db: Session, limit: Optional[int] = None):
    """Get career outcomes for SVM training"""
    try:
        query = db.query(CareerOutcome)
        if limit:
            query = query.limit(limit)
        return query.all()
    except Exception as e:
        # If CareerOutcome doesn't exist or has issues, return empty list
        return []

def get_career_outcomes_by_profile(db: Session, profile_data: Dict[str, Any]) -> List[CareerOutcome]:
    """Get career outcomes similar to the given profile"""
    try:
        # Simple matching based on education level and location
        education_level = profile_data.get('education_level', '')
        location = profile_data.get('place_of_residence', '')
        
        query = db.query(CareerOutcome)
        
        if education_level:
            query = query.filter(CareerOutcome.education_level.ilike(f'%{education_level}%'))
        
        if location:
            query = query.filter(CareerOutcome.place_of_residence.ilike(f'%{location}%'))
        
        return query.limit(50).all()
    except Exception as e:
        return []
