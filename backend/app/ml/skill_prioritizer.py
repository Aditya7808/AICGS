"""
Smart Skill Gap Prioritizer for CareerBuddy
Integrates trained LightGBM model for skill prioritization
"""

import joblib
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
import os
from pathlib import Path

class SkillGapPrioritizer:
    """Smart Skill Gap Prioritizer for career guidance"""
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize the prioritizer"""
        self.model = None
        self.le_skill = None
        self.le_career = None
        self.feature_columns = None
        self.all_skills = None
        self.skills_by_category = None
        self.careers = None
        
        if model_path:
            self.load_model(model_path)
    
    @classmethod
    def load_default_model(cls):
        """Load the default trained model"""
        current_dir = Path(__file__).parent
        model_path = current_dir / "models" / "skill_gap_prioritizer.joblib"
        return cls(str(model_path))
    
    def load_model(self, model_path: str):
        """Load trained model from file"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        model_artifacts = joblib.load(model_path)
        
        self.model = model_artifacts['model']
        self.le_skill = model_artifacts['le_skill']
        self.le_career = model_artifacts['le_career']
        self.feature_columns = model_artifacts['feature_columns']
        self.all_skills = model_artifacts['all_skills']
        self.skills_by_category = model_artifacts['skills_by_category']
        self.careers = model_artifacts['careers']
        
        print(f"Model loaded successfully from {model_path}")
    
    def predict_skill_priorities(
        self, 
        user_profile: Dict, 
        target_career: str, 
        top_k: int = 10
    ) -> List[Dict]:
        """
        Predict skill priorities for a user
        
        Args:
            user_profile: Dict with user information
            target_career: Target career string
            top_k: Number of top skills to return
            
        Returns:
            List of skill recommendations with priority scores
        """
        if not self.model:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Extract user features
        current_skills = set(user_profile.get('current_skills', []))
        missing_skills = [skill for skill in self.all_skills if skill not in current_skills]
        
        if not missing_skills:
            return []
        
        # Prepare feature matrix for missing skills
        feature_data = []
        skill_names = []
        
        for skill in missing_skills:
            # Calculate features (same as in training)
            skill_importance = self._calculate_skill_importance(skill, target_career)
            market_demand = np.random.uniform(0.5, 1.0)  # Replace with real market data in production
            learning_difficulty = 1 - user_profile.get('learning_capacity', 0.5)
            synergy_score = self._calculate_synergy(skill, current_skills)
            experience_factor = min(1.0, user_profile.get('experience_years', 0) / 10)
            academic_factor = user_profile.get('academic_score', 75) / 100
            learning_capacity = user_profile.get('learning_capacity', 0.5)
            
            # Encode categorical variables
            try:
                skill_encoded = self.le_skill.transform([skill])[0]
            except ValueError:
                # Skip unknown skills
                continue
                
            try:
                career_encoded = self.le_career.transform([target_career])[0]
            except ValueError:
                career_encoded = 0  # Default to first career
            
            feature_row = [
                skill_encoded, career_encoded, skill_importance, market_demand,
                learning_difficulty, synergy_score, experience_factor,
                academic_factor, learning_capacity
            ]
            
            feature_data.append(feature_row)
            skill_names.append(skill)
        
        if not feature_data:
            return []
        
        # Make predictions
        X_pred = pd.DataFrame(feature_data, columns=self.feature_columns)
        predictions = self.model.predict(X_pred)
        
        # Combine skills with predictions and sort
        skill_priorities = list(zip(skill_names, predictions))
        skill_priorities.sort(key=lambda x: x[1], reverse=True)
        
        # Format response
        recommendations = []
        for skill, score in skill_priorities[:top_k]:
            category = self._get_skill_category(skill)
            recommendations.append({
                'skill': skill,
                'priority_score': float(score),
                'category': category,
                'importance': self._calculate_skill_importance(skill, target_career),
                'learning_effort': self._estimate_learning_effort(skill, user_profile)
            })
        
        return recommendations
    
    def analyze_multiple_careers(
        self, 
        user_profile: Dict, 
        target_careers: List[str], 
        top_k: int = 5
    ) -> Dict[str, List[Dict]]:
        """Analyze skill gaps for multiple careers"""
        results = {}
        
        for career in target_careers:
            if career in self.careers:
                priorities = self.predict_skill_priorities(user_profile, career, top_k)
                results[career] = priorities
        
        return results
    
    def get_available_skills(self) -> Dict:
        """Get all available skills and careers"""
        return {
            'skills_by_category': self.skills_by_category,
            'all_skills': self.all_skills,
            'careers': self.careers
        }
    
    def _calculate_skill_importance(self, skill: str, career: str) -> float:
        """Calculate skill importance for career (would be in database in production)"""
        importance_map = {
            'Software Engineer': {
                'Python': 0.9, 'JavaScript': 0.8, 'Java': 0.7, 'Git': 0.9,
                'React': 0.7, 'Node.js': 0.6, 'SQL': 0.6, 'Docker': 0.5
            },
            'Data Scientist': {
                'Python': 0.95, 'Statistics': 0.95, 'Machine Learning': 0.9,
                'SQL': 0.8, 'Pandas': 0.9, 'NumPy': 0.85, 'Data Visualization': 0.8
            },
            'UI/UX Designer': {
                'Figma': 0.9, 'UI/UX Design': 0.95, 'Prototyping': 0.8,
                'User Research': 0.85, 'Photoshop': 0.7
            },
            'Digital Marketing Manager': {
                'Digital Marketing': 0.95, 'SEO': 0.8, 'Google Analytics': 0.8,
                'Social Media': 0.7, 'Content Marketing': 0.75
            }
        }
        
        if career in importance_map and skill in importance_map[career]:
            return importance_map[career][skill]
        return 0.5  # Default importance
    
    def _calculate_synergy(self, skill: str, current_skills: set) -> float:
        """Calculate synergy with existing skills"""
        synergy = 0
        for existing_skill in current_skills:
            for category, skills_in_category in self.skills_by_category.items():
                if skill in skills_in_category and existing_skill in skills_in_category:
                    synergy += 0.2
        return min(1.0, synergy)
    
    def _get_skill_category(self, skill: str) -> str:
        """Get category for a skill"""
        for category, skills in self.skills_by_category.items():
            if skill in skills:
                return category
        return 'other'
    
    def _estimate_learning_effort(self, skill: str, user_profile: Dict) -> str:
        """Estimate learning effort for a skill"""
        base_difficulty = {
            'Python': 'Medium', 'JavaScript': 'Medium', 'Statistics': 'High',
            'Machine Learning': 'High', 'SQL': 'Low', 'Excel': 'Low',
            'Figma': 'Low', 'Photoshop': 'Medium'
        }
        
        difficulty = base_difficulty.get(skill, 'Medium')
        
        # Adjust based on user's learning capacity and experience
        learning_capacity = user_profile.get('learning_capacity', 0.5)
        experience_years = user_profile.get('experience_years', 0)
        
        if learning_capacity > 0.7 or experience_years > 5:
            if difficulty == 'High':
                difficulty = 'Medium'
            elif difficulty == 'Medium':
                difficulty = 'Low'
        
        return difficulty

# Global instance for easy access
skill_prioritizer = None

def get_skill_prioritizer():
    """Get global skill prioritizer instance"""
    global skill_prioritizer
    if skill_prioritizer is None:
        skill_prioritizer = SkillGapPrioritizer.load_default_model()
    return skill_prioritizer
