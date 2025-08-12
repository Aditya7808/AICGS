"""
ML API routes for CareerBuddy skill prioritization
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging

from app.ml.skill_prioritizer import get_skill_prioritizer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ml", tags=["machine-learning"])

# Pydantic models for request/response
class UserProfile(BaseModel):
    current_skills: List[str] = []
    experience_years: int = 0
    academic_score: float = 75.0
    learning_capacity: float = 0.5

class SkillPriorityRequest(BaseModel):
    user_profile: UserProfile
    target_career: str
    top_k: int = 10

class MultiCareerAnalysisRequest(BaseModel):
    user_profile: UserProfile
    target_careers: List[str]
    top_k: int = 5

class SkillRecommendation(BaseModel):
    skill: str
    priority_score: float
    category: str
    importance: float
    learning_effort: str

class SkillPriorityResponse(BaseModel):
    user_profile: UserProfile
    target_career: str
    recommendations: List[SkillRecommendation]
    total_recommendations: int

class MultiCareerAnalysisResponse(BaseModel):
    user_profile: UserProfile
    career_analysis: Dict[str, List[SkillRecommendation]]

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        prioritizer = get_skill_prioritizer()
        return {
            "status": "healthy",
            "model_loaded": prioritizer.model is not None,
            "available_skills": len(prioritizer.all_skills) if prioritizer.all_skills else 0,
            "available_careers": len(prioritizer.careers) if prioritizer.careers else 0
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}")

@router.get("/skills/available")
async def get_available_skills():
    """Get all available skills and careers"""
    try:
        prioritizer = get_skill_prioritizer()
        return prioritizer.get_available_skills()
    except Exception as e:
        logger.error(f"Error getting available skills: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/skills/prioritize", response_model=SkillPriorityResponse)
async def prioritize_skills(request: SkillPriorityRequest):
    """Get personalized skill priorities for a user"""
    try:
        prioritizer = get_skill_prioritizer()
        
        # Convert Pydantic model to dict
        user_profile_dict = {
            "current_skills": request.user_profile.current_skills,
            "experience_years": request.user_profile.experience_years,
            "academic_score": request.user_profile.academic_score,
            "learning_capacity": request.user_profile.learning_capacity
        }
        
        # Get recommendations
        recommendations = prioritizer.predict_skill_priorities(
            user_profile_dict,
            request.target_career,
            request.top_k
        )
        
        # Convert to response model
        skill_recommendations = [
            SkillRecommendation(**rec) for rec in recommendations
        ]
        
        return SkillPriorityResponse(
            user_profile=request.user_profile,
            target_career=request.target_career,
            recommendations=skill_recommendations,
            total_recommendations=len(skill_recommendations)
        )
        
    except Exception as e:
        logger.error(f"Error prioritizing skills: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/skills/analyze-gaps", response_model=MultiCareerAnalysisResponse)
async def analyze_skill_gaps(request: MultiCareerAnalysisRequest):
    """Analyze skill gaps for multiple careers"""
    try:
        prioritizer = get_skill_prioritizer()
        
        # Convert Pydantic model to dict
        user_profile_dict = {
            "current_skills": request.user_profile.current_skills,
            "experience_years": request.user_profile.experience_years,
            "academic_score": request.user_profile.academic_score,
            "learning_capacity": request.user_profile.learning_capacity
        }
        
        # Analyze multiple careers
        analysis_results = prioritizer.analyze_multiple_careers(
            user_profile_dict,
            request.target_careers,
            request.top_k
        )
        
        # Convert to response model
        career_analysis = {}
        for career, recommendations in analysis_results.items():
            career_analysis[career] = [
                SkillRecommendation(**rec) for rec in recommendations
            ]
        
        return MultiCareerAnalysisResponse(
            user_profile=request.user_profile,
            career_analysis=career_analysis
        )
        
    except Exception as e:
        logger.error(f"Error analyzing skill gaps: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/skills/compare-careers")
async def compare_career_difficulty(request: MultiCareerAnalysisRequest):
    """Compare the difficulty of transitioning to different careers"""
    try:
        prioritizer = get_skill_prioritizer()
        
        user_profile_dict = {
            "current_skills": request.user_profile.current_skills,
            "experience_years": request.user_profile.experience_years,
            "academic_score": request.user_profile.academic_score,
            "learning_capacity": request.user_profile.learning_capacity
        }
        
        career_difficulty = {}
        
        for career in request.target_careers:
            recommendations = prioritizer.predict_skill_priorities(
                user_profile_dict, career, top_k=20
            )
            
            if recommendations:
                # Calculate transition difficulty
                avg_priority = sum(rec['priority_score'] for rec in recommendations) / len(recommendations)
                high_effort_skills = sum(1 for rec in recommendations if rec['learning_effort'] == 'High')
                
                difficulty_score = (1 - avg_priority) * 0.7 + (high_effort_skills / len(recommendations)) * 0.3
                
                career_difficulty[career] = {
                    "difficulty_score": round(difficulty_score, 3),
                    "difficulty_level": "High" if difficulty_score > 0.6 else "Medium" if difficulty_score > 0.3 else "Low",
                    "skills_needed": len(recommendations),
                    "high_effort_skills": high_effort_skills,
                    "avg_priority": round(avg_priority, 3)
                }
        
        # Sort by difficulty
        sorted_careers = sorted(
            career_difficulty.items(), 
            key=lambda x: x[1]['difficulty_score']
        )
        
        return {
            "user_profile": user_profile_dict,
            "career_difficulty_ranking": sorted_careers,
            "easiest_transition": sorted_careers[0][0] if sorted_careers else None,
            "hardest_transition": sorted_careers[-1][0] if sorted_careers else None
        }
        
    except Exception as e:
        logger.error(f"Error comparing careers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
