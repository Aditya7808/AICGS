"""
Supabase CRUD Operations for Progress Tracking
Handles user progress, skills, goals, and assessment history
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
import logging
from ..db.supabase_client import get_supabase_client, get_supabase_service_client
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class ProgressCRUD:
    """CRUD operations for progress tracking in Supabase"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self.supabase_service = get_supabase_service_client()
    
    # User Progress Methods
    async def get_or_create_user_progress(self, user_id: str) -> Dict[str, Any]:
        """Get or create user progress record"""
        try:
            # Try to get existing progress
            result = self.supabase.table("user_progress").select("*").eq("user_id", user_id).execute()
            
            if result.data:
                return result.data[0]
            
            # Create new progress record
            new_progress = {
                "user_id": user_id,
                "total_assessments_completed": 0,
                "career_goals_set": 0,
                "skills_tracked": 0,
                "current_streak_days": 0,
                "longest_streak_days": 0,
                "profile_completeness": 0.1,  # Basic profile exists
                "skill_development_score": 0.0,
                "career_clarity_score": 0.0,
                "milestones_achieved": []
            }
            
            result = self.supabase.table("user_progress").insert(new_progress).execute()
            return result.data[0] if result.data else new_progress
            
        except Exception as e:
            logger.error(f"Error getting/creating user progress for {user_id}: {e}")
            # Return default values if database fails
            return {
                "user_id": user_id,
                "total_assessments_completed": 0,
                "career_goals_set": 0,
                "skills_tracked": 0,
                "current_streak_days": 0,
                "longest_streak_days": 0,
                "profile_completeness": 0.1,
                "skill_development_score": 0.0,
                "career_clarity_score": 0.0,
                "milestones_achieved": []
            }
    
    async def update_user_progress(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user progress metrics"""
        try:
            updates["updated_at"] = datetime.now().isoformat()
            result = self.supabase.table("user_progress").update(updates).eq("user_id", user_id).execute()
            return result.data[0] if result.data else {}
        except Exception as e:
            logger.error(f"Error updating user progress for {user_id}: {e}")
            return {}
    
    async def update_activity_streak(self, user_id: str) -> Dict[str, Any]:
        """Update user activity streak"""
        try:
            progress = await self.get_or_create_user_progress(user_id)
            
            last_activity = progress.get("last_activity_date")
            current_streak = progress.get("current_streak_days", 0)
            longest_streak = progress.get("longest_streak_days", 0)
            
            today = datetime.now().date()
            
            if last_activity:
                # Parse the last activity date
                if isinstance(last_activity, str):
                    last_date = datetime.fromisoformat(last_activity.replace('Z', '+00:00')).date()
                else:
                    last_date = last_activity.date()
                
                days_diff = (today - last_date).days
                
                if days_diff == 1:
                    # Consecutive day - increment streak
                    current_streak += 1
                elif days_diff > 1:
                    # Streak broken - reset
                    current_streak = 1
                # If days_diff == 0, same day - no change to streak
            else:
                # First activity
                current_streak = 1
            
            # Update longest streak if current is longer
            longest_streak = max(longest_streak, current_streak)
            
            updates = {
                "current_streak_days": current_streak,
                "longest_streak_days": longest_streak,
                "last_activity_date": datetime.now().isoformat()
            }
            
            return await self.update_user_progress(user_id, updates)
            
        except Exception as e:
            logger.error(f"Error updating activity streak for {user_id}: {e}")
            return {}
    
    # Skill Progress Methods
    async def get_user_skill_progress(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all skill progress for a user"""
        try:
            result = self.supabase.table("skill_progress").select("*").eq("user_id", user_id).order("created_at", desc=False).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting skill progress for {user_id}: {e}")
            return []
    
    async def create_or_update_skill_progress(self, user_id: str, skill_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update skill progress"""
        try:
            skill_name = skill_data.get("skill_name")
            
            # Check if skill already exists
            existing = self.supabase.table("skill_progress").select("*").eq("user_id", user_id).eq("skill_name", skill_name).execute()
            
            if existing.data:
                # Update existing skill
                skill_id = existing.data[0]["id"]
                updates = {k: v for k, v in skill_data.items() if k != "skill_name"}
                updates["updated_at"] = datetime.now().isoformat()
                
                result = self.supabase.table("skill_progress").update(updates).eq("id", skill_id).execute()
                return result.data[0] if result.data else {}
            else:
                # Create new skill
                new_skill = {
                    "user_id": user_id,
                    **skill_data
                }
                result = self.supabase.table("skill_progress").insert(new_skill).execute()
                return result.data[0] if result.data else {}
                
        except Exception as e:
            logger.error(f"Error creating/updating skill progress for {user_id}: {e}")
            return {}
    
    async def delete_skill_progress(self, user_id: str, skill_id: str) -> bool:
        """Delete a skill progress record"""
        try:
            result = self.supabase.table("skill_progress").delete().eq("id", skill_id).eq("user_id", user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Error deleting skill progress {skill_id} for {user_id}: {e}")
            return False
    
    # Career Goals Methods
    async def get_user_career_goals(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all career goals for a user"""
        try:
            result = self.supabase.table("career_goals").select("*").eq("user_id", user_id).order("created_at", desc=False).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting career goals for {user_id}: {e}")
            return []
    
    async def create_career_goal(self, user_id: str, goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new career goal"""
        try:
            new_goal = {
                "user_id": user_id,
                **goal_data
            }
            result = self.supabase.table("career_goals").insert(new_goal).execute()
            return result.data[0] if result.data else {}
        except Exception as e:
            logger.error(f"Error creating career goal for {user_id}: {e}")
            return {}
    
    async def update_career_goal(self, user_id: str, goal_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a career goal"""
        try:
            updates["updated_at"] = datetime.now().isoformat()
            result = self.supabase.table("career_goals").update(updates).eq("id", goal_id).eq("user_id", user_id).execute()
            return result.data[0] if result.data else {}
        except Exception as e:
            logger.error(f"Error updating career goal {goal_id} for {user_id}: {e}")
            return {}
    
    async def delete_career_goal(self, user_id: str, goal_id: str) -> bool:
        """Delete a career goal"""
        try:
            result = self.supabase.table("career_goals").delete().eq("id", goal_id).eq("user_id", user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Error deleting career goal {goal_id} for {user_id}: {e}")
            return False
    
    # Assessment History Methods
    async def get_user_assessment_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get assessment history for a user"""
        try:
            result = self.supabase.table("assessment_history").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting assessment history for {user_id}: {e}")
            return []
    
    async def create_assessment_record(self, user_id: str, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new assessment record"""
        try:
            new_assessment = {
                "user_id": user_id,
                **assessment_data
            }
            result = self.supabase.table("assessment_history").insert(new_assessment).execute()
            
            # Update total assessments count
            await self.increment_assessment_count(user_id)
            
            return result.data[0] if result.data else {}
        except Exception as e:
            logger.error(f"Error creating assessment record for {user_id}: {e}")
            return {}
    
    async def increment_assessment_count(self, user_id: str) -> None:
        """Increment the total assessments count"""
        try:
            progress = await self.get_or_create_user_progress(user_id)
            current_count = progress.get("total_assessments_completed", 0)
            
            updates = {
                "total_assessments_completed": current_count + 1,
                "last_assessment_date": datetime.now().isoformat()
            }
            
            await self.update_user_progress(user_id, updates)
            await self.update_activity_streak(user_id)
            
        except Exception as e:
            logger.error(f"Error incrementing assessment count for {user_id}: {e}")
    
    # Analytics Methods
    async def get_progress_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive progress analytics for a user"""
        try:
            # Get data from multiple tables
            progress = await self.get_or_create_user_progress(user_id)
            skills = await self.get_user_skill_progress(user_id)
            goals = await self.get_user_career_goals(user_id)
            history = await self.get_user_assessment_history(user_id, limit=10)
            
            # Calculate analytics
            active_goals = [g for g in goals if g.get("status") == "active"]
            completed_goals = [g for g in goals if g.get("status") == "completed"]
            
            # Skill distribution
            skill_levels = {}
            for skill in skills:
                level = skill.get("current_level", "beginner")
                skill_levels[level] = skill_levels.get(level, 0) + 1
            
            # Assessment patterns
            days_since_last = None
            if progress.get("last_assessment_date"):
                last_date = datetime.fromisoformat(progress["last_assessment_date"].replace('Z', '+00:00'))
                days_since_last = (datetime.now() - last_date).days
            
            # Goal progress analysis
            avg_goal_progress = 0
            if goals:
                total_progress = sum(float(g.get("progress_percentage", 0)) for g in goals)
                avg_goal_progress = total_progress / len(goals)
            
            return {
                "overview": {
                    "total_assessments": progress.get("total_assessments_completed", 0),
                    "active_goals": len(active_goals),
                    "completed_goals": len(completed_goals),
                    "skills_tracked": len(skills),
                    "profile_completeness": float(progress.get("profile_completeness", 0.0)),
                    "current_streak": progress.get("current_streak_days", 0),
                    "longest_streak": progress.get("longest_streak_days", 0)
                },
                "skill_distribution": skill_levels,
                "goal_progress": {
                    "average_progress": avg_goal_progress,
                    "goals_by_status": {
                        "active": len(active_goals),
                        "completed": len(completed_goals),
                        "paused": len([g for g in goals if g.get("status") == "paused"]),
                        "cancelled": len([g for g in goals if g.get("status") == "cancelled"])
                    }
                },
                "assessment_patterns": {
                    "days_since_last_assessment": days_since_last,
                    "recent_assessments": len(history),
                    "assessment_frequency": "regular" if days_since_last and days_since_last < 7 else "irregular"
                },
                "progress_trends": [],  # Could implement trend analysis
                "upcoming_milestones": self._get_upcoming_milestones(skills, goals),
                "recommendations": self._generate_recommendations(progress, skills, goals, history)
            }
            
        except Exception as e:
            logger.error(f"Error getting progress analytics for {user_id}: {e}")
            return {
                "overview": {},
                "skill_distribution": {},
                "goal_progress": {},
                "assessment_patterns": {},
                "progress_trends": [],
                "upcoming_milestones": [],
                "recommendations": []
            }
    
    def _get_upcoming_milestones(self, skills: List[Dict], goals: List[Dict]) -> List[Dict[str, Any]]:
        """Get upcoming milestones from skills and goals"""
        milestones = []
        
        # Check skill target dates
        for skill in skills:
            target_date = skill.get("target_date")
            if target_date:
                try:
                    target = datetime.fromisoformat(target_date.replace('Z', '+00:00'))
                    if target > datetime.now():
                        days_until = (target - datetime.now()).days
                        milestones.append({
                            "type": "skill",
                            "title": f"Complete {skill['skill_name']} ({skill['target_level']})",
                            "due_date": target_date,
                            "days_until": days_until
                        })
                except (ValueError, TypeError):
                    pass
        
        # Check goal completion dates
        for goal in goals:
            if goal.get("status") == "active":
                target_date = goal.get("target_completion_date")
                if target_date:
                    try:
                        target = datetime.fromisoformat(target_date.replace('Z', '+00:00'))
                        if target > datetime.now():
                            days_until = (target - datetime.now()).days
                            milestones.append({
                                "type": "goal",
                                "title": f"Goal: {goal.get('goal_type', 'Career Goal')}",
                                "due_date": target_date,
                                "days_until": days_until
                            })
                    except (ValueError, TypeError):
                        pass
        
        # Sort by due date
        milestones.sort(key=lambda x: x["days_until"])
        return milestones[:5]  # Return top 5 upcoming milestones
    
    def _generate_recommendations(self, progress: Dict, skills: List[Dict], goals: List[Dict], history: List[Dict]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Assessment recommendations
        days_since_last = None
        if progress.get("last_assessment_date"):
            try:
                last_date = datetime.fromisoformat(progress["last_assessment_date"].replace('Z', '+00:00'))
                days_since_last = (datetime.now() - last_date).days
            except (ValueError, TypeError):
                pass
        
        if not history or (days_since_last and days_since_last > 30):
            recommendations.append("Take a new assessment to track your progress")
        
        # Goal recommendations
        active_goals = [g for g in goals if g.get("status") == "active"]
        if not active_goals:
            recommendations.append("Set a career goal to start tracking your progress")
        elif len(active_goals) > 5:
            recommendations.append("Consider focusing on fewer goals for better results")
        
        # Skill recommendations
        if not skills:
            recommendations.append("Add skills you want to develop to track your progress")
        else:
            # Check for skills without recent practice
            for skill in skills:
                last_practice = skill.get("last_practice_date")
                if not last_practice:
                    recommendations.append(f"Start practicing {skill['skill_name']}")
                else:
                    try:
                        last_date = datetime.fromisoformat(last_practice.replace('Z', '+00:00'))
                        if (datetime.now() - last_date).days > 14:
                            recommendations.append(f"Resume practicing {skill['skill_name']}")
                    except (ValueError, TypeError):
                        pass
        
        # Streak recommendations
        current_streak = progress.get("current_streak_days", 0)
        if current_streak == 0:
            recommendations.append("Start building a daily learning streak")
        elif current_streak < 7:
            recommendations.append("Keep building your learning streak")
        
        return recommendations[:5]  # Return top 5 recommendations

# Create a singleton instance
progress_crud = ProgressCRUD()
