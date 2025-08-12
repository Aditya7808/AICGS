"""
Multi-Dimensional Adaptive Recommendation Engine (MARE)
Core implementation for AICGS system
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestRegressor
import json
import logging

@dataclass
class UserProfile:
    """Multi-dimensional user profile"""
    user_id: int
    
    # Personal dimensions
    age: int
    education_level: str
    location: str
    
    # Cultural dimensions
    cultural_context: str
    family_background: str
    language_preference: str
    
    # Economic dimensions
    economic_context: str
    
    # Geographic dimensions
    geographic_constraints: str
    urban_rural_type: str
    infrastructure_level: str
    
    # Social dimensions
    family_expectations: str
    
    # Optional fields with defaults
    financial_constraints: Optional[str] = None
    peer_influence_score: float = 0.5
    community_values: Optional[str] = None
    
    # Skills and interests
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    skill_weights: Optional[Dict[str, float]] = None
    interest_weights: Optional[Dict[str, float]] = None
    
    # Career preferences
    career_goals: str = ""
    preferred_industries: Optional[List[str]] = None
    work_environment_preference: str = ""
    salary_expectations: str = ""
    work_life_balance_priority: int = 5

@dataclass
class CareerOpportunity:
    """Career opportunity with multi-dimensional attributes"""
    opportunity_id: int
    title: str
    industry: str
    
    # Skills requirements
    required_skills: List[str]
    preferred_skills: List[str]
    
    # Geographic factors
    locations: List[str]
    remote_available: bool
    urban_rural_suitability: str
    
    # Economic factors
    salary_range_min: int
    salary_range_max: int
    education_requirements: List[str]
    
    # Cultural factors
    family_friendly_rating: int
    cultural_adaptability_score: float
    traditional_modern_spectrum: str
    
    # Growth factors
    growth_potential_score: float
    job_security_score: float
    future_outlook: str

class MAREEngine:
    """Multi-Dimensional Adaptive Recommendation Engine"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.dimension_weights = self.config['dimension_weights']
        self.scalers = {}
        self.encoders = {}
        self.models = {}
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _default_config(self) -> Dict:
        """Default configuration for MARE"""
        return {
            'dimension_weights': {
                'skills_match': 0.25,
                'cultural_fit': 0.20,
                'economic_viability': 0.20,
                'geographic_accessibility': 0.15,
                'social_alignment': 0.10,
                'growth_potential': 0.10
            },
            'similarity_threshold': 0.3,
            'max_recommendations': 10,
            'adaptive_learning_rate': 0.1
        }
    
    def calculate_skills_match(self, user_profile: UserProfile, 
                              opportunity: CareerOpportunity) -> float:
        """Calculate skills-based matching score"""
        try:
            if not user_profile.skills:
                return 0.0
                
            user_skills_set = set(user_profile.skills or [])
            required_skills_set = set(opportunity.required_skills or [])
            preferred_skills_set = set(opportunity.preferred_skills or [])
            
            # Calculate overlap with required skills (higher weight)
            required_overlap = len(user_skills_set & required_skills_set)
            required_total = len(required_skills_set)
            required_score = required_overlap / required_total if required_total > 0 else 0
            
            # Calculate overlap with preferred skills
            preferred_overlap = len(user_skills_set & preferred_skills_set)
            preferred_total = len(preferred_skills_set)
            preferred_score = preferred_overlap / preferred_total if preferred_total > 0 else 0
            
            # Weighted combination (required skills are more important)
            skills_score = (required_score * 0.7) + (preferred_score * 0.3)
            
            # Apply user skill weights if available
            if user_profile.skill_weights:
                weighted_score = 0
                total_weight = 0
                for skill in (user_skills_set & (required_skills_set | preferred_skills_set)):
                    weight = user_profile.skill_weights.get(skill, 1.0) or 1.0
                    weighted_score += weight
                    total_weight += weight
                
                if total_weight > 0:
                    skills_score = (skills_score + (weighted_score / total_weight)) / 2
            
            return float(min(skills_score, 1.0))
        except Exception as e:
            self.logger.error(f"Error calculating skills match: {e}")
            return 0.0  # Default to no match on error
    
    def calculate_cultural_fit(self, user_profile: UserProfile, 
                             opportunity: CareerOpportunity) -> float:
        """Calculate cultural compatibility score"""
        try:
            cultural_score = 0.0
            
            # Family-friendly alignment with null protection
            family_expectation_score = self._get_family_expectation_score(
                user_profile.family_expectations, 
                opportunity.family_friendly_rating
            ) or 0.5
            
            # Traditional vs Modern career alignment with null protection
            traditional_modern_score = self._get_traditional_modern_alignment(
                user_profile.cultural_context,
                opportunity.traditional_modern_spectrum
            ) or 0.5
            
            # Language and cultural adaptability with proper null protection
            cultural_adaptability_score = opportunity.cultural_adaptability_score
            if cultural_adaptability_score is None:
                cultural_adaptability_score = 0.5
            else:
                cultural_adaptability_score = float(cultural_adaptability_score)
            
            # Economic background alignment with null protection
            economic_cultural_score = self._get_economic_cultural_alignment(
                user_profile,
                opportunity
            ) or 0.5
            
            # Weighted combination with explicit float conversion
            cultural_score = (
                float(family_expectation_score) * 0.3 +
                float(traditional_modern_score) * 0.25 +
                float(cultural_adaptability_score) * 0.25 +
                float(economic_cultural_score) * 0.2
            )
            
            return float(cultural_score)
        except Exception as e:
            self.logger.error(f"Error calculating cultural fit: {e}")
            return 0.5  # Default middle score
    
    def calculate_economic_viability(self, user_profile: UserProfile,
                                   opportunity: CareerOpportunity) -> float:
        """Calculate economic viability score"""
        try:
            economic_score = 0.0
            
            # Education requirement match with null protection
            education_score = self._get_education_match_score(
                user_profile,
                opportunity
            ) or 0.5
            
            # Salary expectation alignment with null protection
            salary_score = self._get_salary_alignment_score(
                user_profile,
                opportunity
            ) or 0.5
            
            # Financial accessibility with null protection
            financial_score = self._get_financial_accessibility_score(
                user_profile,
                opportunity
            ) or 0.5
            
            economic_score = (
                education_score * 0.4 +
                salary_score * 0.35 +
                financial_score * 0.25
            )
            
            return float(economic_score)
        except Exception as e:
            self.logger.error(f"Error calculating economic viability: {e}")
            return 0.5  # Default middle score
    
    def calculate_geographic_accessibility(self, user_profile: UserProfile,
                                        opportunity: CareerOpportunity) -> float:
        """Calculate geographic accessibility score"""
        try:
            geographic_score = 0.0
            
            # Location proximity/availability with null protection
            location_score = self._get_location_accessibility_score(
                user_profile,
                opportunity
            ) or 0.5
            
            # Urban/rural suitability with null protection
            urban_rural_score = self._get_urban_rural_match_score(
                user_profile,
                opportunity
            ) or 0.5
            
            # Infrastructure compatibility with null protection
            infrastructure_score = self._get_infrastructure_compatibility_score(
                user_profile,
                opportunity
            ) or 0.5
            
            geographic_score = (
                location_score * 0.5 +
                urban_rural_score * 0.3 +
                infrastructure_score * 0.2
            )
            
            return float(geographic_score)
        except Exception as e:
            self.logger.error(f"Error calculating geographic accessibility: {e}")
            return 0.5  # Default middle score
    
    def calculate_social_alignment(self, user_profile: UserProfile,
                                 opportunity: CareerOpportunity) -> float:
        """Calculate social factors alignment score"""
        try:
            social_score = 0.0
            
            # Family expectations alignment with null protection
            family_score = self._get_family_career_alignment(
                user_profile,
                opportunity
            ) or 0.5
            
            # Peer influence consideration with null protection
            peer_score = user_profile.peer_influence_score or 0.5
            
            # Community values alignment with null protection
            community_score = self._get_community_values_alignment(
                user_profile,
                opportunity
            ) or 0.5
            
            social_score = (
                family_score * 0.5 +
                peer_score * 0.3 +
                community_score * 0.2
            )
            
            return float(social_score)
        except Exception as e:
            self.logger.error(f"Error calculating social alignment: {e}")
            return 0.5  # Default middle score
    
    def calculate_growth_potential(self, user_profile: UserProfile,
                                 opportunity: CareerOpportunity) -> float:
        """Calculate growth and future potential score"""
        try:
            # Direct opportunity scores with null protection
            growth_score = (
                (opportunity.growth_potential_score or 0.5) * 0.4 +
                (opportunity.job_security_score or 0.5) * 0.3 +
                (self._get_future_outlook_score(opportunity.future_outlook) or 0.5) * 0.3
            )
            
            # Adjust based on user's career goals alignment with null protection
            career_goals_alignment = self._get_career_goals_alignment(
                user_profile,
                opportunity
            ) or 0.5
            
            result = (growth_score * 0.7) + (career_goals_alignment * 0.3)
            return float(result)
        except Exception as e:
            self.logger.error(f"Error calculating growth potential: {e}")
            return 0.5  # Default middle score
    
    def generate_recommendations(self, user_profile: UserProfile,
                               career_opportunities: List[CareerOpportunity],
                               context: Optional[Dict] = None) -> List[Tuple[CareerOpportunity, float, Dict]]:
        """Generate multi-dimensional recommendations"""
        
        recommendations = []
        
        for opportunity in career_opportunities:
            # Calculate scores for each dimension with null handling
            scores = {}
            try:
                # Use enhanced skills matching for better OR logic support
                scores['skills_match'] = self.calculate_enhanced_skills_match(user_profile, opportunity) or 0.0
                scores['cultural_fit'] = self.calculate_cultural_fit(user_profile, opportunity) or 0.0
                scores['economic_viability'] = self.calculate_economic_viability(user_profile, opportunity) or 0.0
                scores['geographic_accessibility'] = self.calculate_geographic_accessibility(user_profile, opportunity) or 0.0
                scores['social_alignment'] = self.calculate_social_alignment(user_profile, opportunity) or 0.0
                scores['growth_potential'] = self.calculate_growth_potential(user_profile, opportunity) or 0.0
            except Exception as e:
                self.logger.error(f"Error calculating scores for opportunity {opportunity.title}: {e}")
                # Use default scores if calculation fails
                scores = {
                    'skills_match': 0.0,
                    'cultural_fit': 0.5,
                    'economic_viability': 0.5,
                    'geographic_accessibility': 0.5,
                    'social_alignment': 0.5,
                    'growth_potential': 0.5
                }
            
            # Calculate weighted overall score with null protection
            try:
                overall_score = sum(
                    (scores.get(dimension, 0.0) or 0.0) * (weight or 0.0)
                    for dimension, weight in self.dimension_weights.items()
                )
            except Exception as e:
                self.logger.error(f"Error calculating overall score: {e}")
                overall_score = 0.0
            
            # Apply contextual adjustments if provided
            if context:
                try:
                    overall_score = self._apply_contextual_adjustments(
                        overall_score, user_profile, opportunity, context
                    )
                except Exception as e:
                    self.logger.error(f"Error applying contextual adjustments: {e}")
            
            # Only include recommendations above threshold
            if overall_score >= self.config['similarity_threshold']:
                recommendations.append((opportunity, overall_score, scores))
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:self.config['max_recommendations']]
    
    def get_recommendations(self, user_profile: UserProfile, 
                           career_opportunities: List[CareerOpportunity],
                           context: Optional[Dict] = None) -> List:
        """Get recommendations with proper response format"""
        raw_recommendations = self.generate_recommendations(user_profile, career_opportunities, context)
        
        formatted_recommendations = []
        for opp, overall_score, dimension_scores in raw_recommendations:
            recommendation = type('Recommendation', (), {
                'opportunity_id': opp.opportunity_id,
                'career_id': str(opp.opportunity_id),
                'title': opp.title,
                'industry': opp.industry,
                'overall_score': overall_score,
                'dimension_scores': dimension_scores,
                'explanation': self._generate_explanation(dimension_scores, opp),
                'confidence_level': self._determine_confidence_level(overall_score)
            })()
            formatted_recommendations.append(recommendation)
        
        return formatted_recommendations
    
    def _generate_explanation(self, dimension_scores: Dict, opportunity) -> Dict[str, str]:
        """Generate human-readable explanations for recommendations"""
        explanations = {}
        
        for dimension, score in dimension_scores.items():
            if score >= 0.8:
                explanations[dimension] = f"Excellent match in {dimension.replace('_', ' ')}"
            elif score >= 0.6:
                explanations[dimension] = f"Good match in {dimension.replace('_', ' ')}"
            elif score >= 0.4:
                explanations[dimension] = f"Fair match in {dimension.replace('_', ' ')}"
            else:
                explanations[dimension] = f"Needs improvement in {dimension.replace('_', ' ')}"
        
        return explanations
    
    def _determine_confidence_level(self, overall_score: float) -> str:
        """Determine confidence level based on overall score"""
        if overall_score >= 0.8:
            return "High"
        elif overall_score >= 0.6:
            return "Medium"
        elif overall_score >= 0.4:
            return "Low"
        else:
            return "Very Low"

    def adaptive_learning_update(self, user_feedback: Dict):
        """Update recommendation weights based on user feedback"""
        # This would implement the adaptive learning component
        # Adjusting dimension weights based on user acceptance/rejection
        
        feedback_score = user_feedback.get('rating', 0)
        recommendation_scores = user_feedback.get('dimension_scores', {})
        
        if feedback_score >= 4:  # Positive feedback
            learning_rate = self.config['adaptive_learning_rate']
            
            # Increase weights for dimensions that scored well
            for dimension, score in recommendation_scores.items():
                if score > 0.7 and dimension in self.dimension_weights:
                    self.dimension_weights[dimension] += learning_rate * 0.1
            
        elif feedback_score <= 2:  # Negative feedback
            learning_rate = self.config['adaptive_learning_rate']
            
            # Decrease weights for dimensions that may have been over-weighted
            for dimension, score in recommendation_scores.items():
                if score > 0.8 and dimension in self.dimension_weights:
                    self.dimension_weights[dimension] -= learning_rate * 0.05
        
        # Normalize weights to sum to 1
        total_weight = sum(self.dimension_weights.values())
        for dimension in self.dimension_weights:
            self.dimension_weights[dimension] /= total_weight
        
        self.logger.info(f"Updated dimension weights: {self.dimension_weights}")
    
    # Safe score execution wrapper
    def _safe_score(self, score_func, *args, default=0.5):
        """Safely execute score function with default fallback"""
        try:
            result = score_func(*args)
            return float(result) if result is not None else default
        except Exception as e:
            self.logger.warning(f"Score function {score_func.__name__} failed: {e}")
            return default
    
    # Helper methods for specific calculations
    def _get_family_expectation_score(self, family_expectations: str, 
                                    family_friendly_rating: int) -> float:
        """Calculate family expectation alignment"""
        try:
            if not family_expectations:
                return 0.5
                
            # Ensure family_friendly_rating is a valid integer
            friendly_rating = family_friendly_rating if family_friendly_rating is not None else 3
            
            expectation_mapping = {
                'very_supportive': 0.9,
                'supportive_with_guidance': 0.8,
                'traditional_careers': 0.6 if friendly_rating >= 4 else 0.3,
                'high_earning_focus': 0.8,
                'local_opportunities': 0.7,
                'government_job': 0.5,
                'no_specific_expectations': 0.7
            }
            
            base_score = expectation_mapping.get(family_expectations, 0.5)
            
            # Adjust based on family-friendly rating with proper null protection
            family_rating_factor = float(friendly_rating) / 5.0
            
            return (base_score + family_rating_factor) / 2
        except Exception as e:
            self.logger.error(f"Error in family expectation score: {e}")
            return 0.5
    
    def _get_traditional_modern_alignment(self, cultural_context: str,
                                        traditional_modern_spectrum: str) -> float:
        """Calculate traditional vs modern career alignment"""
        try:
            context_scores = {
                'traditional': {'traditional': 0.9, 'moderate': 0.6, 'modern': 0.3},
                'moderate': {'traditional': 0.6, 'moderate': 0.9, 'modern': 0.6},
                'modern': {'traditional': 0.3, 'moderate': 0.6, 'modern': 0.9}
            }
            
            user_context = 'moderate'  # default
            if cultural_context and 'traditional' in cultural_context.lower():
                user_context = 'traditional'
            elif cultural_context and 'modern' in cultural_context.lower():
                user_context = 'modern'
            
            spectrum = traditional_modern_spectrum or 'moderate'
            return context_scores.get(user_context, {}).get(spectrum, 0.5)
        except Exception as e:
            self.logger.error(f"Error in traditional modern alignment: {e}")
            return 0.5
    
    def _get_economic_cultural_alignment(self, profile: UserProfile, opportunity: CareerOpportunity) -> float:
        """Calculate alignment between economic and cultural contexts"""
        try:
            score = 0.5  # Base score
            
            # Consider salary expectations vs range
            if profile.salary_expectations and opportunity.salary_range_min:
                # Simple heuristic - will be enhanced with real logic
                score += 0.3
                
            # Cultural adaptability with proper null protection
            cultural_score = opportunity.cultural_adaptability_score
            if cultural_score is not None:
                score += float(cultural_score) * 0.2
            
            return float(min(score, 1.0))
        except Exception as e:
            self.logger.error(f"Error in economic cultural alignment: {e}")
            return 0.5
    
    def _get_education_match_score(self, profile: UserProfile, opportunity: CareerOpportunity) -> float:
        """Calculate education requirements match"""
        try:
            # Simple education level matching
            education_levels = {
                'high_school': 1,
                'diploma': 2,
                'undergraduate': 3,
                'bachelor': 3,
                'postgraduate': 4,
                'master': 4,
                'phd': 5,
                'doctorate': 5
            }
            
            user_level = education_levels.get((profile.education_level or "").lower(), 3)
            required_level = 3  # Default bachelor's requirement
            
            if user_level >= required_level:
                return 1.0
            else:
                return max(0.3, user_level / required_level)
        except Exception as e:
            self.logger.error(f"Error in education match score: {e}")
            return 0.7
    
    def _get_salary_alignment_score(self, profile: UserProfile, opportunity: CareerOpportunity) -> float:
        """Calculate salary expectation alignment"""
        try:
            # Simple salary alignment - assume good match if no specific expectations
            salary_min = opportunity.salary_range_min if opportunity.salary_range_min is not None else 0
            salary_max = opportunity.salary_range_max if opportunity.salary_range_max is not None else 0
            
            if salary_min > 0 and salary_max > 0:
                avg_salary = (float(salary_min) + float(salary_max)) / 2
                # Simple heuristic: higher salary = better score up to a point
                return min(1.0, avg_salary / 1000000)  # Normalize to reasonable range
            
            return 0.7  # Default reasonable score
        except Exception as e:
            self.logger.error(f"Error in salary alignment score: {e}")
            return 0.7
    
    def _get_financial_accessibility_score(self, profile: UserProfile, opportunity: CareerOpportunity) -> float:
        """Calculate financial accessibility"""
        try:
            # Simple financial accessibility based on economic context
            economic_context = (profile.economic_context or "").lower()
            
            if "high" in economic_context:
                return 1.0
            elif "middle" in economic_context:
                return 0.8
            elif "low" in economic_context:
                return 0.6
            else:
                return 0.7  # Default
        except Exception as e:
            self.logger.error(f"Error in financial accessibility score: {e}")
            return 0.7
    
    def _get_infrastructure_compatibility_score(self, profile: UserProfile, opportunity: CareerOpportunity) -> float:
        """Calculate infrastructure compatibility"""
        try:
            # Simple heuristic based on infrastructure level
            infra_level = (profile.infrastructure_level or "good").lower()
            
            if "high" in infra_level or "good" in infra_level:
                return 1.0
            elif "medium" in infra_level or "fair" in infra_level:
                return 0.8
            else:
                return 0.6
        except Exception as e:
            self.logger.error(f"Error in infrastructure compatibility score: {e}")
            return 0.8
    
    def _get_location_accessibility_score(self, profile: UserProfile, opportunity: CareerOpportunity) -> float:
        """Calculate location accessibility"""
        try:
            if opportunity.remote_available:
                return 1.0
                
            # Simple location matching with null protection
            user_location = (profile.location or "").lower()
            for location in (opportunity.locations or []):
                if user_location in (location or "").lower():
                    return 1.0
                    
            return 0.6  # Partial match
        except Exception as e:
            self.logger.error(f"Error in location accessibility score: {e}")
            return 0.6
    
    def _get_urban_rural_match_score(self, profile: UserProfile, opportunity: CareerOpportunity) -> float:
        """Calculate urban/rural environment match"""
        try:
            user_type = (profile.urban_rural_type or "urban").lower()
            suitability = (opportunity.urban_rural_suitability or "both").lower()
            
            if user_type in suitability or "both" in suitability:
                return 1.0
            else:
                return 0.5
        except Exception as e:
            self.logger.error(f"Error in urban rural match score: {e}")
            return 0.5
    
    def _get_family_career_alignment(self, profile: UserProfile, opportunity: CareerOpportunity) -> float:
        """Calculate family career alignment"""
        try:
            # Simple family alignment based on family expectations
            expectations = (profile.family_expectations or "").lower()
            
            if "supportive" in expectations:
                return 0.9
            elif "traditional" in expectations:
                return 0.7
            elif "high_earning" in expectations:
                return 0.8
            else:
                return 0.7  # Default
        except Exception as e:
            self.logger.error(f"Error in family career alignment: {e}")
            return 0.7
    
    def _get_community_values_alignment(self, profile: UserProfile, opportunity: CareerOpportunity) -> float:
        """Calculate community values alignment"""
        try:
            # Simple community values alignment
            community_values = (profile.community_values or "").lower()
            
            if "progressive" in community_values or "modern" in community_values:
                return 0.8
            elif "traditional" in community_values:
                return 0.7
            else:
                return 0.75  # Default neutral score
        except Exception as e:
            self.logger.error(f"Error in community values alignment: {e}")
            return 0.75
    
    def _get_future_outlook_score(self, future_outlook: str) -> float:
        """Calculate future outlook score"""
        try:
            outlook_scores = {
                'excellent': 1.0,
                'very_good': 0.9,
                'good': 0.8,
                'booming': 1.0,
                'growing': 0.8,
                'stable': 0.6,
                'declining': 0.3,
                'poor': 0.2
            }
            
            return outlook_scores.get((future_outlook or "stable").lower(), 0.6)
        except Exception as e:
            self.logger.error(f"Error in future outlook score: {e}")
            return 0.6
    
    def _get_career_goals_alignment(self, profile: UserProfile, opportunity: CareerOpportunity) -> float:
        """Calculate career goals alignment"""
        try:
            # Simple career goals alignment based on keywords
            goals = (profile.career_goals or "").lower()
            title = (opportunity.title or "").lower()
            industry = (opportunity.industry or "").lower()
            
            # Look for keyword matches
            if any(word in goals for word in [title, industry]):
                return 0.9
            elif any(word in goals for word in ['technology', 'tech', 'software', 'data']):
                if any(word in industry for word in ['technology', 'tech', 'software', 'data']):
                    return 0.8
            
            return 0.6  # Default reasonable alignment
        except Exception as e:
            self.logger.error(f"Error in career goals alignment: {e}")
            return 0.6
    
    def _apply_contextual_adjustments(self, score: float, profile: UserProfile, 
                                    opportunity: CareerOpportunity, context: Dict) -> float:
        """Apply contextual adjustments to base score"""
        try:
            # Simple contextual adjustments
            adjusted_score = score
            
            # Apply any context-based adjustments
            if context.get('priority_skills'):
                # Boost score if opportunity matches priority skills
                priority_skills = set(context['priority_skills'])
                opp_skills = set(opportunity.required_skills or []) | set(opportunity.preferred_skills or [])
                if priority_skills & opp_skills:
                    adjusted_score *= 1.1
            
            return min(1.0, adjusted_score)
        except Exception as e:
            self.logger.error(f"Error in contextual adjustments: {e}")
            return score
    
    # Enhanced skill matching with OR logic
    SKILL_KEYWORDS_MAP = {
        'Communication': ['communication', 'speaking', 'presentation', 'writing', 'customer service', 'teaching', 'training', 'sales', 'marketing', 'public relations'],
        'Programming': ['software', 'developer', 'programming', 'coding', 'engineer', 'computer', 'technology', 'IT', 'python', 'java', 'javascript'],
        'Leadership': ['manager', 'director', 'leader', 'supervisor', 'executive', 'head', 'chief', 'coordinator', 'team lead'],
        'Problem Solving': ['analyst', 'consultant', 'researcher', 'scientist', 'engineer', 'troubleshoot', 'analytical', 'critical thinking'],
        'Creativity': ['designer', 'artist', 'creative', 'content', 'marketing', 'advertising', 'media', 'design', 'innovation'],
        'Teaching': ['teacher', 'educator', 'instructor', 'trainer', 'professor', 'tutor', 'academic', 'education'],
        'Healthcare': ['doctor', 'nurse', 'medical', 'health', 'physician', 'therapist', 'pharmacist', 'clinical'],
        'Sales': ['sales', 'business development', 'account manager', 'relationship manager', 'marketing', 'business'],
        'Finance': ['financial', 'accountant', 'banking', 'investment', 'analyst', 'finance', 'economics'],
        'Engineering': ['engineer', 'technical', 'design', 'development', 'construction', 'manufacturing', 'mechanical'],
        'Research': ['researcher', 'scientist', 'analyst', 'academic', 'laboratory', 'study', 'investigation'],
        'Management': ['manager', 'director', 'supervisor', 'coordinator', 'administrator', 'executive', 'operations'],
        'Data Analysis': ['analyst', 'data', 'statistics', 'research', 'scientist', 'business intelligence', 'analytics'],
        'Customer Service': ['customer', 'service', 'support', 'relations', 'representative', 'associate', 'help desk'],
        'Project Management': ['project', 'manager', 'coordinator', 'planner', 'operations', 'administrator', 'scrum']
    }

    def get_career_keywords_for_skill(self, skill: str) -> List[str]:
        """Get career keywords that match a user skill for OR logic search"""
        return self.SKILL_KEYWORDS_MAP.get(skill, [skill.lower()])

    def calculate_enhanced_skills_match(self, user_profile: UserProfile, 
                                      opportunity: CareerOpportunity) -> float:
        """Enhanced skills matching with OR logic and keyword-based search"""
        try:
            if not user_profile.skills:
                return 0.0
            
            # Convert opportunity data to searchable text
            searchable_text = (
                f"{opportunity.title} {opportunity.industry} "
                f"{' '.join(opportunity.required_skills or [])} "
                f"{' '.join(opportunity.preferred_skills or [])}"
            ).lower()
            
            # Calculate matches for each user skill using OR logic
            skill_matches = []
            total_possible_score = 0
            
            for skill in user_profile.skills:
                if not skill:
                    continue
                    
                skill_weight = user_profile.skill_weights.get(skill, 1.0) if user_profile.skill_weights else 1.0
                total_possible_score += skill_weight
                
                # Direct skill match
                skill_score = 0.0
                if skill.lower() in searchable_text:
                    skill_score = 1.0
                else:
                    # Keyword-based matching
                    keywords = self.get_career_keywords_for_skill(skill)
                    keyword_matches = sum(1 for keyword in keywords if keyword in searchable_text)
                    if keyword_matches > 0:
                        # Partial score based on keyword matches
                        skill_score = min(keyword_matches / len(keywords), 1.0) * 0.8
                
                # Apply skill weight
                weighted_score = skill_score * skill_weight
                skill_matches.append(weighted_score)
                
                self.logger.debug(f"Skill '{skill}' match score: {skill_score:.3f}, weighted: {weighted_score:.3f}")
            
            # Calculate overall skills match score
            if total_possible_score > 0:
                overall_score = sum(skill_matches) / total_possible_score
            else:
                overall_score = 0.0
            
            # Bonus for exact skill matches in required/preferred skills
            exact_matches = self.calculate_skills_match(user_profile, opportunity)
            
            # Combine enhanced matching with exact matching
            final_score = (overall_score * 0.7) + (exact_matches * 0.3)
            
            self.logger.debug(f"Enhanced skills match: {overall_score:.3f}, exact match: {exact_matches:.3f}, final: {final_score:.3f}")
            
            return float(min(final_score, 1.0))
            
        except Exception as e:
            self.logger.error(f"Error in enhanced skills matching: {e}")
            return self.calculate_skills_match(user_profile, opportunity)  # Fallback to basic matching

# Usage Example
if __name__ == "__main__":
    # Initialize MARE engine
    mare = MAREEngine()
    
    # Create sample user profile
    user = UserProfile(
        user_id=1,
        age=22,
        education_level="undergraduate",
        location="Mumbai",
        cultural_context="traditional",
        family_background="middle_class",
        language_preference="hindi",
        economic_context="middle_income",
        geographic_constraints="same_state",
        urban_rural_type="urban",
        infrastructure_level="good",
        family_expectations="high_earning_focus",
        skills=["Programming", "Communication", "Problem Solving"],
        interests=["Technology", "Data Science"],
        career_goals="Want to work in AI and make a positive impact"
    )
    
    # Create sample career opportunity
    opportunity = CareerOpportunity(
        opportunity_id=1,
        title="Data Scientist",
        industry="Technology",
        required_skills=["Programming", "Statistics", "Data Analysis"],
        preferred_skills=["Machine Learning", "Python", "SQL"],
        locations=["Mumbai", "Bangalore", "Delhi"],
        remote_available=True,
        urban_rural_suitability="urban",
        salary_range_min=800000,
        salary_range_max=1200000,
        education_requirements=["Bachelor's Degree"],
        family_friendly_rating=4,
        cultural_adaptability_score=0.8,
        traditional_modern_spectrum="modern",
        growth_potential_score=0.9,
        job_security_score=0.7,
        future_outlook="excellent"
    )
    
    # Generate recommendations
    recommendations = mare.generate_recommendations(user, [opportunity])
    
    for opp, score, dimension_scores in recommendations:
        print(f"Career: {opp.title}")
        print(f"Overall Score: {score:.3f}")
        print(f"Dimension Scores: {dimension_scores}")
        print("-" * 50)
