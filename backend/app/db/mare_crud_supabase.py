"""
MARE CRUD Operations for Supabase (PostgreSQL)
Enhanced database operations for Multi-Dimensional Adaptive Recommendation Engine using Supabase
"""

from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, or_, func, desc
from supabase import Client
import logging
import json
import uuid

from ..db.supabase_client import get_supabase_client, get_db
from ..core.config import settings

logger = logging.getLogger(__name__)

class MAReCRUDSupabase:
    """CRUD operations for MARE system using Supabase"""
    
    def __init__(self, supabase_client: Optional[Client] = None):
        self.supabase = supabase_client or get_supabase_client()
        self.db_session = None
    
    def _get_session(self) -> Session:
        """Get database session"""
        if not self.db_session:
            from ..db.supabase_client import supabase_manager
            self.db_session = supabase_manager.SessionLocal()
        return self.db_session
    
    # User Profile Operations
    def create_user_profile(self, user_id: str, profile_data: Dict) -> str:
        """Create multi-dimensional user profile"""
        try:
            profile_payload = {
                "user_id": user_id,
                "age": profile_data.get("age"),
                "education_level": profile_data.get("education_level"),
                "location": profile_data.get("location"),
                "cultural_context": profile_data.get("cultural_context"),
                "family_background": profile_data.get("family_background"),
                "language_preference": profile_data.get("language_preference", "en"),
                "economic_context": profile_data.get("economic_context"),
                "financial_constraints": profile_data.get("financial_constraints"),
                "geographic_constraints": profile_data.get("geographic_constraints"),
                "urban_rural_type": profile_data.get("urban_rural_type", "urban"),
                "infrastructure_level": profile_data.get("infrastructure_level", "good"),
                "family_expectations": profile_data.get("family_expectations"),
                "peer_influence_score": profile_data.get("peer_influence_score", 0.5),
                "community_values": profile_data.get("community_values"),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Use upsert to handle existing profiles
            result = self.supabase.table("user_profiles").upsert(
                profile_payload,
                on_conflict="user_id"
            ).execute()
            
            if result.data:
                profile_id = result.data[0]["id"]
                logger.info(f"User profile created/updated: {profile_id}")
                return profile_id
            else:
                raise Exception("Failed to create user profile")
                
        except Exception as e:
            logger.error(f"Error creating user profile: {str(e)}")
            raise
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get complete user profile by user_id"""
        try:
            # Build complete profile from individual tables since view may not exist
            complete_profile = {}
            
            # Get base profile
            profile_result = self.supabase.table("profiles").select("*").eq("id", user_id).execute()
            if profile_result.data:
                complete_profile.update(profile_result.data[0])
                complete_profile["user_id"] = user_id
            else:
                logger.warning(f"No base profile found for user: {user_id}")
                return None
            
            # Get user_profiles
            user_profile_result = self.supabase.table("user_profiles").select("*").eq("user_id", user_id).execute()
            if user_profile_result.data:
                user_profile = user_profile_result.data[0]
                # Remove duplicate user_id and id to avoid conflicts
                user_profile.pop("user_id", None)
                user_profile.pop("id", None)
                complete_profile.update(user_profile)
            
            # Get career preferences
            prefs_result = self.supabase.table("career_preferences").select("*").eq("user_id", user_id).execute()
            if prefs_result.data:
                prefs = prefs_result.data[0]
                prefs.pop("user_id", None)
                prefs.pop("id", None)
                complete_profile.update(prefs)
            
            # Get skills and interests
            skills_result = self.supabase.table("user_skills_interests").select("*").eq("user_id", user_id).execute()
            if skills_result.data:
                skills = skills_result.data[0]
                skills.pop("user_id", None)
                skills.pop("id", None)
                complete_profile.update(skills)
            
            logger.info(f"Retrieved complete user profile for user: {user_id}")
            return complete_profile
            
        except Exception as e:
            logger.error(f"Error getting user profile: {str(e)}")
            return None
    
    def create_career_preferences(self, user_id: str, preferences_data: Dict) -> str:
        """Create or update career preferences"""
        try:
            preferences_payload = {
                "user_id": user_id,
                "career_goals": preferences_data.get("career_goals", ""),
                "preferred_industries": preferences_data.get("preferred_industries", []),
                "work_environment_preference": preferences_data.get("work_environment_preference", "office"),
                "salary_expectations": preferences_data.get("salary_expectations", ""),
                "work_life_balance_priority": preferences_data.get("work_life_balance_priority", 5),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Use INSERT/UPDATE pattern instead of upsert for now
            existing = self.supabase.table("career_preferences").select("id").eq("user_id", user_id).execute()
            
            if existing.data:
                # Update existing record
                result = self.supabase.table("career_preferences").update(
                    preferences_payload
                ).eq("user_id", user_id).execute()
            else:
                # Insert new record
                result = self.supabase.table("career_preferences").insert(
                    preferences_payload
                ).execute()
            
            if result.data:
                preferences_id = result.data[0]["id"]
                logger.info(f"Career preferences created/updated: {preferences_id}")
                return preferences_id
            else:
                raise Exception("Failed to create career preferences")
                
        except Exception as e:
            logger.error(f"Error creating career preferences: {str(e)}")
            raise
    
    def create_skills_interests(self, user_id: str, skills_data: Dict) -> str:
        """Create or update user skills and interests record"""
        try:
            # Map to actual table columns based on the real schema
            skills_payload = {
                "user_id": user_id,
                # Map our expected fields to actual table columns
                "technical_skills": skills_data.get("skills", []) + skills_data.get("technical_skills", []),
                "soft_skills": skills_data.get("soft_skills", []),
                "interests": skills_data.get("interests", []),
                "learning_preferences": skills_data.get("learning_preferences", []),
                "personality_traits": skills_data.get("personality_traits", []),
                "skill_assessments": skills_data.get("skill_assessments", {}),
                "interest_strength_scores": skills_data.get("interest_weights", {}),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # Use INSERT/UPDATE pattern instead of upsert for now
            existing = self.supabase.table("user_skills_interests").select("id").eq("user_id", user_id).execute()
            
            if existing.data:
                # Update existing record
                result = self.supabase.table("user_skills_interests").update(
                    skills_payload
                ).eq("user_id", user_id).execute()
            else:
                # Insert new record
                result = self.supabase.table("user_skills_interests").insert(
                    skills_payload
                ).execute()
            
            if result.data:
                skills_id = result.data[0]["id"]
                logger.info(f"Skills and interests created/updated: {skills_id}")
                return skills_id
            else:
                raise Exception("Failed to create skills and interests")
                
        except Exception as e:
            logger.error(f"Error creating skills and interests: {str(e)}")
            raise
    
    def _calculate_skill_scores(self, skills: List[str]) -> Dict[str, float]:
        """Calculate skill category scores based on user skills"""
        skill_categories = {
            "technical": [
                "Programming", "Data Analysis", "Machine Learning", "Web Development", 
                "Software Engineering", "Database Management", "System Administration",
                "Cybersecurity", "Mobile Development", "DevOps", "Cloud Computing"
            ],
            "creative": [
                "Design", "Writing", "Art", "Photography", "Video Editing",
                "Content Creation", "Graphic Design", "UI/UX Design", "Creative Writing"
            ],
            "analytical": [
                "Research", "Analysis", "Problem Solving", "Mathematics", 
                "Statistics", "Data Science", "Business Analysis", "Financial Analysis"
            ],
            "communication": [
                "Public Speaking", "Writing", "Languages", "Teaching",
                "Presentation", "Negotiation", "Customer Service", "Sales"
            ],
            "leadership": [
                "Management", "Team Leadership", "Project Management", "Mentoring",
                "Strategic Planning", "Decision Making", "Conflict Resolution"
            ]
        }
        
        scores = {}
        for category, category_skills in skill_categories.items():
            matches = sum(1 for skill in skills if any(
                cat_skill.lower() in skill.lower() or skill.lower() in cat_skill.lower()
                for cat_skill in category_skills
            ))
            scores[category] = min(matches / len(category_skills) * 2, 1.0)  # Cap at 1.0
        
        return scores
    
    # Career Opportunities Operations
    def get_career_opportunities(self, filters: Optional[Dict] = None, limit: int = 100) -> List[Dict]:
        """Get career opportunities with optional filters"""
        try:
            query = self.supabase.table("career_opportunities").select("*").eq("is_active", True)
            
            if filters:
                if filters.get("industry"):
                    query = query.eq("industry", filters["industry"])
                if filters.get("location"):
                    query = query.ilike("location", f"%{filters['location']}%")
                if filters.get("salary_min"):
                    query = query.gte("salary_range_min", filters["salary_min"])
                if filters.get("salary_max"):
                    query = query.lte("salary_range_max", filters["salary_max"])
                if filters.get("remote_available") is not None:
                    query = query.eq("remote_available", filters["remote_available"])
                if filters.get("urban_rural_type"):
                    query = query.in_("urban_rural_suitability", [filters["urban_rural_type"], "both"])
            
            result = query.limit(limit).execute()
            
            if result.data:
                logger.info(f"Retrieved {len(result.data)} career opportunities")
                return result.data
            return []
            
        except Exception as e:
            logger.error(f"Error getting career opportunities: {str(e)}")
            return []
    
    def get_career_opportunity(self, opportunity_id: str) -> Optional[Dict]:
        """Get single career opportunity by ID"""
        try:
            result = self.supabase.table("career_opportunities").select("*").eq("id", opportunity_id).execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            return None
            
        except Exception as e:
            logger.error(f"Error getting career opportunity: {str(e)}")
            return None
    
    def update_mare_compatibility_score(self, opportunity_id: str, score: float) -> bool:
        """Update MARE compatibility score for a career opportunity"""
        try:
            result = self.supabase.table("career_opportunities").update({
                "mare_compatibility_score": score,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", opportunity_id).execute()
            
            return bool(result.data)
            
        except Exception as e:
            logger.error(f"Error updating MARE compatibility score: {str(e)}")
            return False
    
    # Feedback and Learning Operations
    def save_recommendation_feedback(self, feedback_data: Dict) -> str:
        """Save user feedback for recommendations"""
        try:
            feedback_payload = {
                "user_id": feedback_data.get("user_id"),
                "career_opportunity_id": feedback_data.get("career_opportunity_id"),
                "recommendation_score": feedback_data.get("recommendation_score"),
                "user_rating": feedback_data.get("user_rating"),
                "user_feedback": feedback_data.get("user_feedback"),
                "selected": feedback_data.get("selected", False),
                "time_spent_viewing": feedback_data.get("time_spent_viewing", 0),
                "context_snapshot": feedback_data.get("context_snapshot", {}),
                "created_at": datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table("recommendation_feedback").upsert(
                feedback_payload,
                on_conflict="user_id,career_opportunity_id"
            ).execute()
            
            if result.data:
                feedback_id = result.data[0]["id"]
                logger.info(f"Recommendation feedback saved: {feedback_id}")
                return feedback_id
            else:
                raise Exception("Failed to save recommendation feedback")
                
        except Exception as e:
            logger.error(f"Error saving recommendation feedback: {str(e)}")
            raise
    
    def get_user_feedback_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's feedback history for learning"""
        try:
            result = self.supabase.table("recommendation_feedback").select(
                "*", 
                "career_opportunities(title, industry)"
            ).eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
            
            if result.data:
                logger.info(f"Retrieved {len(result.data)} feedback records for user: {user_id}")
                return result.data
            return []
            
        except Exception as e:
            logger.error(f"Error getting user feedback history: {str(e)}")
            return []
    
    # Analytics and Reporting
    def get_recommendation_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get recommendation analytics for the last N days"""
        try:
            # Use the recommendation_analytics view
            from_date = (datetime.utcnow().date() - timedelta(days=days)).isoformat()
            
            # Get analytics data using raw SQL through Supabase RPC
            result = self.supabase.rpc("get_recommendation_analytics", {
                "days_back": days
            }).execute()
            
            if result.data:
                return result.data[0]
            
            # Fallback to basic query if RPC not available
            feedback_result = self.supabase.table("recommendation_feedback").select("*").gte(
                "created_at", from_date
            ).execute()
            
            if feedback_result.data:
                total_recommendations = len(feedback_result.data)
                positive_feedback = sum(1 for f in feedback_result.data if f.get("user_rating", 0) >= 4)
                conversions = sum(1 for f in feedback_result.data if f.get("selected"))
                
                return {
                    "total_recommendations": total_recommendations,
                    "positive_feedback_rate": positive_feedback / total_recommendations if total_recommendations > 0 else 0,
                    "conversion_rate": conversions / total_recommendations if total_recommendations > 0 else 0,
                    "average_rating": sum(f.get("user_rating", 0) for f in feedback_result.data if f.get("user_rating")) / max(1, sum(1 for f in feedback_result.data if f.get("user_rating")))
                }
            
            return {
                "total_recommendations": 0,
                "positive_feedback_rate": 0.0,
                "conversion_rate": 0.0,
                "average_rating": 0.0
            }
            
        except Exception as e:
            logger.error(f"Error getting recommendation analytics: {str(e)}")
            return {
                "total_recommendations": 0,
                "positive_feedback_rate": 0.0,
                "conversion_rate": 0.0,
                "average_rating": 0.0
            }
    
    def get_popular_career_paths(self, limit: int = 10) -> List[Dict]:
        """Get most popular career paths based on user selections"""
        try:
            result = self.supabase.table("career_opportunities").select(
                "*",
                "recommendation_feedback(count)"
            ).eq("is_active", True).order("recommendation_count", desc=True).limit(limit).execute()
            
            if result.data:
                logger.info(f"Retrieved {len(result.data)} popular career paths")
                return result.data
            return []
            
        except Exception as e:
            logger.error(f"Error getting popular career paths: {str(e)}")
            return []

# Utility function to get MARE CRUD instance
def get_mare_crud_supabase() -> MAReCRUDSupabase:
    """Get MARE CRUD instance with Supabase"""
    return MAReCRUDSupabase()
