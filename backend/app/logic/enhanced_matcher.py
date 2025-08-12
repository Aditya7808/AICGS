from typing import List, Dict, Any, Tuple, Optional
# Legacy SQLAlchemy imports - only used for backward compatibility
# from sqlalchemy.orm import Session
# from ..db.crud import get_careers, get_user_profile, get_career_outcomes_by_profile
# from ..models.user import UserProfile
# from ..models.career import Career
# from ..models.interaction import CareerOutcome
from .feature_engineering import FeatureEngineer
import numpy as np
import logging

logger = logging.getLogger(__name__)

def safe_get_attr(obj, attr: str, default=None):
    """Safely get attribute from SQLAlchemy object"""
    try:
        value = getattr(obj, attr, default)
        return value if value is not None else default
    except:
        return default

def safe_float(value, default: float = 0.0) -> float:
    """Safely convert value to float"""
    try:
        if value is None:
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

class EnhancedContentFilter:
    """Enhanced content-based filtering with academic performance and multi-dimensional similarity"""
    
    def __init__(self):
        self.feature_engineer = FeatureEngineer()
        
    def calculate_academic_compatibility(self, user_profile: Dict[str, Any], career: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Calculate academic compatibility score with explanations"""
        score = 0.0
        explanations = []
        
        # Get user academic data
        user_marks = safe_float(user_profile.get('current_marks_value', 0))
        user_10th = safe_float(user_profile.get('tenth_percentage', 0))
        user_12th = safe_float(user_profile.get('twelfth_percentage', 0))
        
        # Career requirements - safely access attributes
        min_10th = safe_float(safe_get_attr(career, 'min_percentage_10th'))
        min_12th = safe_float(safe_get_attr(career, 'min_percentage_12th'))
        min_cgpa = safe_float(safe_get_attr(career, 'min_cgpa'))
        
        # Check 10th grade requirement
        if min_10th > 0:
            if user_10th >= min_10th:
                score += 0.3
                explanations.append(f"10th grade: {user_10th}% meets requirement ({min_10th}%)")
            else:
                explanations.append(f"10th grade: {user_10th}% below requirement ({min_10th}%)")
        else:
            score += 0.3  # No requirement, give full score
        
        # Check 12th grade requirement
        if min_12th > 0:
            if user_12th >= min_12th:
                score += 0.3
                explanations.append(f"12th grade: {user_12th}% meets requirement ({min_12th}%)")
            else:
                explanations.append(f"12th grade: {user_12th}% below requirement ({min_12th}%)")
        else:
            score += 0.3  # No requirement, give full score
        
        # Check current academic performance
        user_marks_normalized = user_marks
        if user_profile.get('current_marks_type') == 'CGPA':
            user_marks_normalized = user_marks * 10  # Convert CGPA to percentage equivalent
        
        if min_cgpa > 0:
            min_percentage_equiv = min_cgpa * 10
            if user_marks_normalized >= min_percentage_equiv:
                score += 0.4
                explanations.append(f"Current performance: {user_marks_normalized:.1f}% exceeds minimum")
            else:
                score *= 0.7  # Reduce score if below minimum
                explanations.append(f"Current performance: {user_marks_normalized:.1f}% below recommended")
        else:
            score += 0.4  # No specific requirement, give full score
        
        return min(score, 1.0), explanations
    
    def calculate_interest_skill_similarity(self, user_profile: Dict[str, Any], career: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Calculate interest and skill similarity with detailed matching"""
        explanations = []
        
        # Parse user interests and skills
        user_interests = set()
        if user_profile.get('interests'):
            user_interests = set(i.strip().lower() for i in user_profile['interests'].split('|') if i.strip())
        
        user_skills = set()
        if user_profile.get('skills'):
            user_skills = set(s.strip().lower() for s in user_profile['skills'].split('|') if s.strip())
        
        # Parse career requirements - safely access attributes
        career_interests = set()
        career_interests_str = safe_get_attr(career, 'interests', '')
        if career_interests_str:
            career_interests = set(i.strip().lower() for i in str(career_interests_str).split(',') if i.strip())
        
        career_skills = set()
        career_skills_str = safe_get_attr(career, 'required_skills', '')
        if career_skills_str:
            career_skills = set(s.strip().lower() for s in str(career_skills_str).split(',') if s.strip())
        
        # Calculate interest overlap
        interest_overlap = user_interests.intersection(career_interests)
        interest_score = len(interest_overlap) / max(len(career_interests), 1) if career_interests else 0.5
        
        if interest_overlap:
            explanations.append(f"Shared interests: {', '.join(interest_overlap)}")
        
        # Calculate skill overlap
        skill_overlap = user_skills.intersection(career_skills)
        skill_score = len(skill_overlap) / max(len(career_skills), 1) if career_skills else 0.5
        
        if skill_overlap:
            explanations.append(f"Matching skills: {', '.join(skill_overlap)}")
        
        # Combined score with weights
        combined_score = (interest_score * 0.6) + (skill_score * 0.4)
        
        return combined_score, explanations
    
    def calculate_demographic_compatibility(self, user_profile: Dict[str, Any], career: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Calculate demographic and regional compatibility"""
        score = 0.5  # Base score
        explanations = []
        
        # Location compatibility
        user_residence = user_profile.get('residence_type', '').lower()
        remote_feasibility = safe_get_attr(career, 'remote_work_feasibility', 'Medium')
        
        if user_residence in ['rural', 'semi-urban'] and remote_feasibility in ['High', 'Medium']:
            score += 0.3
            explanations.append("Good remote work options for your location")
        elif user_residence in ['urban', 'metro']:
            score += 0.2
            explanations.append("Good opportunities in urban areas")
        
        # Family background consideration
        family_bg = user_profile.get('family_background', '')
        placement_rate = safe_float(safe_get_attr(career, 'placement_success_rate'))
        
        if family_bg == 'Lower Income':
            # Prefer careers with good placement rates and growth
            if placement_rate > 0.7:
                score += 0.2
                explanations.append("High placement success rate")
        elif family_bg == 'Upper Income':
            # Can consider more diverse career options
            score += 0.1
        
        return min(score, 1.0), explanations
    
    def calculate_success_probability(self, user_profile: Dict[str, Any], career: Dict[str, Any],
                                    similar_outcomes: List[Dict[str, Any]]) -> Tuple[float, List[str]]:
        """Calculate success probability based on similar student outcomes"""
        if not similar_outcomes:
            return 0.5, ["Limited data for similar profiles"]
        
        explanations = []
        career_name = safe_get_attr(career, 'name', '').lower()
        
        # Find outcomes for this specific career
        career_specific_outcomes = []
        for outcome in similar_outcomes:
            outcome_role = safe_get_attr(outcome, 'job_role', '')
            if outcome_role and str(outcome_role).lower() == career_name:
                career_specific_outcomes.append(outcome)
        
        if career_specific_outcomes:
            successful_count = 0
            for outcome in career_specific_outcomes:
                if safe_get_attr(outcome, 'is_successful_outcome', False) is True:
                    successful_count += 1
            
            success_rate = successful_count / len(career_specific_outcomes)
            explanations.append(f"Success rate among similar students: {success_rate:.1%}")
            return success_rate, explanations
        
        # If no direct matches, use general success patterns
        user_marks = safe_float(user_profile.get('current_marks_value', 0))
        similar_performance_outcomes = []
        
        for outcome in similar_outcomes:
            outcome_marks = safe_float(safe_get_attr(outcome, 'marks_value', 0))
            if abs(outcome_marks - user_marks) <= 10:  # Within 10 points
                similar_performance_outcomes.append(outcome)
        
        if similar_performance_outcomes:
            successful_count = 0
            for outcome in similar_performance_outcomes:
                if safe_get_attr(outcome, 'is_successful_outcome', False) is True:
                    successful_count += 1
            
            success_rate = successful_count / len(similar_performance_outcomes)
            explanations.append(f"Success rate for similar academic performance: {success_rate:.1%}")
            return success_rate, explanations
        
        # Use career's general success rate
        career_success_rate = safe_float(safe_get_attr(career, 'placement_success_rate', 0.5))
        explanations.append(f"General career success rate: {career_success_rate:.1%}")
        return career_success_rate, explanations

def calculate_enhanced_career_match(user_profile: Dict[str, Any], career: Dict[str, Any],
                                  similar_outcomes: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Enhanced career matching with comprehensive scoring"""
    
    if similar_outcomes is None:
        similar_outcomes = []
    
    content_filter = EnhancedContentFilter()
    
    # Calculate different compatibility dimensions
    academic_score, academic_explanations = content_filter.calculate_academic_compatibility(user_profile, career)
    interest_score, interest_explanations = content_filter.calculate_interest_skill_similarity(user_profile, career)
    demographic_score, demographic_explanations = content_filter.calculate_demographic_compatibility(user_profile, career)
    success_score, success_explanations = content_filter.calculate_success_probability(
        user_profile, career, similar_outcomes
    )
    
    # Weighted final score
    weights = {
        'academic': 0.3,
        'interest_skill': 0.35,
        'demographic': 0.15,
        'success_probability': 0.2
    }
    
    final_score = (
        academic_score * weights['academic'] +
        interest_score * weights['interest_skill'] +
        demographic_score * weights['demographic'] +
        success_score * weights['success_probability']
    )
    
    # Confidence level based on data quality
    confidence = 0.7  # Base confidence
    if similar_outcomes and len(similar_outcomes) > 5:
        confidence += 0.2
    if academic_score > 0.8:
        confidence += 0.1
    
    confidence = min(confidence, 1.0)
    
    return {
        'career_id': safe_get_attr(career, 'id'),
        'career_name': safe_get_attr(career, 'name', 'Unknown Career'),
        'category': safe_get_attr(career, 'category', 'General'),
        'overall_score': round(final_score, 3),
        'confidence_level': round(confidence, 3),
        'dimension_scores': {
            'academic_compatibility': round(academic_score, 3),
            'interest_skill_match': round(interest_score, 3),
            'demographic_fit': round(demographic_score, 3),
            'success_probability': round(success_score, 3)
        },
        'explanations': {
            'academic': academic_explanations,
            'interests_skills': interest_explanations,
            'demographic': demographic_explanations,
            'success_factors': success_explanations
        },
        'career_details': {
            'local_demand': safe_get_attr(career, 'local_demand', 'Medium'),
            'average_salary': safe_get_attr(career, 'average_salary_range', 'Not specified'),
            'growth_prospects': safe_get_attr(career, 'growth_prospects', 'Good'),
            'placement_rate': safe_float(safe_get_attr(career, 'placement_success_rate'))
        }
    }

# Legacy function - disabled during Supabase migration
# def get_enhanced_career_recommendations(db: Session, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
#     """Get enhanced career recommendations using improved content filtering"""
#     
#     # Get all careers
#     careers = get_careers(db)
#     
#     # Get similar student outcomes for context
#     similar_outcomes = []
#     if all(key in user_data for key in ['education_level', 'residence_type', 'family_background']):
#         similar_outcomes = get_career_outcomes_by_profile(
#             db,
#             user_data['education_level'],
#             user_data['residence_type'],
#             user_data['family_background'],
#             safe_float(user_data.get('current_marks_value', 0)) - 10  # Allow 10-point range
#         )
#     
#     recommendations = []
#     
#     # Calculate enhanced match for each career
#     for career in careers:
#         is_active = safe_get_attr(career, 'is_active', True)
#         if is_active:  # Only consider active careers
#             match_result = calculate_enhanced_career_match(user_data, career, similar_outcomes)
#             recommendations.append(match_result)
#     
#     # Sort by overall score and confidence
#     recommendations.sort(key=lambda x: (x['overall_score'], x['confidence_level']), reverse=True)
#     
#     # Return top 10 recommendations
#     return recommendations[:10]

# Supabase-based enhanced recommendations
async def get_enhanced_career_recommendations_supabase(user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get enhanced career recommendations using Supabase data"""
    try:
        from ..db.career_crud_supabase import career_crud
        
        # Get all careers from Supabase
        careers = await career_crud.get_all_careers()
        
        if not careers:
            logger.warning("No careers found in Supabase")
            return []
        
        recommendations = []
        
        # Calculate enhanced match for each career
        for career in careers:
            if career.get('is_active', True):  # Only consider active careers
                match_result = calculate_enhanced_career_match_supabase(user_data, career)
                recommendations.append(match_result)
        
        # Sort by overall score and confidence
        recommendations.sort(key=lambda x: (x['overall_score'], x['confidence_level']), reverse=True)
        
        # Return top 10 recommendations
        return recommendations[:10]
        
    except Exception as e:
        logger.error(f"Error getting enhanced career recommendations from Supabase: {e}")
        return []

def calculate_enhanced_career_match_supabase(user_data: Dict[str, Any], career: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate enhanced match score for Supabase career data"""
    
    # Basic compatibility scores
    skill_score = calculate_skill_compatibility_supabase(user_data, career)
    interest_score = calculate_interest_compatibility_supabase(user_data, career)
    academic_score = calculate_academic_compatibility_supabase(user_data, career)
    
    # Calculate weighted overall score
    overall_score = (
        skill_score * 0.4 +
        interest_score * 0.3 +
        academic_score * 0.3
    )
    
    # Determine confidence level
    confidence_level = determine_confidence_level_supabase(skill_score, interest_score, academic_score)
    
    return {
        'career_id': career.get('id'),
        'career_name': career.get('name', 'Unknown Career'),
        'category': career.get('category', 'General'),
        'overall_score': round(overall_score, 3),
        'confidence_level': confidence_level,
        'skill_match_score': round(skill_score, 3),
        'interest_match_score': round(interest_score, 3),
        'academic_compatibility_score': round(academic_score, 3),
        'career_details': {
            'description': career.get('description_en', 'No description available'),
            'required_skills': career.get('required_skills', []),
            'min_education': career.get('min_education_level', 'Any'),
            'local_demand': career.get('local_demand', 'Medium'),
            'salary_range': career.get('average_salary_range', 'Not specified'),
            'growth_prospects': career.get('growth_prospects', 'Stable')
        },
        'explanations': generate_explanations_supabase(user_data, career, skill_score, interest_score, academic_score)
    }

def calculate_skill_compatibility_supabase(user_data: Dict[str, Any], career: Dict[str, Any]) -> float:
    """Calculate skill compatibility for Supabase data"""
    user_skills = set(skill.lower() for skill in user_data.get('skills', []))
    career_skills = career.get('required_skills', [])
    
    if isinstance(career_skills, str):
        career_skills = [s.strip().lower() for s in career_skills.split(',')]
    elif isinstance(career_skills, list):
        career_skills = [s.lower() if isinstance(s, str) else str(s).lower() for s in career_skills]
    else:
        career_skills = []
    
    if not career_skills:
        return 0.5  # Neutral score if no skills specified
    
    career_skills_set = set(career_skills)
    matches = len(user_skills.intersection(career_skills_set))
    
    return min(matches / len(career_skills_set), 1.0)

def calculate_interest_compatibility_supabase(user_data: Dict[str, Any], career: Dict[str, Any]) -> float:
    """Calculate interest compatibility for Supabase data"""
    user_interests = set(interest.lower() for interest in user_data.get('interests', []))
    career_interests = career.get('interests', [])
    
    if isinstance(career_interests, str):
        career_interests = [i.strip().lower() for i in career_interests.split(',')]
    elif isinstance(career_interests, list):
        career_interests = [i.lower() if isinstance(i, str) else str(i).lower() for i in career_interests]
    else:
        career_interests = []
    
    if not career_interests:
        return 0.5  # Neutral score if no interests specified
    
    career_interests_set = set(career_interests)
    matches = len(user_interests.intersection(career_interests_set))
    
    return min(matches / len(career_interests_set), 1.0)

def calculate_academic_compatibility_supabase(user_data: Dict[str, Any], career: Dict[str, Any]) -> float:
    """Calculate academic compatibility for Supabase data"""
    score = 0.5  # Base score
    
    # Check minimum requirements
    user_10th = safe_float(user_data.get('tenth_percentage', 0))
    user_12th = safe_float(user_data.get('twelfth_percentage', 0))
    user_cgpa = safe_float(user_data.get('current_marks_value', 0))
    
    min_10th = safe_float(career.get('min_percentage_10th', 0))
    min_12th = safe_float(career.get('min_percentage_12th', 0))
    min_cgpa = safe_float(career.get('min_cgpa', 0))
    
    # Check if user meets minimum requirements
    meets_requirements = True
    if min_10th > 0 and user_10th < min_10th:
        meets_requirements = False
    if min_12th > 0 and user_12th < min_12th:
        meets_requirements = False
    if min_cgpa > 0 and user_cgpa < min_cgpa:
        meets_requirements = False
    
    if not meets_requirements:
        return 0.2  # Low score if requirements not met
    
    # Bonus for exceeding requirements
    if user_10th > min_10th + 10:
        score += 0.2
    if user_12th > min_12th + 10:
        score += 0.2
    if user_cgpa > min_cgpa + 1:
        score += 0.1
    
    return min(score, 1.0)

def determine_confidence_level_supabase(skill_score: float, interest_score: float, academic_score: float) -> str:
    """Determine confidence level for Supabase-based recommendations"""
    avg_score = (skill_score + interest_score + academic_score) / 3
    
    if avg_score >= 0.8:
        return "high"
    elif avg_score >= 0.6:
        return "medium"
    else:
        return "low"

def generate_explanations_supabase(user_data: Dict[str, Any], career: Dict[str, Any], 
                                 skill_score: float, interest_score: float, academic_score: float) -> List[str]:
    """Generate explanations for Supabase-based recommendations"""
    explanations = []
    
    if skill_score > 0.7:
        explanations.append("Strong skill match with your profile")
    elif skill_score > 0.4:
        explanations.append("Good skill alignment with some gaps to fill")
    else:
        explanations.append("Significant skill development needed")
    
    if interest_score > 0.7:
        explanations.append("Excellent match with your interests")
    elif interest_score > 0.4:
        explanations.append("Moderate interest alignment")
    else:
        explanations.append("May require developing new interests")
    
    if academic_score > 0.7:
        explanations.append("Strong academic fit")
    elif academic_score > 0.4:
        explanations.append("Meets academic requirements")
    else:
        explanations.append("Academic requirements may be challenging")
    
    # Add career-specific insights
    local_demand = career.get('local_demand', 'Medium').lower()
    if local_demand == 'high':
        explanations.append("High local demand in your area")
    elif local_demand == 'low':
        explanations.append("Limited local opportunities")
    
    return explanations
