from typing import List, Dict, Any
from sqlalchemy.orm import Session
from .enhanced_matcher import get_enhanced_career_recommendations
import logging

logger = logging.getLogger(__name__)

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
    enhanced_recommendations = get_enhanced_career_recommendations(db, user_data)
    
    # Convert to legacy format
    legacy_recommendations = []
    for rec in enhanced_recommendations:
        legacy_rec = {
            "career": rec['career_name'],
            "score": rec['overall_score'],
            "local_demand": rec['career_details']['local_demand'],
            "description": f"Career in {rec['category']} field"
        }
        legacy_recommendations.append(legacy_rec)
    
    return legacy_recommendations
