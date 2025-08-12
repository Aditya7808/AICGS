
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Load the trained model
model_artifacts = joblib.load('models/skill_gap_prioritizer.joblib')
model = model_artifacts['model']
le_skill = model_artifacts['le_skill']
le_career = model_artifacts['le_career']
feature_columns = model_artifacts['feature_columns']
all_skills = model_artifacts['all_skills']
skills_by_category = model_artifacts['skills_by_category']
careers = model_artifacts['careers']

class SkillGapAPI:
    def __init__(self, model, le_skill, le_career, feature_columns, all_skills):
        self.model = model
        self.le_skill = le_skill
        self.le_career = le_career
        self.feature_columns = feature_columns
        self.all_skills = all_skills
        
    def predict_skill_priorities(self, user_profile, target_career, top_k=10):
        """Predict skill priorities for a user"""
        
        current_skills = set(user_profile.get('current_skills', []))
        missing_skills = [skill for skill in self.all_skills if skill not in current_skills]
        
        if not missing_skills:
            return []
        
        feature_data = []
        
        for skill in missing_skills:
            # Calculate features
            skill_importance = self._calculate_skill_importance(skill, target_career)
            market_demand = np.random.uniform(0.5, 1.0)  # Replace with real market data
            learning_difficulty = 1 - user_profile.get('learning_capacity', 0.5)
            synergy_score = self._calculate_synergy(skill, current_skills)
            experience_factor = min(1.0, user_profile.get('experience_years', 0) / 10)
            academic_factor = user_profile.get('academic_score', 75) / 100
            learning_capacity = user_profile.get('learning_capacity', 0.5)
            
            # Encode categorical variables
            try:
                skill_encoded = self.le_skill.transform([skill])[0]
            except ValueError:
                continue  # Skip unknown skills
                
            try:
                career_encoded = self.le_career.transform([target_career])[0]
            except ValueError:
                career_encoded = 0
            
            feature_row = [
                skill_encoded, career_encoded, skill_importance, market_demand,
                learning_difficulty, synergy_score, experience_factor,
                academic_factor, learning_capacity
            ]
            
            feature_data.append((skill, feature_row))
        
        if not feature_data:
            return []
        
        # Make predictions
        skills_list = [item[0] for item in feature_data]
        features_list = [item[1] for item in feature_data]
        
        X_pred = pd.DataFrame(features_list, columns=self.feature_columns)
        predictions = self.model.predict(X_pred)
        
        # Combine and sort
        skill_priorities = list(zip(skills_list, predictions))
        skill_priorities.sort(key=lambda x: x[1], reverse=True)
        
        return skill_priorities[:top_k]
    
    def _calculate_skill_importance(self, skill, career):
        """Calculate skill importance for career"""
        # Career-skill importance mapping (would be in database in production)
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
            }
        }
        
        if career in importance_map and skill in importance_map[career]:
            return importance_map[career][skill]
        return 0.5  # Default importance
    
    def _calculate_synergy(self, skill, current_skills):
        """Calculate synergy with existing skills"""
        synergy = 0
        for existing_skill in current_skills:
            for category, skills_in_category in skills_by_category.items():
                if skill in skills_in_category and existing_skill in skills_in_category:
                    synergy += 0.2
        return min(1.0, synergy)

# Initialize the API
prioritizer_api = SkillGapAPI(model, le_skill, le_career, feature_columns, all_skills)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': True})

@app.route('/api/skills/available', methods=['GET'])
def get_available_skills():
    """Get all available skills by category"""
    return jsonify({
        'skills_by_category': skills_by_category,
        'all_skills': all_skills,
        'careers': careers
    })

@app.route('/api/skills/prioritize', methods=['POST'])
def prioritize_skills():
    """Prioritize skills for a user"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['target_career']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Extract user profile
        user_profile = {
            'current_skills': data.get('current_skills', []),
            'experience_years': data.get('experience_years', 0),
            'academic_score': data.get('academic_score', 75),
            'learning_capacity': data.get('learning_capacity', 0.5)
        }
        
        target_career = data['target_career']
        top_k = data.get('top_k', 10)
        
        # Get skill priorities
        priorities = prioritizer_api.predict_skill_priorities(
            user_profile, target_career, top_k
        )
        
        # Format response
        recommendations = []
        for skill, score in priorities:
            recommendations.append({
                'skill': skill,
                'priority_score': float(score),
                'category': next(
                    (cat for cat, skills in skills_by_category.items() if skill in skills),
                    'other'
                )
            })
        
        return jsonify({
            'user_profile': user_profile,
            'target_career': target_career,
            'recommendations': recommendations,
            'total_recommendations': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills/analyze-gap', methods=['POST'])
def analyze_skill_gap():
    """Analyze skill gaps for multiple careers"""
    try:
        data = request.json
        user_profile = data.get('user_profile', {})
        target_careers = data.get('target_careers', [])
        
        results = {}
        for career in target_careers:
            priorities = prioritizer_api.predict_skill_priorities(
                user_profile, career, top_k=5
            )
            results[career] = [
                {'skill': skill, 'priority_score': float(score)}
                for skill, score in priorities
            ]
        
        return jsonify({
            'user_profile': user_profile,
            'career_analysis': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
