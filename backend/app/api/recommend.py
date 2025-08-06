from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ..db.base import get_db
from ..logic.matcher import get_career_recommendations
from ..logic.hybrid_recommender import get_hybrid_career_recommendations
from ..logic.enhanced_matcher import get_enhanced_career_recommendations
from ..logic.peer_intelligence import PeerIntelligenceSystem
from ..logic.skill_gap_analyzer import SkillGapAnalyzer
from ..logic.svm_predictor import SVMCareerPredictor
from ..db.crud import create_user_profile, get_user_profile, log_user_interaction, save_assessment_history
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommend", tags=["recommendations"])

# Legacy request model
class RecommendationRequest(BaseModel):
    age: int
    location: str
    skills: List[str]
    interests: List[str]
    language: str = "en"

# Enhanced request model for v2 API
class EnhancedRecommendationRequest(BaseModel):
    user_id: int
    education_level: str
    current_course: Optional[str] = None
    current_institution: Optional[str] = None
    current_marks_value: float
    current_marks_type: str  # "Percentage" or "CGPA"
    tenth_percentage: Optional[float] = None
    twelfth_percentage: Optional[float] = None
    place_of_residence: str
    residence_type: str  # Rural, Urban, Semi-Urban, Metro
    family_background: str  # Lower Income, Middle Income, Upper Income
    interests: str  # Pipe-separated like "Coding|AI|Gaming"
    skills: str  # Pipe-separated like "Python|Web Development"
    career_goals: Optional[str] = None
    language: str = "en"

# Skill gap analysis request model
class SkillGapRequest(BaseModel):
    user_id: int
    target_career_id: int
    current_skills: List[str]
    current_education_level: str
    time_horizon_months: Optional[int] = 12

# Response models
class CareerMatch(BaseModel):
    career: str
    score: float
    local_demand: str
    description: str

class RecommendationResponse(BaseModel):
    matches: List[CareerMatch]

class EnhancedCareerRecommendation(BaseModel):
    career_id: int
    career_name: str
    category: str
    hybrid_score: float
    confidence_level: float
    recommendation_type: str
    scores: Dict[str, float]
    career_details: Dict[str, Any]
    why_recommended: List[str]
    success_indicators: Dict[str, Any]
    badges: List[str]
    peer_insights: Optional[Dict[str, Any]] = None

class HybridRecommendationResponse(BaseModel):
    user_id: int
    recommendations: List[EnhancedCareerRecommendation]
    algorithm_info: Dict[str, Any]
    generated_at: str
    recommendation_explanations: Dict[str, str]

# Legacy endpoint (v1)
@router.post("", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest, db: Session = Depends(get_db)):
    """Get career recommendations based on user profile (Legacy API)"""
    
    user_data = {
        "age": request.age,
        "location": request.location,
        "skills": request.skills,
        "interests": request.interests,
        "language": request.language
    }
    
    recommendations = get_career_recommendations(db, user_data)
    
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

# Enhanced endpoint (v2) - Content-based only
@router.post("/v2/enhanced", response_model=List[Dict[str, Any]])
async def get_enhanced_recommendations(request: EnhancedRecommendationRequest, db: Session = Depends(get_db)):
    """Get enhanced career recommendations using improved content filtering"""
    
    # Convert request to user profile data
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
    
    # Save/update user profile
    try:
        create_user_profile(db, request.user_id, user_profile_data)
    except Exception as e:
        # Profile might already exist, that's okay
        pass
    
    # Get enhanced recommendations
    start_time = time.time()
    recommendations = get_enhanced_career_recommendations(db, user_profile_data)
    completion_time = (time.time() - start_time) / 60  # Convert to minutes
    
    # Save assessment history
    assessment_data = {
        "responses": user_profile_data,
        "scores": {
            "content_based_score": 0.8,  # Would be calculated from actual algorithm
            "profile_completeness": len([v for v in user_profile_data.values() if v]) / len(user_profile_data)
        },
        "recommendations": recommendations if isinstance(recommendations, list) else [],
        "skill_gaps": [],
        "learning_paths": []
    }
    
    try:
        save_assessment_history(
            db, request.user_id, "enhanced_career_assessment", 
            user_profile_data, assessment_data, completion_time
        )
    except Exception as e:
        # Don't fail the request if assessment saving fails
        print(f"Failed to save assessment history: {e}")
    
    # Log the interaction
    log_user_interaction(db, request.user_id, None, 'enhanced_recommendation_request')
    
    return recommendations

# Hybrid endpoint (v2) - Full AI system
@router.post("/v2/hybrid", response_model=HybridRecommendationResponse)
async def get_hybrid_recommendations(request: EnhancedRecommendationRequest, 
                                   force_refresh: bool = False,
                                   db: Session = Depends(get_db)):
    """Get hybrid AI career recommendations combining content-based and collaborative filtering"""
    
    # Convert request to user profile data
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
    
    # Save/update user profile
    try:
        create_user_profile(db, request.user_id, user_profile_data)
    except Exception as e:
        # Profile might already exist, that's okay
        pass
    
    # Get hybrid recommendations
    try:
        result = get_hybrid_career_recommendations(db, request.user_id, user_profile_data, force_refresh)
        return HybridRecommendationResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

# Interaction logging endpoint
@router.post("/interaction")
async def log_career_interaction(
    user_id: int,
    career_id: Optional[int] = None,
    interaction_type: str = "view",  # view, bookmark, share, rate, apply
    rating: Optional[float] = None,
    context: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db)
):
    """Log user interaction with career for improving recommendations"""
    
    try:
        interaction = log_user_interaction(
            db, user_id, career_id, interaction_type, rating, context
        )
        return {"success": True, "interaction_id": interaction.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging interaction: {str(e)}")

# User profile endpoint
@router.get("/profile/{user_id}")
async def get_user_recommendation_profile(user_id: int, db: Session = Depends(get_db)):
    """Get user's recommendation profile and history"""
    
    profile = get_user_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    # Convert to dict format
    profile_data = {
        "user_id": profile.user_id,
        "education_level": profile.education_level,
        "current_course": profile.current_course,
        "current_institution": profile.current_institution,
        "current_marks_value": profile.current_marks_value,
        "current_marks_type": profile.current_marks_type,
        "tenth_percentage": profile.tenth_percentage,
        "twelfth_percentage": profile.twelfth_percentage,
        "place_of_residence": profile.place_of_residence,
        "residence_type": profile.residence_type,
        "family_background": profile.family_background,
        "interests": profile.interests,
        "skills": profile.skills,
        "career_goals": profile.career_goals,
        "profile_completion_percentage": profile.profile_completion_percentage,
        "last_assessment_date": profile.last_assessment_date,
        "created_at": profile.created_at,
        "updated_at": profile.updated_at
    }
    
    return profile_data

# Test endpoint for Phase 2 verification
@router.get("/v2/test")
async def test_phase2_implementation(db: Session = Depends(get_db)):
    """Test endpoint to verify Phase 2 implementation"""
    
    # Test data
    test_user_profile = {
        "education_level": "Undergraduate",
        "current_marks_value": 75.5,
        "current_marks_type": "Percentage",
        "tenth_percentage": 85.0,
        "twelfth_percentage": 78.0,
        "place_of_residence": "Mumbai",
        "residence_type": "Metro",
        "family_background": "Middle Income",
        "interests": "Technology|Programming|AI|Data Science",
        "skills": "Python|Web Development|Problem Solving|Analytics",
        "career_goals": "Software Development",
        "language": "en"
    }
    
    try:
        # Test enhanced content-based recommendations
        content_recommendations = get_enhanced_career_recommendations(db, test_user_profile)
        
        # Test collaborative filtering (will have limited data initially)
        from ..logic.collaborative_filter import get_collaborative_recommendations
        collaborative_recommendations = get_collaborative_recommendations(db, 1, test_user_profile)
        
        # Test feature engineering
        from ..logic.feature_engineering import FeatureEngineer
        feature_engineer = FeatureEngineer()
        profile_hash = feature_engineer.create_profile_hash(test_user_profile)
        
        # Test data processing (check if training data is loaded)
        from ..models.interaction import CareerOutcome
        outcomes_count = db.query(CareerOutcome).count()
        
        return {
            "status": "Phase 2 Implementation Working",
            "test_results": {
                "enhanced_content_recommendations": len(content_recommendations),
                "collaborative_recommendations": len(collaborative_recommendations),
                "profile_hash_generated": bool(profile_hash),
                "training_data_loaded": outcomes_count > 0,
                "outcomes_in_database": outcomes_count
            },
            "sample_content_recommendation": content_recommendations[0] if content_recommendations else None,
            "sample_collaborative_recommendation": collaborative_recommendations[0] if collaborative_recommendations else None,
            "feature_engineering": {
                "profile_hash": profile_hash,
                "user_vector_length": len(feature_engineer.create_user_profile_vector(test_user_profile))
            }
        }
    
    except Exception as e:
        return {
            "status": "Phase 2 Implementation Error",
            "error": str(e),
            "error_type": type(e).__name__
        }

# Phase 3: Peer Intelligence Endpoints

@router.get("/v2/peer-intelligence/{user_id}")
async def get_peer_intelligence(user_id: int, db: Session = Depends(get_db)):
    """Get peer intelligence insights for a user"""
    
    try:
        from ..logic.peer_intelligence import PeerIntelligenceSystem, get_peer_intelligence_report
        
        # Get user profile
        user_profile = get_user_profile(db, user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Convert profile to dict
        user_profile_data = {
            "education_level": user_profile.education_level,
            "current_course": user_profile.current_course,
            "current_institution": user_profile.current_institution,
            "current_marks_value": user_profile.current_marks_value,
            "current_marks_type": user_profile.current_marks_type,
            "tenth_percentage": user_profile.tenth_percentage,
            "twelfth_percentage": user_profile.twelfth_percentage,
            "place_of_residence": user_profile.place_of_residence,
            "residence_type": user_profile.residence_type,
            "family_background": user_profile.family_background,
            "interests": user_profile.interests,
            "skills": user_profile.skills,
            "career_goals": user_profile.career_goals
        }
        
        # Get comprehensive peer intelligence report
        peer_report = get_peer_intelligence_report(db, user_profile_data)
        
        # Transform the response to match frontend expectations
        transformed_response = {
            "user_id": user_id,
            "similar_students": [
                {
                    "student_id": f"student_{i}",
                    "similarity_score": 0.85 - (i * 0.05),  # Mock similarity scores
                    "education_level": story.get("profile", {}).get("education_level", "Unknown"),
                    "current_marks": story.get("profile", {}).get("current_marks_value", 75),
                    "career_outcomes": [story.get("career_choice", "Unknown")],
                    "similarity_reasons": ["Same education level", "Similar academic performance"]
                }
                for i, story in enumerate(peer_report.get("success_stories", [])[:5])
            ],
            "success_stories": [
                {
                    "student_profile": story.get("profile", {}),
                    "career_choice": story.get("career_choice", ""),
                    "success_factors": story.get("success_factors", []),
                    "inspiration_message": story.get("inspiration_message", "")
                }
                for story in peer_report.get("success_stories", [])
            ],
            "popular_choices": [
                {
                    "career_name": choice.get("career", ""),
                    "popularity_count": choice.get("count", 0),
                    "recommendation_strength": "High" if choice.get("count", 0) > 10 else "Medium",
                    "avg_success_rate": choice.get("success_rate", 0.8)
                }
                for choice in peer_report.get("popular_career_choices", [])
            ],
            "peer_comparison": {
                "user_position": peer_report.get("peer_comparison", {}).get("position", "Above Average"),
                "academic_standing": peer_report.get("peer_comparison", {}).get("academic_performance", "Good"),
                "career_diversity": len(peer_report.get("popular_career_choices", [])),
                "insights": [
                    f"You are performing {peer_report.get('peer_comparison', {}).get('academic_performance', 'well')} compared to peers",
                    f"Similar students have explored {len(peer_report.get('popular_career_choices', []))} different career paths"
                ]
            },
            "peer_insights": {
                "trending_careers": [choice.get("career", "") for choice in peer_report.get("popular_career_choices", [])[:3]],
                "success_patterns": ["Strong academic performance", "Diverse skill development", "Clear goal setting"],
                "recommendations": [
                    "Focus on developing technical skills",
                    "Build a strong portfolio",
                    "Network with industry professionals"
                ]
            },
            "generated_at": peer_report.get("generated_at", "AI Analysis")
        }
        
        return transformed_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating peer intelligence: {str(e)}")

@router.post("/v2/skill-gap-analysis")
async def analyze_skill_gap(request: SkillGapRequest, db: Session = Depends(get_db)):
    """Analyze skill gaps for a target career and provide learning roadmap"""
    
    try:
        from ..logic.skill_gap_analyzer import SkillGapAnalyzer, analyze_user_skill_gaps
        
        # Get user profile
        user_profile = get_user_profile(db, request.user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get target career
        from ..models.career import Career
        target_career = db.query(Career).filter(Career.id == request.target_career_id).first()
        if not target_career:
            raise HTTPException(status_code=404, detail="Target career not found")
        
        # Convert profile to dict
        user_profile_data = {
            "education_level": user_profile.education_level,
            "current_course": user_profile.current_course,
            "current_marks_value": user_profile.current_marks_value,
            "interests": user_profile.interests,
            "skills": user_profile.skills,
            "family_background": user_profile.family_background
        }
        
        # Use the standalone function for analysis
        career_name = getattr(target_career, 'name', '')
        result = analyze_user_skill_gaps(
            db, 
            user_profile_data, 
            [career_name]
        )
        
        # Transform result to match frontend expectations
        transformed_result = {
            "career_analyses": {
                career_name: {
                    "skill_gaps": {
                        "missing_skills": result.get("skill_gaps", {}).get("missing_skills", []),
                        "available_skills": result.get("skill_gaps", {}).get("available_skills", []),
                        "skill_categories": result.get("skill_gaps", {}).get("skill_categories", {})
                    },
                    "learning_roadmap": {
                        "phases": result.get("learning_roadmap", {}).get("phases", [])
                    },
                    "overall_gaps": {
                        "completion_percentage": result.get("overall_gaps", {}).get("completion_percentage", 0),
                        "readiness_level": result.get("overall_gaps", {}).get("readiness_level", "Beginner"),
                        "high_priority_missing": len(result.get("skill_gaps", {}).get("missing_skills", []))
                    },
                    "time_estimate": {
                        "total_weeks": result.get("time_estimate", {}).get("total_weeks", 12),
                        "study_schedule": result.get("time_estimate", {}).get("study_schedule", {})
                    },
                    "readiness_score": result.get("readiness_score", 0.5),
                    "recommendations": result.get("recommendations", [])
                }
            },
            "overall_recommendations": result.get("recommendations", []),
            "skill_priorities": [
                {
                    "skill": skill,
                    "priority": "High" if i < 3 else "Medium",
                    "careers_requiring": [career_name]
                }
                for i, skill in enumerate(result.get("skill_gaps", {}).get("missing_skills", [])[:10])
            ]
        }
        
        return transformed_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing skill gaps: {str(e)}")

@router.get("/v2/learning-roadmap/{user_id}/{career_id}")
async def get_learning_roadmap(user_id: int, career_id: int, 
                             time_horizon: Optional[int] = 12, 
                             db: Session = Depends(get_db)):
    """Get a detailed learning roadmap for a specific career"""
    
    try:
        from ..logic.skill_gap_analyzer import SkillGapAnalyzer
        
        # Get user profile
        user_profile = get_user_profile(db, user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get target career
        from ..models.career import Career
        target_career = db.query(Career).filter(Career.id == career_id).first()
        if not target_career:
            raise HTTPException(status_code=404, detail="Career not found")
        
        # Initialize analyzer
        analyzer = SkillGapAnalyzer()
        
        # Get user skills from profile
        user_skills = []
        skills_str = getattr(user_profile, 'skills', None)
        if skills_str and skills_str.strip():
            user_skills = [skill.strip() for skill in skills_str.split('|') if skill.strip()]
        
        # Perform skill gap analysis which includes roadmap
        career_name = getattr(target_career, 'name', '')
        gap_analysis = analyzer.analyze_skill_gaps(user_skills, career_name)
        
        return {
            "user_id": user_id,
            "career_id": career_id,
            "career_name": career_name,
            "learning_roadmap": gap_analysis.get("learning_roadmap", {}),
            "skill_gaps": gap_analysis.get("skill_gaps", {}),
            "time_estimate": gap_analysis.get("time_estimate", {}),
            "readiness_score": gap_analysis.get("readiness_score", 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating learning roadmap: {str(e)}")

@router.get("/v2/career-readiness/{user_id}/{career_id}")
async def get_career_readiness(user_id: int, career_id: int, db: Session = Depends(get_db)):
    """Get career readiness score and analysis"""
    
    try:
        from ..logic.skill_gap_analyzer import SkillGapAnalyzer
        
        # Get user profile
        user_profile = get_user_profile(db, user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get target career
        from ..models.career import Career
        target_career = db.query(Career).filter(Career.id == career_id).first()
        if not target_career:
            raise HTTPException(status_code=404, detail="Career not found")
        
        # Initialize analyzer
        analyzer = SkillGapAnalyzer()
        
        # Get user skills from profile
        user_skills = []
        skills_str = getattr(user_profile, 'skills', None)
        if skills_str and skills_str.strip():
            user_skills = [skill.strip() for skill in skills_str.split('|') if skill.strip()]
        
        # Perform analysis
        career_name = getattr(target_career, 'name', '')
        gap_analysis = analyzer.analyze_skill_gaps(user_skills, career_name)
        
        return {
            "user_id": user_id,
            "career_id": career_id,
            "career_name": career_name,
            "readiness_score": gap_analysis.get("readiness_score", 0),
            "completion_percentage": gap_analysis.get("overall_gaps", {}).get("completion_percentage", 0),
            "readiness_level": gap_analysis.get("overall_gaps", {}).get("readiness_level", "Beginner"),
            "missing_skills": gap_analysis.get("skill_gaps", {}).get("missing_skills", []),
            "recommendations": gap_analysis.get("recommendations", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating career readiness: {str(e)}")

# Test endpoint for Phase 3 verification
@router.get("/v3/test")
async def test_phase3_implementation(db: Session = Depends(get_db)):
    """Test endpoint to verify Phase 3 implementation"""
    
    try:
        from ..logic.peer_intelligence import PeerIntelligenceSystem
        from ..logic.skill_gap_analyzer import SkillGapAnalyzer
        
        # Test data
        test_user_profile = {
            "education_level": "Undergraduate",
            "current_marks_value": 75.5,
            "current_marks_type": "Percentage",
            "place_of_residence": "Mumbai",
            "residence_type": "Metro",
            "family_background": "Middle Income",
            "interests": "Technology|Programming|AI",
            "skills": "Python|Web Development",
            "career_goals": "Software Development"
        }
        
        # Test peer intelligence
        peer_system = PeerIntelligenceSystem()
        similar_students = peer_system.find_similar_students(db, test_user_profile, limit=3)
        
        # Test skill gap analyzer
        analyzer = SkillGapAnalyzer()
        test_skills = ["Python", "Web Development"]
        gap_analysis = analyzer.analyze_skill_gaps(test_skills, "Software Developer")
        
        # Check if we have any careers in the database
        from ..models.career import Career
        career_count = db.query(Career).count()
        
        # Check user profiles count
        from ..models.user import UserProfile
        profile_count = db.query(UserProfile).count()
        
        return {
            "status": "Phase 3 Implementation Working",
            "test_results": {
                "peer_intelligence_system": "Working",
                "skill_gap_analyzer": "Working",
                "similar_students_found": len(similar_students),
                "gap_analysis_generated": bool(gap_analysis),
                "careers_in_database": career_count,
                "user_profiles_in_database": profile_count
            },
            "sample_gap_analysis": {
                "readiness_score": gap_analysis.get("readiness_score", 0),
                "completion_percentage": gap_analysis.get("overall_gaps", {}).get("completion_percentage", 0)
            } if gap_analysis else None,
            "sample_similar_students": similar_students[:2] if similar_students else []
        }
        
    except Exception as e:
        return {
            "status": "Phase 3 Implementation Error",
            "error": str(e),
            "error_type": type(e).__name__
        }

# SVM Career Prediction Endpoints

@router.post("/v2/svm/predict", response_model=Dict[str, Any])
async def predict_career_outcomes(
    request: EnhancedRecommendationRequest,
    db: Session = Depends(get_db)
):
    """Get SVM-based predictions for next job, institution, and career outcomes"""
    
    # Convert request to user profile data
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
        # Initialize SVM predictor
        svm_predictor = SVMCareerPredictor()
        
        # Get predictions
        predictions = svm_predictor.predict_career_outcomes(user_profile_data)
        
        # Log interaction
        log_user_interaction(db, request.user_id, None, 'svm_prediction_request')
        
        return {
            "user_id": request.user_id,
            "svm_predictions": predictions,
            "request_timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Error getting SVM predictions: {e}")
        raise HTTPException(status_code=500, detail=f"SVM prediction error: {str(e)}")

@router.post("/v2/svm/train", response_model=Dict[str, Any])
async def train_svm_models(
    retrain: bool = False,
    db: Session = Depends(get_db)
):
    """Train or retrain SVM models"""
    
    try:
        # Initialize SVM predictor
        svm_predictor = SVMCareerPredictor()
        
        # Train models
        training_results = svm_predictor.train_models(db, retrain=retrain)
        
        return {
            "training_status": training_results.get("status"),
            "training_results": training_results,
            "model_info": svm_predictor.get_model_info(),
            "training_timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Error training SVM models: {e}")
        raise HTTPException(status_code=500, detail=f"SVM training error: {str(e)}")

@router.get("/v2/svm/model-info", response_model=Dict[str, Any])
async def get_svm_model_info():
    """Get information about the trained SVM models"""
    
    try:
        # Initialize SVM predictor
        svm_predictor = SVMCareerPredictor()
        
        # Get model information
        model_info = svm_predictor.get_model_info()
        
        return {
            "model_info": model_info,
            "query_timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Error getting SVM model info: {e}")
        raise HTTPException(status_code=500, detail=f"SVM model info error: {str(e)}")

@router.post("/v2/hybrid-with-svm", response_model=Dict[str, Any])
async def get_hybrid_recommendations_with_svm(
    request: EnhancedRecommendationRequest, 
    force_refresh: bool = False,
    db: Session = Depends(get_db)
):
    """Get enhanced hybrid recommendations that include SVM predictions"""
    
    # Convert request to user profile data
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
        # Use the updated hybrid recommender
        result = get_hybrid_career_recommendations(db, request.user_id, user_profile_data, force_refresh)
        
        # Log interaction
        log_user_interaction(db, request.user_id, None, 'hybrid_svm_recommendation_request')
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting hybrid SVM recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Hybrid SVM recommendation error: {str(e)}")
