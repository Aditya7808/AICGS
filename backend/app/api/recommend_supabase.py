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
                career=rec["career"],
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
