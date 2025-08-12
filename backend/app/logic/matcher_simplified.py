"""
Simplified Career Matcher - Legacy compatibility + Supabase Integration
Provides both legacy SQLAlchemy and new Supabase-based recommendation functions
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
# Legacy import - commented out during migration
# from .enhanced_matcher import get_enhanced_career_recommendations
from ..db.career_crud_supabase import career_crud
import logging

logger = logging.getLogger(__name__)

# Legacy functions for backward compatibility
def calculate_career_match_score(user_skills: List[str], user_interests: List[str], 
                               career_skills: List[str], career_interests: List[str]) -> float:
    """Legacy function - kept for backward compatibility"""
    # Simple similarity calculation
    user_skills_set = set(skill.lower().strip() for skill in user_skills)
    user_interests_set = set(interest.lower().strip() for interest in user_interests)
    career_skills_set = set(skill.lower().strip() for skill in career_skills)
    career_interests_set = set(interest.lower().strip() for interest in career_interests)
    
    # Calculate overlap
    skill_overlap = len(user_skills_set.intersection(career_skills_set))
    interest_overlap = len(user_interests_set.intersection(career_interests_set))
    
    # Calculate scores
    skill_score = skill_overlap / max(len(career_skills_set), 1) if career_skills_set else 0
    interest_score = interest_overlap / max(len(career_interests_set), 1) if career_interests_set else 0
    
    # Weighted average
    final_score = (skill_score * 0.4) + (interest_score * 0.6)
    
    return final_score

def get_career_recommendations(db: Session, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Legacy function - kept for backward compatibility"""
    # Legacy implementation disabled during migration
    # enhanced_recommendations = get_enhanced_career_recommendations(db, user_data)
    
    # Return placeholder for backward compatibility
    return [
        {
            "career_name": "Software Engineer",
            "overall_score": 0.85,
            "category": "Technology", 
            "career_details": {"local_demand": "High"}
        },
        {
            "career_name": "Data Scientist", 
            "overall_score": 0.80,
            "category": "Technology",
            "career_details": {"local_demand": "High"}
        }
    ]

# New Supabase-based functions
async def get_career_recommendations_supabase(user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Get career recommendations using Supabase data
    
    Args:
        user_data: Dictionary containing user information (skills, interests, etc.)
        
    Returns:
        List of career recommendations with scores
    """
    try:
        # Get all careers from Supabase
        careers = await career_crud.get_all_careers()
        
        if not careers:
            logger.warning("No careers found in Supabase")
            return []
        
        recommendations = []
        user_skills = set(skill.lower() for skill in user_data.get("skills", []))
        user_interests = set(interest.lower() for interest in user_data.get("interests", []))
        
        for career in careers:
            score = calculate_career_match_score_supabase(career, user_skills, user_interests)
            
            # Only include careers with a reasonable match score
            if score > 0.1:
                recommendation = {
                    "career": {
                        "id": career.get("id"),
                        "name": career.get("name", "Unknown Career"),
                        "category": career.get("category", "General"),
                        "description": career.get("description_en", "No description available")
                    },
                    "score": round(score, 3),
                    "local_demand": career.get("local_demand", "Medium"),
                    "description": career.get("description_en", "No description available"),
                    "required_skills": career.get("required_skills", []),
                    "min_education": career.get("min_education_level", "Any"),
                    "salary_range": career.get("average_salary_range", "Not specified")
                }
                recommendations.append(recommendation)
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        # Return top 10 recommendations
        return recommendations[:10]
        
    except Exception as e:
        logger.error(f"Error getting career recommendations: {e}")
        return []

def calculate_career_match_score_supabase(career: Dict[str, Any], user_skills: set, user_interests: set) -> float:
    """
    Calculate match score between user and career for Supabase data
    
    Args:
        career: Career data from Supabase
        user_skills: Set of user skills (lowercase)
        user_interests: Set of user interests (lowercase)
        
    Returns:
        Match score between 0.0 and 1.0
    """
    score = 0.0
    total_weight = 0.0
    
    # Skills matching (50% weight)
    skills_weight = 0.5
    career_skills = career.get("required_skills", [])
    if isinstance(career_skills, str):
        # Handle case where skills are stored as comma-separated string
        career_skills = [s.strip().lower() for s in career_skills.split(",")]
    elif isinstance(career_skills, list):
        career_skills = [s.lower() if isinstance(s, str) else str(s).lower() for s in career_skills]
    else:
        career_skills = []
    
    if career_skills:
        career_skills_set = set(career_skills)
        skill_matches = len(user_skills.intersection(career_skills_set))
        skill_score = skill_matches / len(career_skills_set) if career_skills_set else 0
        score += skill_score * skills_weight
        total_weight += skills_weight
    
    # Interests matching (30% weight)
    interests_weight = 0.3
    career_interests = career.get("interests", [])
    if isinstance(career_interests, str):
        career_interests = [i.strip().lower() for i in career_interests.split(",")]
    elif isinstance(career_interests, list):
        career_interests = [i.lower() if isinstance(i, str) else str(i).lower() for i in career_interests]
    else:
        career_interests = []
    
    if career_interests:
        career_interests_set = set(career_interests)
        interest_matches = len(user_interests.intersection(career_interests_set))
        interest_score = interest_matches / len(career_interests_set) if career_interests_set else 0
        score += interest_score * interests_weight
        total_weight += interests_weight
    
    # Category bonus (10% weight)
    category_weight = 0.1
    category = career.get("category", "").lower()
    if any(interest in category for interest in user_interests):
        score += 1.0 * category_weight
    total_weight += category_weight
    
    # Local demand bonus (10% weight)
    demand_weight = 0.1
    local_demand = career.get("local_demand", "Medium").lower()
    demand_score = {"high": 1.0, "medium": 0.7, "low": 0.4}.get(local_demand, 0.5)
    score += demand_score * demand_weight
    total_weight += demand_weight
    
    # Normalize score
    final_score = score / total_weight if total_weight > 0 else 0.0
    
    return min(final_score, 1.0)
