from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from ..db.crud import (
    get_user_interactions, get_similar_users_by_interactions, 
    get_user_profile, get_careers
)
from ..models.user import UserProfile
from ..models.career import Career
from ..models.interaction import UserInteraction
from .feature_engineering import FeatureEngineer
import numpy as np
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)

class CollaborativeFilter:
    """Collaborative filtering for career recommendations based on user similarity"""
    
    def __init__(self):
        self.feature_engineer = FeatureEngineer()
        self.user_similarity_cache = {}
        
    def calculate_user_similarity(self, user_profile1: Dict[str, Any], user_profile2: Dict[str, Any]) -> float:
        """Calculate similarity between two user profiles"""
        try:
            return self.feature_engineer.calculate_profile_similarity(user_profile1, user_profile2)
        except Exception as e:
            logger.warning(f"Error calculating user similarity: {e}")
            return 0.0
    
    def find_similar_users(self, db: Session, target_user_id: int, target_profile: Dict[str, Any], 
                          limit: int = 20) -> List[Tuple[int, float]]:
        """Find users similar to the target user based on profile and interactions"""
        
        # First, get users with similar interaction patterns
        interaction_similar_users = get_similar_users_by_interactions(db, target_user_id, limit * 2)
        
        # Then, calculate profile similarity for these users
        similar_users = []
        
        for similar_user_id in interaction_similar_users:
            if similar_user_id == target_user_id:
                continue
                
            # Get the similar user's profile
            similar_user_profile_obj = get_user_profile(db, similar_user_id)
            
            if similar_user_profile_obj:
                # Convert to dictionary format
                similar_profile = {
                    'education_level': getattr(similar_user_profile_obj, 'education_level', ''),
                    'current_marks_value': getattr(similar_user_profile_obj, 'current_marks_value', 0),
                    'current_marks_type': getattr(similar_user_profile_obj, 'current_marks_type', ''),
                    'tenth_percentage': getattr(similar_user_profile_obj, 'tenth_percentage', 0),
                    'twelfth_percentage': getattr(similar_user_profile_obj, 'twelfth_percentage', 0),
                    'interests': getattr(similar_user_profile_obj, 'interests', ''),
                    'skills': getattr(similar_user_profile_obj, 'skills', ''),
                    'residence_type': getattr(similar_user_profile_obj, 'residence_type', ''),
                    'family_background': getattr(similar_user_profile_obj, 'family_background', ''),
                }
                
                # Calculate similarity
                similarity_score = self.calculate_user_similarity(target_profile, similar_profile)
                
                if similarity_score > 0.3:  # Threshold for similarity
                    similar_users.append((similar_user_id, similarity_score))
        
        # Sort by similarity score and return top users
        similar_users.sort(key=lambda x: x[1], reverse=True)
        return similar_users[:limit]
    
    def get_peer_career_preferences(self, db: Session, similar_users: List[Tuple[int, float]]) -> Dict[int, float]:
        """Get career preferences from similar users weighted by similarity"""
        
        career_scores = defaultdict(float)
        career_counts = defaultdict(int)
        
        for user_id, similarity_score in similar_users:
            # Get user interactions
            user_interactions = get_user_interactions(db, user_id, limit=50)
            
            for interaction in user_interactions:
                career_id = getattr(interaction, 'career_id', None)
                interaction_type = getattr(interaction, 'interaction_type', '')
                rating = getattr(interaction, 'rating', None)
                
                if career_id:
                    # Weight the interaction based on type and similarity
                    interaction_weight = self._get_interaction_weight(interaction_type, rating)
                    weighted_score = interaction_weight * similarity_score
                    
                    career_scores[career_id] += weighted_score
                    career_counts[career_id] += 1
        
        # Normalize scores by count and similarity
        normalized_scores = {}
        for career_id, total_score in career_scores.items():
            if career_counts[career_id] > 0:
                normalized_scores[career_id] = total_score / career_counts[career_id]
        
        return normalized_scores
    
    def _get_interaction_weight(self, interaction_type: str, rating: Optional[float]) -> float:
        """Get weight for different types of interactions"""
        weights = {
            'view': 0.1,
            'bookmark': 0.6,
            'share': 0.8,
            'rate': 0.9,
            'apply': 1.0
        }
        
        base_weight = weights.get(interaction_type, 0.1)
        
        # If there's a rating, incorporate it
        if rating is not None and interaction_type == 'rate':
            # Normalize rating (assuming 1-10 scale) and combine with base weight
            normalized_rating = min(max(rating, 1), 10) / 10.0
            return base_weight * normalized_rating
        
        return base_weight
    
    def get_trending_careers(self, db: Session, user_profile: Dict[str, Any], 
                           time_window_days: int = 30) -> Dict[int, float]:
        """Get trending careers among users with similar demographics"""
        
        # This is a simplified version - in production, you'd filter by time
        # and use more sophisticated trending algorithms
        
        demographic_filters = {
            'education_level': user_profile.get('education_level', ''),
            'residence_type': user_profile.get('residence_type', ''),
            'family_background': user_profile.get('family_background', '')
        }
        
        # For now, return empty dict - can be enhanced with time-based trending
        return {}
    
    def calculate_collaborative_scores(self, db: Session, user_id: int, 
                                     user_profile: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
        """Calculate collaborative filtering scores for all careers"""
        
        # Find similar users
        similar_users = self.find_similar_users(db, user_id, user_profile)
        
        if not similar_users:
            logger.info(f"No similar users found for user {user_id}")
            return {}
        
        # Get peer preferences
        peer_preferences = self.get_peer_career_preferences(db, similar_users)
        
        # Get trending careers
        trending_careers = self.get_trending_careers(db, user_profile)
        
        # Combine scores
        collaborative_scores = {}
        
        for career_id, peer_score in peer_preferences.items():
            trending_score = trending_careers.get(career_id, 0.0)
            
            # Combine peer and trending scores
            combined_score = (peer_score * 0.8) + (trending_score * 0.2)
            
            # Get peer insights
            peer_insights = self._generate_peer_insights(db, career_id, similar_users)
            
            collaborative_scores[career_id] = {
                'score': combined_score,
                'peer_score': peer_score,
                'trending_score': trending_score,
                'similar_users_count': len(similar_users),
                'peer_insights': peer_insights
            }
        
        return collaborative_scores
    
    def _generate_peer_insights(self, db: Session, career_id: int, 
                               similar_users: List[Tuple[int, float]]) -> Dict[str, Any]:
        """Generate insights about peer preferences for a career"""
        
        # Count how many similar users interacted with this career
        interested_users = 0
        total_rating = 0.0
        rating_count = 0
        interaction_types = Counter()
        
        for user_id, similarity_score in similar_users:
            user_interactions = get_user_interactions(db, user_id, limit=50)
            
            for interaction in user_interactions:
                if getattr(interaction, 'career_id', None) == career_id:
                    interested_users += 1
                    interaction_type = getattr(interaction, 'interaction_type', '')
                    interaction_types[interaction_type] += 1
                    
                    rating = getattr(interaction, 'rating', None)
                    if rating is not None:
                        total_rating += rating
                        rating_count += 1
                    
                    break  # Count each user only once
        
        avg_rating = total_rating / rating_count if rating_count > 0 else 0.0
        interest_percentage = (interested_users / len(similar_users)) * 100 if similar_users else 0
        
        return {
            'interested_users_count': interested_users,
            'interest_percentage': round(interest_percentage, 1),
            'average_rating': round(avg_rating, 1),
            'most_common_interaction': interaction_types.most_common(1)[0][0] if interaction_types else None,
            'total_interactions': sum(interaction_types.values())
        }

def get_collaborative_recommendations(db: Session, user_id: int, 
                                    user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get career recommendations using collaborative filtering"""
    
    collaborative_filter = CollaborativeFilter()
    
    # Calculate collaborative scores
    collaborative_scores = collaborative_filter.calculate_collaborative_scores(db, user_id, user_profile)
    
    if not collaborative_scores:
        return []
    
    # Get career details and combine with scores
    careers = get_careers(db)
    career_dict = {getattr(career, 'id', 0): career for career in careers}
    
    recommendations = []
    
    for career_id, score_data in collaborative_scores.items():
        if career_id in career_dict:
            career = career_dict[career_id]
            
            recommendation = {
                'career_id': career_id,
                'career_name': getattr(career, 'name', 'Unknown'),
                'category': getattr(career, 'category', 'General'),
                'collaborative_score': round(score_data['score'], 3),
                'peer_score': round(score_data['peer_score'], 3),
                'similar_users_count': score_data['similar_users_count'],
                'peer_insights': score_data['peer_insights'],
                'recommendation_reason': f"Popular among {score_data['peer_insights']['interested_users_count']} similar users",
                'career_details': {
                    'local_demand': getattr(career, 'local_demand', 'Medium'),
                    'average_salary': getattr(career, 'average_salary_range', 'Not specified'),
                    'growth_prospects': getattr(career, 'growth_prospects', 'Good')
                }
            }
            
            recommendations.append(recommendation)
    
    # Sort by collaborative score
    recommendations.sort(key=lambda x: x['collaborative_score'], reverse=True)
    
    return recommendations[:10]  # Return top 10

def calculate_peer_popularity(db: Session, career_id: int, user_demographics: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate how popular a career is among peers with similar demographics"""
    
    # This is a simplified implementation
    # In production, you would filter users by demographics and calculate popularity
    
    collaborative_filter = CollaborativeFilter()
    
    # For now, return basic popularity metrics
    return {
        'popularity_score': 0.5,  # Placeholder
        'peer_interest_percentage': 0.0,
        'average_peer_rating': 0.0,
        'total_peer_interactions': 0
    }
