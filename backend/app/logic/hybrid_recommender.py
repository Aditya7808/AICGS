from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from ..db.crud import (
    get_user_profile, get_cached_recommendations, cache_recommendations,
    log_user_interaction
)
from .enhanced_matcher import get_enhanced_career_recommendations, calculate_enhanced_career_match
from .collaborative_filter import get_collaborative_recommendations, calculate_peer_popularity
from .feature_engineering import FeatureEngineer
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class HybridRecommendationEngine:
    """Hybrid recommendation engine combining content-based and collaborative filtering"""
    
    def __init__(self):
        self.feature_engineer = FeatureEngineer()
        self.content_weight = 0.6  # Weight for content-based filtering
        self.collaborative_weight = 0.4  # Weight for collaborative filtering
        
    def get_hybrid_recommendations(self, db: Session, user_id: int, 
                                 user_profile_data: Dict[str, Any],
                                 force_refresh: bool = False) -> Dict[str, Any]:
        """Get hybrid recommendations combining content-based and collaborative filtering"""
        
        # Create profile hash for caching
        profile_hash = self.feature_engineer.create_profile_hash(user_profile_data)
        
        # Check cache first (unless force refresh)
        if not force_refresh:
            cached_result = get_cached_recommendations(db, profile_hash)
            if cached_result:
                logger.info(f"Returning cached recommendations for user {user_id}")
                return cached_result.recommendations_json
        
        # Get content-based recommendations
        content_recommendations = get_enhanced_career_recommendations(db, user_profile_data)
        
        # Get collaborative recommendations
        collaborative_recommendations = get_collaborative_recommendations(db, user_id, user_profile_data)
        
        # Combine recommendations
        hybrid_recommendations = self._combine_recommendations(
            content_recommendations, 
            collaborative_recommendations,
            user_profile_data
        )
        
        # Generate final result
        result = {
            'user_id': user_id,
            'recommendations': hybrid_recommendations,
            'algorithm_info': {
                'content_weight': self.content_weight,
                'collaborative_weight': self.collaborative_weight,
                'content_recommendations_count': len(content_recommendations),
                'collaborative_recommendations_count': len(collaborative_recommendations),
                'hybrid_recommendations_count': len(hybrid_recommendations)
            },
            'generated_at': datetime.utcnow().isoformat(),
            'recommendation_explanations': self._generate_explanations(hybrid_recommendations)
        }
        
        # Cache the result
        try:
            scores = {
                'content_score': self._calculate_avg_content_score(content_recommendations),
                'collaborative_score': self._calculate_avg_collaborative_score(collaborative_recommendations),
                'hybrid_score': self._calculate_avg_hybrid_score(hybrid_recommendations),
                'confidence_level': self._calculate_overall_confidence(hybrid_recommendations)
            }
            cache_recommendations(db, profile_hash, result, scores)
        except Exception as e:
            logger.warning(f"Failed to cache recommendations: {e}")
        
        return result
    
    def _combine_recommendations(self, content_recs: List[Dict[str, Any]], 
                               collaborative_recs: List[Dict[str, Any]],
                               user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Combine content-based and collaborative recommendations"""
        
        # Create mappings for easier lookup
        content_by_id = {rec['career_id']: rec for rec in content_recs}
        collaborative_by_id = {rec['career_id']: rec for rec in collaborative_recs}
        
        # Get all unique career IDs
        all_career_ids = set(content_by_id.keys()) | set(collaborative_by_id.keys())
        
        hybrid_recommendations = []
        
        for career_id in all_career_ids:
            content_rec = content_by_id.get(career_id)
            collaborative_rec = collaborative_by_id.get(career_id)
            
            # Calculate hybrid score
            content_score = content_rec['overall_score'] if content_rec else 0.0
            collaborative_score = collaborative_rec['collaborative_score'] if collaborative_rec else 0.0
            
            # Handle cold start problem - if no collaborative data, rely more on content
            if collaborative_score == 0.0:
                adjusted_content_weight = 0.8
                adjusted_collaborative_weight = 0.2
            else:
                adjusted_content_weight = self.content_weight
                adjusted_collaborative_weight = self.collaborative_weight
            
            hybrid_score = (content_score * adjusted_content_weight + 
                          collaborative_score * adjusted_collaborative_weight)
            
            # Create combined recommendation
            hybrid_rec = self._create_hybrid_recommendation(
                career_id, content_rec, collaborative_rec, hybrid_score, user_profile
            )
            
            hybrid_recommendations.append(hybrid_rec)
        
        # Sort by hybrid score
        hybrid_recommendations.sort(key=lambda x: x['hybrid_score'], reverse=True)
        
        # Return top 15 recommendations
        return hybrid_recommendations[:15]
    
    def _create_hybrid_recommendation(self, career_id: int, content_rec: Optional[Dict[str, Any]], 
                                    collaborative_rec: Optional[Dict[str, Any]], 
                                    hybrid_score: float, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create a hybrid recommendation combining content and collaborative data"""
        
        # Base information (prefer content_rec as it has more details)
        base_rec = content_rec if content_rec else collaborative_rec
        
        recommendation = {
            'career_id': career_id,
            'career_name': base_rec['career_name'],
            'category': base_rec['category'],
            'hybrid_score': round(hybrid_score, 3),
            'recommendation_type': self._determine_recommendation_type(content_rec, collaborative_rec),
            'confidence_level': self._calculate_recommendation_confidence(content_rec, collaborative_rec),
            
            # Scores breakdown
            'scores': {
                'content_score': content_rec['overall_score'] if content_rec else 0.0,
                'collaborative_score': collaborative_rec['collaborative_score'] if collaborative_rec else 0.0,
                'academic_compatibility': content_rec['dimension_scores']['academic_compatibility'] if content_rec else 0.0,
                'interest_skill_match': content_rec['dimension_scores']['interest_skill_match'] if content_rec else 0.0,
                'peer_popularity': collaborative_rec['peer_score'] if collaborative_rec else 0.0
            },
            
            # Career details
            'career_details': base_rec['career_details'],
            
            # Explanations and insights
            'why_recommended': self._generate_recommendation_explanation(content_rec, collaborative_rec),
            'peer_insights': collaborative_rec['peer_insights'] if collaborative_rec else None,
            'content_explanations': content_rec['explanations'] if content_rec else None,
            
            # Success indicators
            'success_indicators': self._extract_success_indicators(content_rec, collaborative_rec),
            
            # Badges/tags
            'badges': self._generate_recommendation_badges(content_rec, collaborative_rec, user_profile)
        }
        
        return recommendation
    
    def _determine_recommendation_type(self, content_rec: Optional[Dict[str, Any]], 
                                     collaborative_rec: Optional[Dict[str, Any]]) -> str:
        """Determine the type of recommendation"""
        if content_rec and collaborative_rec:
            return "hybrid"
        elif content_rec:
            return "content_based"
        elif collaborative_rec:
            return "peer_based"
        else:
            return "unknown"
    
    def _calculate_recommendation_confidence(self, content_rec: Optional[Dict[str, Any]], 
                                           collaborative_rec: Optional[Dict[str, Any]]) -> float:
        """Calculate confidence level for the recommendation"""
        confidence = 0.5  # Base confidence
        
        if content_rec:
            confidence += content_rec['confidence_level'] * 0.6
        
        if collaborative_rec:
            peer_confidence = min(collaborative_rec['similar_users_count'] / 20.0, 0.4)
            confidence += peer_confidence
        
        return min(confidence, 1.0)
    
    def _generate_recommendation_explanation(self, content_rec: Optional[Dict[str, Any]], 
                                           collaborative_rec: Optional[Dict[str, Any]]) -> List[str]:
        """Generate explanation for why this career was recommended"""
        explanations = []
        
        if content_rec:
            # Add content-based explanations
            if content_rec['dimension_scores']['academic_compatibility'] > 0.7:
                explanations.append("Strong academic match for your background")
            
            if content_rec['dimension_scores']['interest_skill_match'] > 0.7:
                explanations.append("Excellent match with your interests and skills")
            
            # Add specific explanations from content analysis
            for category, category_explanations in content_rec['explanations'].items():
                if category_explanations:
                    explanations.extend(category_explanations[:2])  # Add top 2 explanations
        
        if collaborative_rec:
            # Add collaborative explanations
            peer_insights = collaborative_rec['peer_insights']
            if peer_insights['interest_percentage'] > 30:
                explanations.append(f"Popular among {peer_insights['interest_percentage']:.0f}% of similar students")
            
            if peer_insights['average_rating'] > 7:
                explanations.append(f"Highly rated ({peer_insights['average_rating']:.1f}/10) by peers")
        
        return explanations[:5]  # Return top 5 explanations
    
    def _extract_success_indicators(self, content_rec: Optional[Dict[str, Any]], 
                                  collaborative_rec: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract success indicators from both recommendation types"""
        indicators = {}
        
        if content_rec:
            career_details = content_rec['career_details']
            indicators.update({
                'placement_rate': career_details.get('placement_rate', 0),
                'market_demand': career_details.get('local_demand', 'Medium'),
                'growth_prospects': career_details.get('growth_prospects', 'Good')
            })
        
        if collaborative_rec:
            peer_insights = collaborative_rec['peer_insights']
            indicators.update({
                'peer_interest_count': peer_insights['interested_users_count'],
                'peer_rating': peer_insights['average_rating']
            })
        
        return indicators
    
    def _generate_recommendation_badges(self, content_rec: Optional[Dict[str, Any]], 
                                      collaborative_rec: Optional[Dict[str, Any]],
                                      user_profile: Dict[str, Any]) -> List[str]:
        """Generate badges/tags for the recommendation"""
        badges = []
        
        if content_rec:
            # Academic fit badges
            if content_rec['dimension_scores']['academic_compatibility'] > 0.8:
                badges.append("Perfect Academic Match")
            
            # Interest fit badges
            if content_rec['dimension_scores']['interest_skill_match'] > 0.8:
                badges.append("Excellent Interest Match")
            
            # Success probability badges
            if content_rec['dimension_scores']['success_probability'] > 0.7:
                badges.append("High Success Probability")
        
        if collaborative_rec:
            peer_insights = collaborative_rec['peer_insights']
            
            # Peer popularity badges
            if peer_insights['interest_percentage'] > 50:
                badges.append("Popular Among Peers")
            
            if peer_insights['average_rating'] > 8:
                badges.append("Highly Rated by Peers")
            
            if collaborative_rec['similar_users_count'] > 10:
                badges.append("Strong Peer Data")
        
        # Special badges based on user profile
        family_bg = user_profile.get('family_background', '')
        if family_bg == 'Lower Income':
            if content_rec and content_rec['career_details'].get('placement_rate', 0) > 0.8:
                badges.append("High Placement Rate")
        
        return badges[:4]  # Return top 4 badges
    
    def _generate_explanations(self, recommendations: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate overall explanations for the recommendation set"""
        if not recommendations:
            return {}
        
        total_recommendations = len(recommendations)
        hybrid_count = len([r for r in recommendations if r['recommendation_type'] == 'hybrid'])
        content_only_count = len([r for r in recommendations if r['recommendation_type'] == 'content_based'])
        peer_only_count = len([r for r in recommendations if r['recommendation_type'] == 'peer_based'])
        
        explanations = {
            'overview': f"Generated {total_recommendations} personalized career recommendations",
            'methodology': f"Combined academic/interest matching ({content_only_count + hybrid_count} careers) with peer analysis ({peer_only_count + hybrid_count} careers)",
            'confidence': f"High confidence recommendations based on {hybrid_count} careers with both academic and peer validation"
        }
        
        return explanations
    
    def _calculate_avg_content_score(self, content_recs: List[Dict[str, Any]]) -> float:
        """Calculate average content score"""
        if not content_recs:
            return 0.0
        return sum(rec['overall_score'] for rec in content_recs) / len(content_recs)
    
    def _calculate_avg_collaborative_score(self, collaborative_recs: List[Dict[str, Any]]) -> float:
        """Calculate average collaborative score"""
        if not collaborative_recs:
            return 0.0
        return sum(rec['collaborative_score'] for rec in collaborative_recs) / len(collaborative_recs)
    
    def _calculate_avg_hybrid_score(self, hybrid_recs: List[Dict[str, Any]]) -> float:
        """Calculate average hybrid score"""
        if not hybrid_recs:
            return 0.0
        return sum(rec['hybrid_score'] for rec in hybrid_recs) / len(hybrid_recs)
    
    def _calculate_overall_confidence(self, hybrid_recs: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence level"""
        if not hybrid_recs:
            return 0.0
        return sum(rec['confidence_level'] for rec in hybrid_recs) / len(hybrid_recs)

def get_hybrid_career_recommendations(db: Session, user_id: int, 
                                    user_profile_data: Optional[Dict[str, Any]] = None,
                                    force_refresh: bool = False) -> Dict[str, Any]:
    """Main function to get hybrid career recommendations"""
    
    # Get user profile if not provided
    if user_profile_data is None:
        user_profile_obj = get_user_profile(db, user_id)
        if not user_profile_obj:
            raise ValueError(f"User profile not found for user {user_id}")
        
        user_profile_data = {
            'education_level': getattr(user_profile_obj, 'education_level', ''),
            'current_marks_value': getattr(user_profile_obj, 'current_marks_value', 0),
            'current_marks_type': getattr(user_profile_obj, 'current_marks_type', ''),
            'tenth_percentage': getattr(user_profile_obj, 'tenth_percentage', 0),
            'twelfth_percentage': getattr(user_profile_obj, 'twelfth_percentage', 0),
            'interests': getattr(user_profile_obj, 'interests', ''),
            'skills': getattr(user_profile_obj, 'skills', ''),
            'residence_type': getattr(user_profile_obj, 'residence_type', ''),
            'family_background': getattr(user_profile_obj, 'family_background', ''),
            'place_of_residence': getattr(user_profile_obj, 'place_of_residence', ''),
        }
    
    # Create hybrid engine and get recommendations
    hybrid_engine = HybridRecommendationEngine()
    recommendations = hybrid_engine.get_hybrid_recommendations(
        db, user_id, user_profile_data, force_refresh
    )
    
    # Log the recommendation request
    try:
        log_user_interaction(db, user_id, None, 'recommendation_request', context_data={
            'recommendation_count': len(recommendations.get('recommendations', [])),
            'algorithm_version': 'hybrid_v2.0'
        })
    except Exception as e:
        logger.warning(f"Failed to log recommendation interaction: {e}")
    
    return recommendations
