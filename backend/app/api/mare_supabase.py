"""
FastAPI integration for MARE (Multi-Dimensional Adaptive Recommendation Engine) - Supabase Version
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import logging

from ..logic.mare_engine import MAREEngine, UserProfile, CareerOpportunity
from ..db.mare_crud_supabase import get_mare_crud_supabase
from .auth_supabase import get_current_user
from ..logic.groq_mare_enhancer import groq_enhancer, GroqSuggestion

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/mare", tags=["MARE Recommendations"])

# Initialize MARE engine
mare_engine = MAREEngine()

class MARERecommendationRequest(BaseModel):
    """Enhanced recommendation request for MARE"""
    # Personal dimensions
    age: int = Field(..., ge=13, le=100)
    education_level: str
    location: str
    
    # Cultural dimensions
    cultural_context: str
    family_background: str
    language_preference: str = "en"
    
    # Economic dimensions
    economic_context: str
    financial_constraints: Optional[str] = None
    
    # Geographic dimensions
    geographic_constraints: str
    urban_rural_type: str = Field(default="urban")
    infrastructure_level: str = Field(default="good")
    
    # Social dimensions
    family_expectations: str
    peer_influence_score: float = Field(default=0.5, ge=0.0, le=1.0)
    community_values: Optional[str] = None
    
    # Skills and interests
    skills: List[str]
    interests: List[str]
    skill_weights: Optional[Dict[str, float]] = None
    interest_weights: Optional[Dict[str, float]] = None
    
    # Career preferences
    career_goals: str = ""
    preferred_industries: Optional[List[str]] = None
    work_environment_preference: str = "office"
    salary_expectations: str = ""
    work_life_balance_priority: int = Field(default=5, ge=1, le=10)

class MARERecommendationResponse(BaseModel):
    """MARE recommendation response"""
    career_id: str
    title: str
    industry: str
    overall_score: float
    dimension_scores: Dict[str, float]
    explanation: Dict[str, str]
    confidence_level: str

class GroqEnhancedSuggestion(BaseModel):
    """Groq-enhanced suggestion response"""
    career_title: str
    personalized_insight: str
    actionable_steps: List[str]
    skill_development_plan: List[str]
    cultural_considerations: str
    timeline_suggestion: str
    confidence_score: float

class EnhancedMAREResponse(BaseModel):
    """Enhanced MARE response with Groq suggestions"""
    standard_recommendations: List[MARERecommendationResponse]
    groq_enhanced_suggestions: List[GroqEnhancedSuggestion]
    career_pathway_summary: Optional[str] = None
    enhancement_available: bool

class RecommendationFeedback(BaseModel):
    """User feedback on recommendations"""
    career_opportunity_id: str
    recommendation_score: float
    user_rating: Optional[int] = Field(None, ge=1, le=5)
    user_feedback: Optional[str] = None
    selected: bool = False
    time_spent_viewing: Optional[int] = 0
    context_snapshot: Optional[Dict] = None

@router.post("/recommendations", response_model=List[MARERecommendationResponse])
async def get_mare_recommendations(
    request: MARERecommendationRequest,
    current_user = Depends(get_current_user)
):
    """Generate multi-dimensional adaptive recommendations"""
    
    start_time = datetime.now()
    user_id = current_user["sub"]  # Supabase uses 'sub' for user ID
    
    try:
        crud = get_mare_crud_supabase()
        
        # Create or update user profile
        profile_data = {
            "age": request.age,
            "education_level": request.education_level,
            "location": request.location,
            "cultural_context": request.cultural_context,
            "family_background": request.family_background,
            "language_preference": request.language_preference,
            "economic_context": request.economic_context,
            "financial_constraints": request.financial_constraints,
            "geographic_constraints": request.geographic_constraints,
            "urban_rural_type": request.urban_rural_type,
            "infrastructure_level": request.infrastructure_level,
            "family_expectations": request.family_expectations,
            "peer_influence_score": request.peer_influence_score,
            "community_values": request.community_values
        }
        
        # Save profile components
        profile_id = crud.create_user_profile(user_id, profile_data)
        
        preferences_data = {
            "career_goals": request.career_goals,
            "preferred_industries": request.preferred_industries or [],
            "work_environment_preference": request.work_environment_preference,
            "salary_expectations": request.salary_expectations,
            "work_life_balance_priority": request.work_life_balance_priority
        }
        crud.create_career_preferences(user_id, preferences_data)
        
        skills_data = {
            "skills": request.skills,
            "interests": request.interests,
            "skill_weights": request.skill_weights or {},
            "interest_weights": request.interest_weights or {}
        }
        crud.create_skills_interests(user_id, skills_data)
        
        # Create UserProfile for MARE engine
        user_profile = UserProfile(
            user_id=user_id,
            age=request.age,
            education_level=request.education_level,
            location=request.location,
            cultural_context=request.cultural_context,
            family_background=request.family_background,
            language_preference=request.language_preference,
            economic_context=request.economic_context,
            geographic_constraints=request.geographic_constraints,
            urban_rural_type=request.urban_rural_type,
            infrastructure_level=request.infrastructure_level,
            family_expectations=request.family_expectations,
            financial_constraints=request.financial_constraints,
            peer_influence_score=request.peer_influence_score,
            community_values=request.community_values,
            skills=request.skills,
            interests=request.interests,
            skill_weights=request.skill_weights,
            interest_weights=request.interest_weights,
            career_goals=request.career_goals,
            preferred_industries=request.preferred_industries,
            work_environment_preference=request.work_environment_preference,
            salary_expectations=request.salary_expectations,
            work_life_balance_priority=request.work_life_balance_priority
        )
        
        # Get career opportunities
        opportunities = crud.get_career_opportunities(limit=50)
        
        # Convert to CareerOpportunity objects
        career_opportunities = []
        for opp in opportunities:
            career_opp = CareerOpportunity(
                opportunity_id=hash(str(opp["id"])) % (10**8),  # Convert UUID to int
                title=opp.get("title", ""),
                industry=opp.get("industry", ""),
                required_skills=opp.get("required_skills", []),
                preferred_skills=opp.get("preferred_skills", []),
                locations=[opp.get("location", "")],
                remote_available=opp.get("remote_available", False),
                urban_rural_suitability=opp.get("urban_rural_suitability", "both"),
                salary_range_min=opp.get("salary_range_min", 0),
                salary_range_max=opp.get("salary_range_max", 0),
                education_requirements=[],
                family_friendly_rating=5,
                cultural_adaptability_score=opp.get("cultural_adaptability_score", 0.5),
                traditional_modern_spectrum=opp.get("traditional_modern_spectrum", "balanced"),
                growth_potential_score=opp.get("growth_potential_score", 0.5),
                job_security_score=opp.get("job_security_score", 0.5),
                future_outlook=opp.get("future_outlook", "stable")
            )
            career_opportunities.append(career_opp)
        
        # Generate recommendations using MARE engine
        recommendations = mare_engine.get_recommendations(user_profile, career_opportunities)
        
        # Convert to response format
        response_recommendations = []
        for rec in recommendations:
            response_rec = MARERecommendationResponse(
                career_id=str(rec.opportunity_id),
                title=rec.title,
                industry=rec.industry,
                overall_score=rec.overall_score,
                dimension_scores=rec.dimension_scores,
                explanation=rec.explanation,
                confidence_level=rec.confidence_level
            )
            response_recommendations.append(response_rec)
        
        # Log performance
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Generated {len(response_recommendations)} recommendations in {duration:.2f}s for user {user_id}")
        
        return response_recommendations
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")

@router.post("/recommendations/enhanced", response_model=EnhancedMAREResponse)
async def get_enhanced_mare_recommendations(
    request: MARERecommendationRequest,
    current_user = Depends(get_current_user)
):
    """Generate MARE recommendations enhanced with Groq LLM insights"""
    
    start_time = datetime.now()
    user_id = current_user["sub"]
    
    try:
        # First get standard MARE recommendations
        standard_recommendations = await get_mare_recommendations(request, current_user)
        
        # Prepare user profile for Groq enhancement
        user_profile_dict = {
            "age": request.age,
            "education_level": request.education_level,
            "location": request.location,
            "cultural_context": request.cultural_context,
            "family_background": request.family_background,
            "economic_context": request.economic_context,
            "skills": request.skills,
            "interests": request.interests,
            "career_goals": request.career_goals,
            "family_expectations": request.family_expectations,
            "geographic_constraints": request.geographic_constraints,
            "financial_constraints": request.financial_constraints
        }
        
        # Convert standard recommendations to dict format for Groq
        recommendations_dict = []
        for rec in standard_recommendations:
            rec_dict = {
                "title": rec.title,
                "industry": rec.industry,
                "overall_score": rec.overall_score,
                "explanation": rec.explanation
            }
            recommendations_dict.append(rec_dict)
        
        # Get enhanced suggestions from Groq (limit to top 3)
        groq_suggestions = []
        career_pathway_summary = None
        enhancement_available = groq_enhancer.is_available()
        
        if enhancement_available:
            try:
                groq_raw_suggestions = await groq_enhancer.enhance_mare_recommendations(
                    user_profile_dict, 
                    recommendations_dict,
                    limit=3
                )
                
                # Convert to response format
                for suggestion in groq_raw_suggestions:
                    groq_suggestion = GroqEnhancedSuggestion(
                        career_title=suggestion.career_title,
                        personalized_insight=suggestion.personalized_insight,
                        actionable_steps=suggestion.actionable_steps,
                        skill_development_plan=suggestion.skill_development_plan,
                        cultural_considerations=suggestion.cultural_considerations,
                        timeline_suggestion=suggestion.timeline_suggestion,
                        confidence_score=suggestion.confidence_score
                    )
                    groq_suggestions.append(groq_suggestion)
                
                # Generate career pathway summary
                career_pathway_summary = await groq_enhancer.generate_career_pathway_summary(
                    user_profile_dict, groq_raw_suggestions
                )
                
            except Exception as e:
                logger.error(f"Error getting Groq enhancements: {e}")
                enhancement_available = False
        
        # Create enhanced response
        enhanced_response = EnhancedMAREResponse(
            standard_recommendations=standard_recommendations,
            groq_enhanced_suggestions=groq_suggestions,
            career_pathway_summary=career_pathway_summary,
            enhancement_available=enhancement_available
        )
        
        # Log performance
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Generated enhanced recommendations in {duration:.2f}s for user {user_id}")
        
        return enhanced_response
        
    except Exception as e:
        logger.error(f"Error generating enhanced recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate enhanced recommendations")

@router.post("/profile")
async def create_user_profile(
    profile_request: MARERecommendationRequest,
    current_user = Depends(get_current_user)
):
    """Create or update user profile for MARE system"""
    
    user_id = current_user["sub"]
    
    try:
        crud = get_mare_crud_supabase()
        
        # Create profile data
        profile_data = {
            "age": profile_request.age,
            "education_level": profile_request.education_level,
            "location": profile_request.location,
            "cultural_context": profile_request.cultural_context,
            "family_background": profile_request.family_background,
            "language_preference": profile_request.language_preference,
            "economic_context": profile_request.economic_context,
            "financial_constraints": profile_request.financial_constraints,
            "geographic_constraints": profile_request.geographic_constraints,
            "urban_rural_type": profile_request.urban_rural_type,
            "infrastructure_level": profile_request.infrastructure_level,
            "family_expectations": profile_request.family_expectations,
            "peer_influence_score": profile_request.peer_influence_score,
            "community_values": profile_request.community_values
        }
        
        profile_id = crud.create_user_profile(user_id, profile_data)
        
        # Create career preferences
        preferences_data = {
            "career_goals": profile_request.career_goals,
            "preferred_industries": profile_request.preferred_industries or [],
            "work_environment_preference": profile_request.work_environment_preference,
            "salary_expectations": profile_request.salary_expectations,
            "work_life_balance_priority": profile_request.work_life_balance_priority
        }
        crud.create_career_preferences(user_id, preferences_data)
        
        # Create skills and interests
        skills_data = {
            "skills": profile_request.skills,
            "interests": profile_request.interests,
            "skill_weights": profile_request.skill_weights or {},
            "interest_weights": profile_request.interest_weights or {}
        }
        crud.create_skills_interests(user_id, skills_data)
        
        return {
            "message": "User profile created successfully",
            "profile_id": profile_id,
            "completeness": _calculate_profile_completeness(profile_data),
            "dominant_skills": _get_dominant_skills(profile_request.skills)
        }
        
    except Exception as e:
        logger.error(f"Error creating user profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create user profile")

@router.post("/feedback")
async def submit_recommendation_feedback(
    feedback: RecommendationFeedback,
    current_user = Depends(get_current_user)
):
    """Submit feedback on recommendations"""
    
    user_id = current_user["sub"]
    
    try:
        crud = get_mare_crud_supabase()
        
        feedback_data = {
            "user_id": user_id,
            "career_opportunity_id": feedback.career_opportunity_id,
            "recommendation_score": feedback.recommendation_score,
            "user_rating": feedback.user_rating,
            "user_feedback": feedback.user_feedback,
            "selected": feedback.selected,
            "time_spent_viewing": feedback.time_spent_viewing,
            "context_snapshot": feedback.context_snapshot or {}
        }
        
        feedback_id = crud.save_recommendation_feedback(feedback_data)
        
        return {
            "message": "Feedback submitted successfully",
            "feedback_id": feedback_id
        }
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

@router.get("/analytics")
async def get_recommendation_analytics(
    days: int = 30,
    current_user = Depends(get_current_user)
):
    """Get recommendation analytics"""
    
    try:
        crud = get_mare_crud_supabase()
        analytics = crud.get_recommendation_analytics(days)
        
        return {
            "period_days": days,
            "analytics": analytics,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get analytics")

@router.get("/popular-careers")
async def get_popular_careers(
    limit: int = 10,
    current_user = Depends(get_current_user)
):
    """Get popular career paths"""
    
    try:
        crud = get_mare_crud_supabase()
        popular_careers = crud.get_popular_career_paths(limit)
        
        return {
            "popular_careers": popular_careers,
            "total_count": len(popular_careers)
        }
        
    except Exception as e:
        logger.error(f"Error getting popular careers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get popular careers")

@router.get("/opportunities")
async def search_career_opportunities(
    industry: Optional[str] = None,
    location: Optional[str] = None,
    salary_min: Optional[int] = None,
    salary_max: Optional[int] = None,
    remote_available: Optional[bool] = None,
    urban_rural_type: Optional[str] = None,
    limit: int = 50,
    current_user = Depends(get_current_user)
):
    """Search career opportunities with filters"""
    
    try:
        crud = get_mare_crud_supabase()
        
        filters = {}
        if industry:
            filters["industry"] = industry
        if location:
            filters["location"] = location
        if salary_min:
            filters["salary_min"] = salary_min
        if salary_max:
            filters["salary_max"] = salary_max
        if remote_available is not None:
            filters["remote_available"] = remote_available
        if urban_rural_type:
            filters["urban_rural_type"] = urban_rural_type
        
        opportunities = crud.get_career_opportunities(filters, limit)
        
        return {
            "opportunities": opportunities,
            "total_count": len(opportunities),
            "filters_applied": filters
        }
        
    except Exception as e:
        logger.error(f"Error searching opportunities: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search opportunities")

@router.get("/opportunities/{opportunity_id}")
async def get_career_opportunity(
    opportunity_id: str,
    current_user = Depends(get_current_user)
):
    """Get single career opportunity by ID"""
    
    try:
        crud = get_mare_crud_supabase()
        opportunity = crud.get_career_opportunity(opportunity_id)
        
        if not opportunity:
            raise HTTPException(status_code=404, detail="Career opportunity not found")
        
        return opportunity
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting opportunity: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get opportunity")

@router.get("/insights/{user_id}")
async def get_user_insights(
    user_id: str,
    current_user = Depends(get_current_user)
):
    """Get user insights and recommendations history"""
    
    # Ensure user can only access their own insights
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        crud = get_mare_crud_supabase()
        
        # Get user profile
        profile = crud.get_user_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get feedback history
        feedback_history = crud.get_user_feedback_history(user_id, 20)
        
        return {
            "user_profile": profile,
            "feedback_history": feedback_history,
            "profile_completeness": _calculate_profile_completeness(profile),
            "dominant_skills": _get_dominant_skills(profile.get("skills", [])),
            "insights_generated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user insights: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get user insights")

@router.get("/skills/suggest")
async def suggest_skills(
    q: str = "",
    limit: int = 5,
    current_user = Depends(get_current_user)
):
    """Suggest skills based on query for autocomplete"""
    
    if not q or len(q) < 2:
        return {"suggestions": []}
    
    # Common skills database
    common_skills = [
        "Leadership", "Communication", "Problem Solving", "Team Management",
        "Project Management", "Data Analysis", "Programming", "Software Development",
        "Web Development", "Mobile Development", "Database Management", "Cloud Computing",
        "Machine Learning", "Artificial Intelligence", "Digital Marketing", 
        "Social Media Marketing", "Content Writing", "Graphic Design", "UI/UX Design",
        "Sales", "Customer Service", "Business Analysis", "Financial Analysis",
        "Accounting", "Research", "Teaching", "Public Speaking", "Negotiation",
        "Strategic Planning", "Operations Management", "Supply Chain Management",
        "Quality Assurance", "Testing", "Cybersecurity", "Network Administration",
        "System Administration", "DevOps", "Agile Methodology", "Scrum", 
        "Photography", "Video Editing", "Animation", "3D Modeling", "CAD Design",
        "Engineering", "Architecture", "Construction Management", "Legal Research",
        "Healthcare", "Nursing", "Medical Research", "Psychology", "Counseling",
        "Human Resources", "Recruitment", "Training and Development", "Event Management",
        "Tourism", "Hospitality", "Cooking", "Retail Management", "Inventory Management"
    ]
    
    # Filter skills based on query
    query_lower = q.lower()
    matching_skills = [
        skill for skill in common_skills 
        if query_lower in skill.lower()
    ]
    
    # Sort by relevance (exact matches first, then partial matches)
    def sort_key(skill):
        skill_lower = skill.lower()
        if skill_lower.startswith(query_lower):
            return (0, skill_lower)
        else:
            return (1, skill_lower)
    
    matching_skills.sort(key=sort_key)
    
    return {
        "suggestions": matching_skills[:limit],
        "query": q,
        "total_matches": len(matching_skills)
    }

def _calculate_profile_completeness(profile: Dict) -> float:
    """Calculate profile completeness percentage"""
    required_fields = [
        'age', 'education_level', 'location', 'cultural_context',
        'family_background', 'economic_context', 'family_expectations'
    ]
    
    completed = sum(1 for field in required_fields if profile.get(field))
    return (completed / len(required_fields)) * 100

def _get_dominant_skills(skills: List[str]) -> List[str]:
    """Get dominant skill categories"""
    categories = {
        'technical': ['programming', 'data', 'software', 'development', 'engineering'],
        'creative': ['design', 'art', 'writing', 'creative'],
        'analytical': ['analysis', 'research', 'mathematics', 'statistics'],
        'communication': ['communication', 'presentation', 'language', 'speaking'],
        'leadership': ['management', 'leadership', 'team', 'project']
    }
    
    category_counts = {}
    for category, keywords in categories.items():
        count = sum(1 for skill in skills if any(keyword in skill.lower() for keyword in keywords))
        if count > 0:
            category_counts[category] = count
    
    # Return top 3 categories
    return sorted(category_counts.keys(), key=lambda x: category_counts[x], reverse=True)[:3]
