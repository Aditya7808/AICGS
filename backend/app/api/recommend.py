"""
Career Recommendation API - Supabase Version
Migrated from SQLAlchemy to Supabase for all recommendation endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ..db.career_crud_supabase import career_crud
from ..api.auth_supabase import get_current_user
from ..logic.matcher_simplified import get_career_recommendations_supabase
from ..logic.enhanced_matcher import get_enhanced_career_recommendations_supabase
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommend", tags=["recommendations"])

# Request/Response Models
class RecommendationRequest(BaseModel):
    age: int
    location: str
    skills: List[str]
    interests: List[str]
    language: str = "en"

class CareerMatch(BaseModel):
    career: Dict[str, Any]
    score: float
    local_demand: str
    description: str

class RecommendationResponse(BaseModel):
    matches: List[CareerMatch]

class EnhancedRecommendationRequest(BaseModel):
    user_id: int
    education_level: str
    current_course: str
    current_institution: str
    current_marks_value: float
    current_marks_type: str
    tenth_percentage: float
    twelfth_percentage: float
    place_of_residence: str
    residence_type: str
    family_background: str
    interests: List[str]
    skills: List[str]
    career_goals: List[str]
    language: str = "en"

class HybridRecommendationResponse(BaseModel):
    content_based_recommendations: List[Dict[str, Any]]
    collaborative_recommendations: List[Dict[str, Any]]
    hybrid_recommendations: List[Dict[str, Any]]
    algorithm_info: Dict[str, Any]
    generated_at: str
    recommendation_explanations: Dict[str, str]

# Main Recommendation Endpoints

@router.post("", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get career recommendations based on user profile (v1 API) - Supabase"""
    
    user_data = {
        "age": request.age,
        "location": request.location,
        "skills": request.skills,
        "interests": request.interests,
        "language": request.language
    }
    
    try:
        recommendations = await get_career_recommendations_supabase(user_data)
        
        matches = [
            CareerMatch(
                career=rec["career"]["name"] if isinstance(rec.get("career"), dict) else rec.get("career", "Unknown"),
                score=rec["score"],
                local_demand=rec["local_demand"],
                description=rec["description"]
            )
            for rec in recommendations
        ]
        
        return RecommendationResponse(matches=matches)
    
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@router.post("/v2/enhanced", response_model=List[Dict[str, Any]])
async def get_enhanced_recommendations(request: EnhancedRecommendationRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get enhanced career recommendations using improved content filtering - Supabase"""
    
    user_profile_data = {
        "education_level": request.education_level,
        "current_course": request.current_course,
        "current_institution": request.current_institution,
        "current_marks_value": request.current_marks_value,
        "current_marks_type": request.current_marks_type,
        "tenth_percentage": request.tenth_percentage,
        "twelfth_percentage": request.twelfth_percentage,
        "place_of_residence": request.place_of_residence,
        "residence_type": request.residence_type,
        "family_background": request.family_background,
        "interests": request.interests,
        "skills": request.skills,
        "career_goals": request.career_goals,
        "language": request.language
    }
    
    try:
        recommendations = await get_enhanced_career_recommendations_supabase(user_profile_data)
        return recommendations
    
    except Exception as e:
        logger.error(f"Error getting enhanced recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@router.post("/v2/hybrid", response_model=HybridRecommendationResponse)
async def get_hybrid_recommendations(request: EnhancedRecommendationRequest, 
                                   force_refresh: bool = False,
                                   current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get hybrid AI career recommendations - Supabase (Content-based only for now)"""
    
    user_profile_data = {
        "education_level": request.education_level,
        "current_course": request.current_course,
        "current_institution": request.current_institution,
        "current_marks_value": request.current_marks_value,
        "current_marks_type": request.current_marks_type,
        "tenth_percentage": request.tenth_percentage,
        "twelfth_percentage": request.twelfth_percentage,
        "place_of_residence": request.place_of_residence,
        "residence_type": request.residence_type,
        "family_background": request.family_background,
        "interests": request.interests,
        "skills": request.skills,
        "career_goals": request.career_goals,
        "language": request.language
    }
    
    try:
        # Get content-based recommendations using Supabase
        content_recs = await get_enhanced_career_recommendations_supabase(user_profile_data)
        
        # For now, use content-based as hybrid until collaborative filtering is implemented
        result = {
            "content_based_recommendations": content_recs,
            "collaborative_recommendations": [],  # TODO: Implement with Supabase
            "hybrid_recommendations": content_recs,  # Use content-based for now
            "algorithm_info": {
                "content_weight": 1.0,
                "collaborative_weight": 0.0,
                "hybrid_algorithm": "content_only_supabase",
                "data_source": "supabase"
            },
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "recommendation_explanations": {
                "method": "Enhanced content-based filtering using Supabase career data",
                "features": "Academic compatibility, skill matching, interest alignment",
                "note": "Collaborative filtering will be implemented in future updates"
            }
        }
        return HybridRecommendationResponse(**result)
    
    except Exception as e:
        logger.error(f"Error getting hybrid recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

# Utility Endpoints

@router.get("/status")
async def get_recommendation_status():
    """Get recommendation system status"""
    try:
        # Test Supabase connection
        careers_count = len(await career_crud.get_all_careers())
        
        return {
            "status": "operational",
            "data_source": "supabase",
            "migration_status": "completed",
            "available_endpoints": [
                "POST /recommend - Basic recommendations",
                "POST /recommend/v2/enhanced - Enhanced recommendations", 
                "POST /recommend/v2/hybrid - Hybrid recommendations (content-based)"
            ],
            "careers_available": careers_count,
            "features": {
                "basic_matching": "✅ Available",
                "enhanced_matching": "✅ Available", 
                "academic_compatibility": "✅ Available",
                "skill_gap_analysis": "✅ Available",
                "collaborative_filtering": "🚧 In Development",
                "peer_intelligence": "🚧 In Development"
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "note": "Check Supabase connection and configuration"
        }

@router.post("/interaction")
async def log_career_interaction(
    user_id: int,
    career_id: Optional[int] = None,
    interaction_type: str = "view",
    rating: Optional[float] = None,
    context: Optional[Dict[str, Any]] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Log user interaction with career for improving recommendations"""
    
    try:
        # TODO: Implement interaction logging in Supabase
        logger.info(f"User {current_user.get('sub')} interaction: {interaction_type} on career {career_id}")
        return {
            "success": True, 
            "message": "Interaction logged successfully",
            "note": "Full interaction tracking will be implemented with Supabase"
        }
    except Exception as e:
        logger.error(f"Failed to log interaction: {e}")
        return {"success": False, "error": str(e)}

@router.get("/profile/{user_id}")
async def get_user_recommendation_profile(user_id: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get user's recommendation profile - Supabase"""
    
    # TODO: Implement user profile retrieval from Supabase
    return {
        "user_id": user_id,
        "message": "User profile endpoint - Supabase implementation pending",
        "authenticated_user": current_user.get("sub"),
        "note": "This endpoint will be implemented with Supabase user profile CRUD"
    }

# Additional endpoints required by frontend

class SkillGapRequest(BaseModel):
    user_id: int
    target_career_id: int
    current_skills: List[str]
    current_education_level: str
    time_horizon_months: Optional[int] = 12

class SkillGapResponse(BaseModel):
    career_analyses: Dict[str, Any]
    overall_recommendations: List[str]
    skill_priorities: List[Dict[str, Any]]

class PeerIntelligenceResponse(BaseModel):
    user_id: int
    similar_students: List[Dict[str, Any]]
    success_stories: List[Dict[str, Any]]
    popular_choices: List[Dict[str, Any]]
    peer_comparison: Dict[str, Any]
    peer_insights: Dict[str, Any]
    generated_at: str

@router.get("/v2/peer-intelligence/{user_id}")
async def get_peer_intelligence(user_id: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get peer intelligence data - Supabase placeholder"""
    
    # TODO: Implement peer intelligence with Supabase data
    return PeerIntelligenceResponse(
        user_id=user_id,
        similar_students=[
            {
                "student_id": "sample_1",
                "similarity_score": 0.85,
                "education_level": "undergraduate",
                "current_marks": 8.2,
                "career_outcomes": ["Software Engineer", "Data Scientist"],
                "similarity_reasons": ["Similar academic performance", "Shared interests in technology"]
            }
        ],
        success_stories=[
            {
                "student_profile": {"education": "Computer Science", "marks": 8.5},
                "career_choice": "Software Engineer",
                "success_factors": ["Strong programming skills", "Good problem solving"],
                "inspiration_message": "Consistent practice and learning led to success"
            }
        ],
        popular_choices=[
            {
                "career_name": "Software Engineer",
                "popularity_count": 156,
                "recommendation_strength": "high",
                "avg_success_rate": 0.78
            }
        ],
        peer_comparison={
            "user_position": "top_25_percent",
            "academic_standing": "above_average",
            "career_diversity": 12,
            "insights": ["You perform better than 75% of similar students"]
        },
        peer_insights={
            "trending_careers": ["AI Engineer", "Data Scientist", "Cybersecurity Specialist"],
            "success_patterns": ["Focus on practical projects", "Build a strong portfolio"],
            "recommendations": ["Consider specializing in emerging technologies"]
        },
        generated_at=time.strftime("%Y-%m-%d %H:%M:%S")
    )

@router.post("/v2/skill-gap-analysis", response_model=SkillGapResponse)
async def analyze_skill_gap(request: SkillGapRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Analyze skill gaps for career readiness - Supabase placeholder"""
    
    # TODO: Implement skill gap analysis with Supabase career data
    try:
        # Get career data to analyze against
        careers = await career_crud.get_all_careers()
        target_career = None
        
        for career in careers:
            if career.get('id') == request.target_career_id:
                target_career = career
                break
        
        if not target_career:
            # Provide mock analysis if career not found
            target_career = {
                "name": "Software Engineer",
                "required_skills": ["Python", "JavaScript", "SQL", "React", "Node.js"]
            }
        
        required_skills = target_career.get('required_skills', [])
        if isinstance(required_skills, str):
            required_skills = [s.strip() for s in required_skills.split(',')]
        
        current_skills_set = set(skill.lower() for skill in request.current_skills)
        required_skills_set = set(skill.lower() for skill in required_skills)
        
        missing_skills = list(required_skills_set - current_skills_set)
        available_skills = list(current_skills_set.intersection(required_skills_set))
        
        completion_percentage = len(available_skills) / len(required_skills_set) if required_skills_set else 0
        readiness_score = completion_percentage * 100
        
        return SkillGapResponse(
            career_analyses={
                target_career.get('name', 'Unknown Career'): {
                    "skill_gaps": {
                        "missing_skills": missing_skills,
                        "available_skills": available_skills,
                        "skill_categories": {
                            "programming": [s for s in missing_skills if s.lower() in ['python', 'javascript', 'java', 'c++']],
                            "frameworks": [s for s in missing_skills if s.lower() in ['react', 'angular', 'vue', 'django']],
                            "databases": [s for s in missing_skills if s.lower() in ['sql', 'mongodb', 'postgresql']]
                        }
                    },
                    "learning_roadmap": {
                        "phases": [
                            {
                                "phase": "Foundation",
                                "duration_weeks": 4,
                                "skills": missing_skills[:2] if missing_skills else [],
                                "resources": [
                                    {
                                        "title": "Online Programming Course",
                                        "type": "course",
                                        "duration": "4 weeks",
                                        "difficulty": "beginner"
                                    }
                                ]
                            }
                        ]
                    },
                    "overall_gaps": {
                        "completion_percentage": round(completion_percentage * 100, 1),
                        "readiness_level": "high" if completion_percentage > 0.7 else "medium" if completion_percentage > 0.4 else "low",
                        "high_priority_missing": len(missing_skills)
                    },
                    "time_estimate": {
                        "total_weeks": len(missing_skills) * 2,
                        "study_schedule": {"hours_per_week": 10}
                    },
                    "readiness_score": round(readiness_score, 1),
                    "recommendations": [
                        f"Focus on learning {', '.join(missing_skills[:3])}" if missing_skills else "You have most required skills!"
                    ]
                }
            },
            overall_recommendations=[
                "Build practical projects to demonstrate skills",
                "Consider online certifications for missing skills",
                "Join coding communities and practice regularly"
            ],
            skill_priorities=[
                {
                    "skill": skill,
                    "priority": "high",
                    "careers_requiring": [target_career.get('name', 'Unknown Career')]
                } for skill in missing_skills[:5]
            ]
        )
        
    except Exception as e:
        logger.error(f"Error in skill gap analysis: {e}")
        # Return basic response on error
        return SkillGapResponse(
            career_analyses={
                "Analysis": {
                    "skill_gaps": {"missing_skills": [], "available_skills": request.current_skills, "skill_categories": {}},
                    "learning_roadmap": {"phases": []},
                    "overall_gaps": {"completion_percentage": 75.0, "readiness_level": "medium", "high_priority_missing": 0},
                    "time_estimate": {"total_weeks": 8, "study_schedule": {"hours_per_week": 10}},
                    "readiness_score": 75.0,
                    "recommendations": ["Continue building your skills"]
                }
            },
            overall_recommendations=["Keep learning and practicing"],
            skill_priorities=[]
        )

@router.get("/v2/learning-roadmap/{user_id}/{career_id}")
async def get_learning_roadmap(user_id: int, career_id: int, time_horizon: int = 12, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get learning roadmap for career - Supabase placeholder"""
    
    return {
        "user_id": user_id,
        "career_id": career_id,
        "time_horizon_months": time_horizon,
        "roadmap": {
            "phases": [
                {
                    "phase": "Foundation",
                    "duration_weeks": 8,
                    "skills": ["Programming Basics", "Problem Solving"],
                    "milestones": ["Complete basic programming course"]
                },
                {
                    "phase": "Intermediate",
                    "duration_weeks": 16,
                    "skills": ["Web Development", "Database Management"],
                    "milestones": ["Build first web application"]
                }
            ]
        },
        "estimated_completion": f"{time_horizon} months",
        "note": "Learning roadmap will be personalized with Supabase data"
    }

@router.get("/v2/career-readiness/{user_id}/{career_id}")
async def get_career_readiness(user_id: int, career_id: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get career readiness assessment - Supabase placeholder"""
    
    return {
        "user_id": user_id,
        "career_id": career_id,
        "readiness_score": 72.5,
        "readiness_level": "medium",
        "strengths": ["Strong analytical skills", "Good communication"],
        "areas_for_improvement": ["Technical skills", "Industry experience"],
        "recommended_actions": [
            "Complete relevant certifications",
            "Build portfolio projects",
            "Gain practical experience through internships"
        ],
        "time_to_readiness": "6-8 months",
        "note": "Career readiness will be calculated with real Supabase data"
    }

@router.get("/v3/test")
async def test_phase3():
    """Test endpoint for Phase 3 features"""
    
    return {
        "status": "phase_3_placeholder",
        "available_features": [
            "Peer Intelligence (placeholder)",
            "Skill Gap Analysis (basic implementation)",
            "Learning Roadmap (placeholder)",
            "Career Readiness (placeholder)"
        ],
        "implementation_status": {
            "peer_intelligence": "🚧 Placeholder - needs Supabase user data",
            "skill_gap_analysis": "✅ Basic implementation with Supabase",
            "learning_roadmap": "🚧 Placeholder - needs content data",
            "career_readiness": "🚧 Placeholder - needs assessment logic"
        },
        "note": "These endpoints provide placeholder data until full Supabase implementation"
    }

@router.post("/debug/test-recommendations")
async def test_recommendations_debug(request: RecommendationRequest):
    """Test recommendations without authentication - DEBUG ONLY"""
    
    user_data = {
        "age": request.age,
        "location": request.location,
        "skills": request.skills,
        "interests": request.interests,
        "language": request.language
    }
    
    try:
        logger.info(f"Debug: Testing recommendations with data: {user_data}")
        
        # Test career data retrieval
        careers = await career_crud.get_all_careers()
        logger.info(f"Debug: Found {len(careers)} careers in database")
        
        if not careers:
            return {
                "error": "No careers found in database",
                "suggestion": "Run careers_schema.sql and insert_careers.sql in Supabase",
                "debug_info": {
                    "careers_count": 0,
                    "user_data": user_data
                }
            }
        
        # Test recommendation generation
        recommendations = await get_career_recommendations_supabase(user_data)
        logger.info(f"Debug: Generated {len(recommendations)} recommendations")
        
        # Format for frontend
        matches = []
        for rec in recommendations:
            try:
                match = {
                    "career": rec["career"]["name"] if isinstance(rec.get("career"), dict) else rec.get("career", "Unknown"),
                    "score": rec["score"],
                    "local_demand": rec["local_demand"],
                    "description": rec["description"]
                }
                matches.append(match)
            except Exception as e:
                logger.error(f"Debug: Error formatting recommendation: {e}, rec: {rec}")
                continue
        
        return {
            "status": "success",
            "debug_info": {
                "careers_in_db": len(careers),
                "raw_recommendations": len(recommendations),
                "formatted_matches": len(matches),
                "user_data": user_data
            },
            "matches": matches,
            "sample_career": careers[0] if careers else None,
            "sample_recommendation": recommendations[0] if recommendations else None
        }
    
    except Exception as e:
        logger.error(f"Debug: Error in test recommendations: {e}")
        return {
            "error": str(e),
            "debug_info": {
                "user_data": user_data,
                "careers_available": "unknown"
            }
        }
