"""
MARE Configuration
Configuration settings for Multi-Dimensional Adaptive Recommendation Engine
"""

from typing import Dict, List, Any
import os
from dataclasses import dataclass

@dataclass
class MAREConfig:
    """Configuration for MARE system"""
    
    # Feature weights for different dimensions
    DIMENSION_WEIGHTS = {
        'personal': 0.25,      # Age, education, location
        'cultural': 0.20,      # Cultural context, family, language
        'economic': 0.20,      # Economic context, financial constraints
        'geographic': 0.15,    # Geographic constraints, infrastructure
        'social': 0.20         # Family expectations, peer influence, community
    }
    
    # Skill categories mapping for better matching
    SKILL_CATEGORIES = {
        'technical': [
            'Programming', 'Data Analysis', 'Machine Learning', 'Web Development',
            'Software Engineering', 'Database Management', 'System Administration',
            'Cybersecurity', 'Mobile Development', 'DevOps', 'Cloud Computing',
            'Artificial Intelligence', 'Blockchain', 'IoT', 'Network Engineering'
        ],
        'creative': [
            'Design', 'Writing', 'Art', 'Photography', 'Video Editing',
            'Content Creation', 'Graphic Design', 'UI/UX Design', 'Creative Writing',
            'Animation', 'Music Production', 'Fashion Design', 'Interior Design'
        ],
        'analytical': [
            'Research', 'Analysis', 'Problem Solving', 'Mathematics', 
            'Statistics', 'Data Science', 'Business Analysis', 'Financial Analysis',
            'Market Research', 'Operations Research', 'Quality Analysis',
            'Risk Assessment', 'Strategic Analysis'
        ],
        'communication': [
            'Public Speaking', 'Writing', 'Languages', 'Teaching',
            'Presentation', 'Negotiation', 'Customer Service', 'Sales',
            'Marketing', 'Public Relations', 'Translation', 'Training',
            'Counseling', 'Journalism'
        ],
        'leadership': [
            'Management', 'Team Leadership', 'Project Management', 'Mentoring',
            'Strategic Planning', 'Decision Making', 'Conflict Resolution',
            'Change Management', 'Business Development', 'Entrepreneurship',
            'Coaching', 'Supervision'
        ]
    }
    
    # Cultural context mappings (higher score = more traditional)
    CULTURAL_CONTEXTS = {
        'traditional': 0.9,
        'conservative': 0.7,
        'balanced': 0.5,
        'modern': 0.3,
        'progressive': 0.1
    }
    
    # Economic context mappings (higher score = higher income bracket)
    ECONOMIC_CONTEXTS = {
        'low_income': 0.2,
        'lower_middle': 0.35,
        'middle_income': 0.5,
        'upper_middle': 0.7,
        'high_income': 0.9
    }
    
    # Infrastructure level mappings
    INFRASTRUCTURE_LEVELS = {
        'poor': 0.2,
        'fair': 0.4,
        'good': 0.6,
        'very_good': 0.8,
        'excellent': 1.0
    }
    
    # Urban/Rural type preferences
    URBAN_RURAL_COMPATIBILITY = {
        'urban': {'urban': 1.0, 'semi_urban': 0.7, 'rural': 0.3},
        'semi_urban': {'urban': 0.8, 'semi_urban': 1.0, 'rural': 0.8},
        'rural': {'urban': 0.3, 'semi_urban': 0.7, 'rural': 1.0}
    }
    
    # Education level hierarchy
    EDUCATION_LEVELS = {
        'below_10th': 1,
        '10th_pass': 2,
        '12th_pass': 3,
        'diploma': 4,
        'bachelors': 5,
        'masters': 6,
        'phd': 7,
        'professional': 5.5  # Professional courses like CA, CS, etc.
    }
    
    # Language preference weights (for Indian context)
    LANGUAGE_WEIGHTS = {
        'en': 1.0,    # English
        'hi': 0.9,    # Hindi
        'bn': 0.8,    # Bengali
        'te': 0.8,    # Telugu
        'mr': 0.8,    # Marathi
        'ta': 0.8,    # Tamil
        'gu': 0.8,    # Gujarati
        'ur': 0.8,    # Urdu
        'kn': 0.8,    # Kannada
        'or': 0.8,    # Odia
        'ml': 0.8,    # Malayalam
        'pa': 0.8,    # Punjabi
        'as': 0.7,    # Assamese
        'other': 0.6  # Other regional languages
    }
    
    # Family background impact on career choices
    FAMILY_BACKGROUND_WEIGHTS = {
        'business': {'entrepreneurship': 0.9, 'sales': 0.8, 'management': 0.8},
        'government': {'public_service': 0.9, 'administration': 0.8, 'teaching': 0.7},
        'farming': {'agriculture': 0.9, 'research': 0.7, 'environmental': 0.8},
        'technical': {'engineering': 0.9, 'technology': 0.8, 'research': 0.8},
        'education': {'teaching': 0.9, 'research': 0.8, 'training': 0.8},
        'healthcare': {'medical': 0.9, 'nursing': 0.8, 'research': 0.7},
        'middle_class': {'stable_jobs': 0.8, 'government': 0.7, 'corporate': 0.7},
        'other': {'general': 0.5}
    }
    
    # Learning and adaptation parameters
    LEARNING_RATE = 0.01
    FEEDBACK_WEIGHT = 0.3
    COLD_START_THRESHOLD = 5  # Minimum feedback required for personalized recommendations
    EXPLORATION_RATE = 0.1  # For exploration vs exploitation in recommendations
    
    # Recommendation parameters
    MAX_RECOMMENDATIONS = 10
    MIN_CONFIDENCE_SCORE = 0.6
    DIVERSITY_WEIGHT = 0.2  # Weight for recommendation diversity
    
    # Similarity thresholds
    SIMILARITY_THRESHOLD = 0.7
    HIGH_SIMILARITY_THRESHOLD = 0.85
    
    # Time-based weights (how much recent feedback matters more)
    TIME_DECAY_FACTOR = 0.95  # Per day
    MAX_FEEDBACK_AGE_DAYS = 365
    
    # Geographic radius for local opportunities (in km)
    LOCAL_RADIUS_KM = 50
    REGIONAL_RADIUS_KM = 200
    
    # Industry-specific adjustments
    INDUSTRY_CULTURAL_FIT = {
        'Technology': {'modern': 0.9, 'progressive': 0.8, 'balanced': 0.6},
        'Healthcare': {'traditional': 0.8, 'balanced': 0.9, 'modern': 0.7},
        'Education': {'traditional': 0.9, 'balanced': 0.8, 'modern': 0.6},
        'Finance': {'conservative': 0.8, 'balanced': 0.9, 'modern': 0.7},
        'Agriculture': {'traditional': 0.9, 'conservative': 0.8, 'balanced': 0.6},
        'Arts': {'progressive': 0.9, 'modern': 0.8, 'balanced': 0.7},
        'Government': {'conservative': 0.9, 'traditional': 0.8, 'balanced': 0.7}
    }
    
    # Career path difficulty levels (affects recommendation confidence)
    CAREER_DIFFICULTY_LEVELS = {
        'entry_level': 0.9,
        'mid_level': 0.7,
        'senior_level': 0.5,
        'expert_level': 0.3
    }
    
    # Feature importance for different user types
    USER_TYPE_WEIGHTS = {
        'fresh_graduate': {
            'skills_match': 0.3,
            'growth_potential': 0.3,
            'entry_barrier': 0.2,
            'cultural_fit': 0.2
        },
        'experienced': {
            'skills_match': 0.4,
            'salary_match': 0.2,
            'growth_potential': 0.2,
            'cultural_fit': 0.2
        },
        'career_changer': {
            'transferable_skills': 0.3,
            'retraining_feasibility': 0.3,
            'cultural_fit': 0.2,
            'market_demand': 0.2
        }
    }

class MAREEnvironmentConfig:
    """Environment-specific configuration"""
    
    def __init__(self):
        self.env = os.getenv('ENVIRONMENT', 'development')
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        # Database configuration
        self.database_url = os.getenv('DATABASE_URL', 'postgresql://localhost/careerbuddy')
        
        # ML Model configurations
        self.model_update_frequency = int(os.getenv('MODEL_UPDATE_FREQUENCY', '7'))  # days
        self.model_retrain_threshold = float(os.getenv('MODEL_RETRAIN_THRESHOLD', '0.1'))  # accuracy drop
        
        # Cache configuration
        self.cache_ttl = int(os.getenv('CACHE_TTL', '3600'))  # seconds
        self.enable_caching = os.getenv('ENABLE_CACHING', 'True').lower() == 'true'
        
        # External API configurations
        self.job_market_api_url = os.getenv('JOB_MARKET_API_URL', '')
        self.salary_data_api_url = os.getenv('SALARY_DATA_API_URL', '')
        
        # Logging configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.enable_request_logging = os.getenv('ENABLE_REQUEST_LOGGING', 'True').lower() == 'true'
        
        # Performance thresholds
        self.max_response_time_ms = int(os.getenv('MAX_RESPONSE_TIME_MS', '2000'))
        self.max_concurrent_requests = int(os.getenv('MAX_CONCURRENT_REQUESTS', '100'))

# Global configuration instances
mare_config = MAREConfig()
env_config = MAREEnvironmentConfig()

# Utility functions
def get_cultural_score(cultural_context: str) -> float:
    """Get cultural context score"""
    return mare_config.CULTURAL_CONTEXTS.get(cultural_context.lower(), 0.5)

def get_economic_score(economic_context: str) -> float:
    """Get economic context score"""
    return mare_config.ECONOMIC_CONTEXTS.get(economic_context.lower(), 0.5)

def get_skill_category_scores(skills: List[str]) -> Dict[str, float]:
    """Calculate skill category scores for a list of skills"""
    scores = {}
    
    for category, category_skills in mare_config.SKILL_CATEGORIES.items():
        matches = 0
        for skill in skills:
            if any(cat_skill.lower() in skill.lower() for cat_skill in category_skills):
                matches += 1
        
        scores[category] = min(matches / len(category_skills), 1.0) if category_skills else 0.0
    
    return scores

def get_urban_rural_compatibility(user_type: str, job_type: str) -> float:
    """Get compatibility score between user location preference and job location"""
    return mare_config.URBAN_RURAL_COMPATIBILITY.get(user_type, {}).get(job_type, 0.5)

def get_industry_cultural_fit(industry: str, cultural_context: str) -> float:
    """Get cultural fit score for industry and cultural context"""
    industry_fits = mare_config.INDUSTRY_CULTURAL_FIT.get(industry, {})
    return industry_fits.get(cultural_context, 0.5)

def calculate_time_weight(days_ago: int) -> float:
    """Calculate time-based weight for feedback (more recent = higher weight)"""
    if days_ago > mare_config.MAX_FEEDBACK_AGE_DAYS:
        return 0.0
    return mare_config.TIME_DECAY_FACTOR ** days_ago

def get_user_type_from_profile(profile: Dict[str, Any]) -> str:
    """Determine user type based on profile for weighted recommendations"""
    age = profile.get('age', 25)
    skills = profile.get('skills', [])
    
    if age <= 24 and len(skills) <= 3:
        return 'fresh_graduate'
    elif len(skills) >= 5:
        return 'experienced'
    else:
        return 'career_changer'
