import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import hashlib
import json

class FeatureEngineer:
    """Feature engineering for recommendation system"""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.tfidf_vectorizers = {}
        self.interest_vocabulary = set()
        self.skill_vocabulary = set()
    
    def create_user_profile_vector(self, user_profile: Dict[str, Any]) -> np.ndarray:
        """Create feature vector from user profile"""
        features = []
        
        # Academic features (normalized 0-1)
        academic_features = self._extract_academic_features(user_profile)
        features.extend(academic_features)
        
        # Demographic features (encoded)
        demographic_features = self._extract_demographic_features(user_profile)
        features.extend(demographic_features)
        
        # Interest/skill features (TF-IDF or binary)
        interest_features = self._extract_interest_features(user_profile)
        features.extend(interest_features)
        
        return np.array(features)
    
    def _extract_academic_features(self, profile: Dict[str, Any]) -> List[float]:
        """Extract and normalize academic features"""
        features = []
        
        # Normalize percentage scores (0-100 -> 0-1)
        tenth_pct = float(profile.get('tenth_percentage', 0)) / 100.0
        twelfth_pct = float(profile.get('twelfth_percentage', 0)) / 100.0
        current_marks = float(profile.get('current_marks_value', 0))
        
        # Normalize current marks based on type
        if profile.get('current_marks_type') == 'CGPA':
            current_marks = current_marks / 10.0  # Assuming 10-point CGPA scale
        else:
            current_marks = current_marks / 100.0  # Percentage
        
        features.extend([tenth_pct, twelfth_pct, current_marks])
        
        # Education level encoding (ordinal)
        education_levels = {
            'High School': 1, 'Intermediate': 2, 'Undergraduate': 3, 'Postgraduate': 4
        }
        edu_level = education_levels.get(profile.get('education_level', ''), 0) / 4.0
        features.append(edu_level)
        
        return features
    
    def _extract_demographic_features(self, profile: Dict[str, Any]) -> List[float]:
        """Extract demographic features"""
        features = []
        
        # Residence type encoding
        residence_types = {'Rural': 0, 'Semi-Urban': 1, 'Urban': 2, 'Metro': 3}
        residence = residence_types.get(profile.get('residence_type', ''), 1) / 3.0
        features.append(residence)
        
        # Family background encoding
        family_backgrounds = {'Lower Income': 0, 'Middle Income': 1, 'Upper Income': 2}
        family_bg = family_backgrounds.get(profile.get('family_background', ''), 1) / 2.0
        features.append(family_bg)
        
        return features
    
    def _extract_interest_features(self, profile: Dict[str, Any]) -> List[float]:
        """Extract interest and skill features using TF-IDF or binary encoding"""
        features = []
        
        # Get interests and skills
        interests_str = profile.get('interests', '')
        skills_str = profile.get('skills', '')
        
        # Combine interests and skills
        combined_text = ' '.join([interests_str, skills_str]).replace('|', ' ')
        
        # For now, use a simplified binary encoding
        # In production, you might want to use TF-IDF
        common_interests = [
            'technology', 'programming', 'coding', 'ai', 'data', 'science',
            'finance', 'healthcare', 'education', 'design', 'art', 'music',
            'sports', 'business', 'research', 'writing', 'communication',
            'leadership', 'analysis', 'mathematics', 'physics', 'chemistry'
        ]
        
        for interest in common_interests:
            has_interest = 1.0 if interest.lower() in combined_text.lower() else 0.0
            features.append(has_interest)
        
        return features
    
    def calculate_profile_similarity(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> float:
        """Calculate cosine similarity between two user profiles"""
        vector1 = self.create_user_profile_vector(profile1)
        vector2 = self.create_user_profile_vector(profile2)
        
        # Cosine similarity
        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def create_career_feature_vector(self, career: Dict[str, Any]) -> np.ndarray:
        """Create feature vector for a career"""
        features = []
        
        # Academic requirements
        min_10th = float(career.get('min_percentage_10th', 0)) / 100.0
        min_12th = float(career.get('min_percentage_12th', 0)) / 100.0
        min_cgpa = float(career.get('min_cgpa', 0)) / 10.0
        features.extend([min_10th, min_12th, min_cgpa])
        
        # Market features
        demand_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
        demand = demand_mapping.get(career.get('local_demand', 'Medium'), 1) / 2.0
        features.append(demand)
        
        # Success metrics
        success_rate = float(career.get('placement_success_rate', 0.5))
        popularity = float(career.get('peer_popularity_score', 0.5))
        features.extend([success_rate, popularity])
        
        # Skill/interest features (similar to user profile)
        skills_str = career.get('required_skills', '')
        interests_str = career.get('interests', '')
        combined_text = ' '.join([skills_str, interests_str]).replace(',', ' ')
        
        common_interests = [
            'technology', 'programming', 'coding', 'ai', 'data', 'science',
            'finance', 'healthcare', 'education', 'design', 'art', 'music',
            'sports', 'business', 'research', 'writing', 'communication',
            'leadership', 'analysis', 'mathematics', 'physics', 'chemistry'
        ]
        
        for interest in common_interests:
            has_interest = 1.0 if interest.lower() in combined_text.lower() else 0.0
            features.append(has_interest)
        
        return np.array(features)
    
    def calculate_user_career_compatibility(self, user_profile: Dict[str, Any], career: Dict[str, Any]) -> float:
        """Calculate compatibility score between user and career"""
        user_vector = self.create_user_profile_vector(user_profile)
        career_vector = self.create_career_feature_vector(career)
        
        # Ensure vectors are same length by padding shorter one
        max_len = max(len(user_vector), len(career_vector))
        user_padded = np.pad(user_vector, (0, max_len - len(user_vector)), mode='constant')
        career_padded = np.pad(career_vector, (0, max_len - len(career_vector)), mode='constant')
        
        # Calculate weighted similarity
        # Give more weight to academic compatibility and interests
        academic_weight = 0.3
        demographic_weight = 0.2
        interest_weight = 0.5
        
        # Academic compatibility (first 4 features)
        academic_user = user_padded[:4]
        academic_career = career_padded[:3]  # Career has 3 academic features
        academic_padded = np.pad(academic_career, (0, 1), mode='constant')
        academic_sim = np.dot(academic_user, academic_padded) / (np.linalg.norm(academic_user) * np.linalg.norm(academic_padded) + 1e-8)
        
        # Interest compatibility (last features)
        interest_user = user_padded[6:]  # Skip first 6 features
        interest_career = career_padded[5:]  # Skip first 5 features
        min_len = min(len(interest_user), len(interest_career))
        if min_len > 0:
            interest_sim = np.dot(interest_user[:min_len], interest_career[:min_len]) / (
                np.linalg.norm(interest_user[:min_len]) * np.linalg.norm(interest_career[:min_len]) + 1e-8
            )
        else:
            interest_sim = 0.0
        
        # Overall compatibility
        compatibility = academic_weight * academic_sim + interest_weight * interest_sim
        return min(max(compatibility, 0.0), 1.0)  # Clamp between 0 and 1
    
    def create_profile_hash(self, profile: Dict[str, Any]) -> str:
        """Create a hash for profile to use for caching"""
        # Create a simplified profile for hashing
        hash_data = {
            'education_level': profile.get('education_level', ''),
            'current_marks_value': profile.get('current_marks_value', 0),
            'interests': profile.get('interests', ''),
            'skills': profile.get('skills', ''),
            'residence_type': profile.get('residence_type', ''),
            'family_background': profile.get('family_background', '')
        }
        
        # Create hash
        profile_str = json.dumps(hash_data, sort_keys=True)
        return hashlib.md5(profile_str.encode()).hexdigest()
    
    def get_feature_importance_explanation(self, user_profile: Dict[str, Any], career: Dict[str, Any]) -> Dict[str, Any]:
        """Explain why a career was recommended"""
        explanations = {
            'academic_match': [],
            'interest_match': [],
            'skill_match': [],
            'demographic_match': []
        }
        
        # Academic explanations
        user_marks = float(user_profile.get('current_marks_value', 0))
        career_min_marks = max(
            float(career.get('min_percentage_10th', 0)),
            float(career.get('min_percentage_12th', 0)),
            float(career.get('min_cgpa', 0)) * 10  # Convert CGPA to percentage equivalent
        )
        
        if user_marks >= career_min_marks:
            explanations['academic_match'].append(f"Your academic performance ({user_marks}%) meets the requirements")
        
        # Interest matching
        user_interests = set(user_profile.get('interests', '').lower().split('|'))
        career_interests = set(career.get('interests', '').lower().split(','))
        common_interests = user_interests.intersection(career_interests)
        
        if common_interests:
            explanations['interest_match'].append(f"Shared interests: {', '.join(common_interests)}")
        
        # Skill matching
        user_skills = set(user_profile.get('skills', '').lower().split('|'))
        career_skills = set(career.get('required_skills', '').lower().split(','))
        common_skills = user_skills.intersection(career_skills)
        
        if common_skills:
            explanations['skill_match'].append(f"Matching skills: {', '.join(common_skills)}")
        
        return explanations
