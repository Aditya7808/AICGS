from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from ..db.crud import get_careers, get_career_outcomes_by_profile
from ..models.career import Career
from ..models.interaction import CareerOutcome
from .enhanced_matcher import safe_get_attr, safe_float
import json
import logging

logger = logging.getLogger(__name__)

class SkillGapAnalyzer:
    """Analyze skill gaps and suggest learning pathways"""
    
    def __init__(self):
        # Industry skill requirements database (in production, this would be a proper database)
        self.industry_skills = {
            'Software Developer': {
                'core_skills': ['Programming', 'Problem Solving', 'Data Structures', 'Algorithms'],
                'technical_skills': ['Python', 'JavaScript', 'Git', 'Database', 'Web Development'],
                'soft_skills': ['Communication', 'Teamwork', 'Time Management'],
                'advanced_skills': ['System Design', 'Cloud Computing', 'DevOps', 'AI/ML'],
                'skill_levels': {
                    'beginner': ['Programming', 'Problem Solving'],
                    'intermediate': ['Data Structures', 'Web Development', 'Database'],
                    'advanced': ['System Design', 'Cloud Computing', 'AI/ML']
                }
            },
            'Data Analyst': {
                'core_skills': ['Statistics', 'Data Analysis', 'Critical Thinking'],
                'technical_skills': ['Excel', 'SQL', 'Python', 'R', 'Tableau', 'Power BI'],
                'soft_skills': ['Communication', 'Presentation', 'Business Acumen'],
                'advanced_skills': ['Machine Learning', 'Big Data', 'Data Engineering'],
                'skill_levels': {
                    'beginner': ['Excel', 'Statistics', 'SQL'],
                    'intermediate': ['Python', 'Tableau', 'Data Analysis'],
                    'advanced': ['Machine Learning', 'Big Data', 'Data Engineering']
                }
            },
            'UI/UX Designer': {
                'core_skills': ['Design Thinking', 'User Research', 'Prototyping'],
                'technical_skills': ['Figma', 'Adobe Creative Suite', 'Sketch', 'HTML/CSS'],
                'soft_skills': ['Creativity', 'Empathy', 'Communication'],
                'advanced_skills': ['User Testing', 'Design Systems', 'Frontend Development'],
                'skill_levels': {
                    'beginner': ['Design Thinking', 'Figma', 'User Research'],
                    'intermediate': ['Prototyping', 'Adobe Creative Suite', 'HTML/CSS'],
                    'advanced': ['Design Systems', 'User Testing', 'Frontend Development']
                }
            },
            'Digital Marketing Specialist': {
                'core_skills': ['Marketing Strategy', 'Content Creation', 'Analytics'],
                'technical_skills': ['Google Analytics', 'Social Media', 'SEO', 'PPC', 'Email Marketing'],
                'soft_skills': ['Communication', 'Creativity', 'Analysis'],
                'advanced_skills': ['Marketing Automation', 'Conversion Optimization', 'Data-Driven Marketing'],
                'skill_levels': {
                    'beginner': ['Social Media', 'Content Creation', 'SEO'],
                    'intermediate': ['Google Analytics', 'PPC', 'Email Marketing'],
                    'advanced': ['Marketing Automation', 'Conversion Optimization']
                }
            },
            'Financial Analyst': {
                'core_skills': ['Financial Analysis', 'Accounting', 'Excel'],
                'technical_skills': ['Financial Modeling', 'Valuation', 'Risk Assessment', 'Bloomberg'],
                'soft_skills': ['Attention to Detail', 'Communication', 'Critical Thinking'],
                'advanced_skills': ['Investment Banking', 'Portfolio Management', 'Derivatives'],
                'skill_levels': {
                    'beginner': ['Excel', 'Financial Analysis', 'Accounting'],
                    'intermediate': ['Financial Modeling', 'Valuation', 'Risk Assessment'],
                    'advanced': ['Investment Banking', 'Portfolio Management', 'Derivatives']
                }
            }
        }
        
        # Learning resources database
        self.learning_resources = {
            'Programming': [
                {'name': 'Python for Beginners', 'type': 'course', 'provider': 'Coursera', 'duration': '6 weeks', 'level': 'beginner'},
                {'name': 'Data Structures and Algorithms', 'type': 'course', 'provider': 'edX', 'duration': '8 weeks', 'level': 'intermediate'}
            ],
            'Data Analysis': [
                {'name': 'Data Analysis with Python', 'type': 'course', 'provider': 'Coursera', 'duration': '5 weeks', 'level': 'intermediate'},
                {'name': 'Excel for Data Analysis', 'type': 'course', 'provider': 'Udemy', 'duration': '3 weeks', 'level': 'beginner'}
            ],
            'Web Development': [
                {'name': 'Full Stack Web Development', 'type': 'bootcamp', 'provider': 'Local Bootcamp', 'duration': '12 weeks', 'level': 'intermediate'},
                {'name': 'HTML/CSS Basics', 'type': 'course', 'provider': 'FreeCodeCamp', 'duration': '2 weeks', 'level': 'beginner'}
            ],
            'Digital Marketing': [
                {'name': 'Google Digital Marketing Course', 'type': 'certification', 'provider': 'Google Skillshop', 'duration': '4 weeks', 'level': 'beginner'},
                {'name': 'Advanced SEO Strategies', 'type': 'course', 'provider': 'Udemy', 'duration': '6 weeks', 'level': 'advanced'}
            ],
            'Design': [
                {'name': 'UI/UX Design Fundamentals', 'type': 'course', 'provider': 'Coursera', 'duration': '8 weeks', 'level': 'beginner'},
                {'name': 'Advanced Figma Techniques', 'type': 'workshop', 'provider': 'Design Academy', 'duration': '2 weeks', 'level': 'intermediate'}
            ]
        }
    
    def analyze_skill_gaps(self, user_skills: List[str], target_career: str) -> Dict[str, Any]:
        """Analyze skill gaps for a target career"""
        
        # Normalize user skills
        user_skills_set = set(skill.lower().strip() for skill in user_skills if skill.strip())
        
        # Get career skill requirements
        career_requirements = self.industry_skills.get(target_career, {})
        
        if not career_requirements:
            # If career not in our database, try to match with similar careers
            career_requirements = self._find_similar_career_skills(target_career)
        
        if not career_requirements:
            return {
                'error': f'Skill requirements not found for {target_career}',
                'suggestion': 'Please choose from available career options'
            }
        
        # Analyze each skill category
        gap_analysis = {}
        
        for category, required_skills in career_requirements.items():
            if category == 'skill_levels':
                continue
                
            if isinstance(required_skills, list):
                required_set = set(skill.lower().strip() for skill in required_skills)
                
                # Find what user has vs what's required
                user_has = user_skills_set.intersection(required_set)
                missing_skills = required_set - user_skills_set
                
                gap_analysis[category] = {
                    'required_skills': required_skills,
                    'user_has': list(user_has),
                    'missing_skills': list(missing_skills),
                    'completion_percentage': (len(user_has) / len(required_set)) * 100 if required_set else 100,
                    'priority_level': self._get_priority_level(category)
                }
        
        # Generate overall analysis
        overall_gaps = self._calculate_overall_gaps(gap_analysis)
        learning_roadmap = self._generate_learning_roadmap(gap_analysis, career_requirements)
        time_estimates = self._estimate_learning_time(gap_analysis)
        
        return {
            'target_career': target_career,
            'user_skills': user_skills,
            'gap_analysis': gap_analysis,
            'overall_assessment': overall_gaps,
            'learning_roadmap': learning_roadmap,
            'time_estimates': time_estimates,
            'readiness_score': self._calculate_readiness_score(gap_analysis),
            'recommendations': self._generate_recommendations(gap_analysis, overall_gaps)
        }
    
    def _find_similar_career_skills(self, career_name: str) -> Dict[str, Any]:
        """Find skill requirements for similar careers"""
        career_lower = career_name.lower()
        
        # Simple keyword matching
        if 'developer' in career_lower or 'programmer' in career_lower:
            return self.industry_skills.get('Software Developer', {})
        elif 'analyst' in career_lower and 'data' in career_lower:
            return self.industry_skills.get('Data Analyst', {})
        elif 'design' in career_lower or 'ui' in career_lower or 'ux' in career_lower:
            return self.industry_skills.get('UI/UX Designer', {})
        elif 'marketing' in career_lower:
            return self.industry_skills.get('Digital Marketing Specialist', {})
        elif 'financial' in career_lower or 'finance' in career_lower:
            return self.industry_skills.get('Financial Analyst', {})
        
        return {}
    
    def _get_priority_level(self, category: str) -> str:
        """Get priority level for skill category"""
        priority_map = {
            'core_skills': 'High',
            'technical_skills': 'High',
            'soft_skills': 'Medium',
            'advanced_skills': 'Low'
        }
        return priority_map.get(category, 'Medium')
    
    def _calculate_overall_gaps(self, gap_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall skill gap assessment"""
        
        total_required = 0
        total_missing = 0
        high_priority_missing = 0
        
        for category, analysis in gap_analysis.items():
            total_required += len(analysis['required_skills'])
            total_missing += len(analysis['missing_skills'])
            
            if analysis['priority_level'] == 'High':
                high_priority_missing += len(analysis['missing_skills'])
        
        overall_completion = ((total_required - total_missing) / total_required) * 100 if total_required > 0 else 100
        
        return {
            'total_skills_required': total_required,
            'total_skills_missing': total_missing,
            'high_priority_missing': high_priority_missing,
            'overall_completion_percentage': overall_completion,
            'readiness_level': self._get_readiness_level(overall_completion, high_priority_missing)
        }
    
    def _get_readiness_level(self, completion_percentage: float, high_priority_missing: int) -> str:
        """Determine readiness level for the career"""
        
        if completion_percentage >= 80 and high_priority_missing <= 1:
            return 'Ready'
        elif completion_percentage >= 60 and high_priority_missing <= 3:
            return 'Nearly Ready'
        elif completion_percentage >= 40:
            return 'Developing'
        else:
            return 'Beginner'
    
    def _generate_learning_roadmap(self, gap_analysis: Dict[str, Any], 
                                 career_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate a structured learning roadmap"""
        
        roadmap = []
        skill_levels = career_requirements.get('skill_levels', {})
        
        # Phase 1: Beginner skills
        beginner_missing = []
        for skill in skill_levels.get('beginner', []):
            for category, analysis in gap_analysis.items():
                if skill.lower() in [s.lower() for s in analysis['missing_skills']]:
                    beginner_missing.append(skill)
                    break
        
        if beginner_missing:
            roadmap.append({
                'phase': 1,
                'title': 'Foundation Skills',
                'duration': '1-3 months',
                'skills_to_learn': beginner_missing,
                'description': 'Build fundamental skills required for the career',
                'resources': self._get_learning_resources(beginner_missing, 'beginner')
            })
        
        # Phase 2: Intermediate skills
        intermediate_missing = []
        for skill in skill_levels.get('intermediate', []):
            for category, analysis in gap_analysis.items():
                if skill.lower() in [s.lower() for s in analysis['missing_skills']]:
                    intermediate_missing.append(skill)
                    break
        
        if intermediate_missing:
            roadmap.append({
                'phase': 2,
                'title': 'Core Professional Skills',
                'duration': '3-6 months',
                'skills_to_learn': intermediate_missing,
                'description': 'Develop core professional skills for the role',
                'resources': self._get_learning_resources(intermediate_missing, 'intermediate')
            })
        
        # Phase 3: Advanced skills
        advanced_missing = []
        for skill in skill_levels.get('advanced', []):
            for category, analysis in gap_analysis.items():
                if skill.lower() in [s.lower() for s in analysis['missing_skills']]:
                    advanced_missing.append(skill)
                    break
        
        if advanced_missing:
            roadmap.append({
                'phase': 3,
                'title': 'Advanced Specialization',
                'duration': '6-12 months',
                'skills_to_learn': advanced_missing,
                'description': 'Master advanced skills for career growth',
                'resources': self._get_learning_resources(advanced_missing, 'advanced')
            })
        
        return roadmap
    
    def _get_learning_resources(self, skills: List[str], level: str) -> List[Dict[str, Any]]:
        """Get learning resources for specific skills"""
        
        resources = []
        
        for skill in skills:
            # Find resources for this skill
            skill_resources = []
            
            # Direct skill match
            if skill in self.learning_resources:
                skill_resources = self.learning_resources[skill]
            else:
                # Fuzzy matching
                for resource_skill, resource_list in self.learning_resources.items():
                    if skill.lower() in resource_skill.lower() or resource_skill.lower() in skill.lower():
                        skill_resources = resource_list
                        break
            
            # Filter by level if specified
            if skill_resources:
                filtered_resources = [r for r in skill_resources if r.get('level', 'beginner') == level]
                if not filtered_resources:
                    filtered_resources = skill_resources[:1]  # Take first available
                
                resources.extend(filtered_resources)
        
        # Remove duplicates and limit to top 5
        seen_names = set()
        unique_resources = []
        for resource in resources:
            if resource['name'] not in seen_names:
                unique_resources.append(resource)
                seen_names.add(resource['name'])
                
                if len(unique_resources) >= 5:
                    break
        
        return unique_resources
    
    def _estimate_learning_time(self, gap_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate time required to fill skill gaps"""
        
        # Rough time estimates per skill category
        time_estimates = {
            'core_skills': 2,      # weeks per skill
            'technical_skills': 3,  # weeks per skill
            'soft_skills': 1,      # weeks per skill
            'advanced_skills': 4   # weeks per skill
        }
        
        total_weeks = 0
        category_times = {}
        
        for category, analysis in gap_analysis.items():
            missing_count = len(analysis['missing_skills'])
            weeks_per_skill = time_estimates.get(category, 2)
            category_time = missing_count * weeks_per_skill
            
            category_times[category] = {
                'missing_skills_count': missing_count,
                'estimated_weeks': category_time,
                'estimated_months': round(category_time / 4, 1)
            }
            
            total_weeks += category_time
        
        return {
            'total_estimated_weeks': total_weeks,
            'total_estimated_months': round(total_weeks / 4, 1),
            'category_breakdown': category_times,
            'recommended_schedule': self._generate_study_schedule(total_weeks)
        }
    
    def _generate_study_schedule(self, total_weeks: int) -> Dict[str, Any]:
        """Generate recommended study schedule"""
        
        if total_weeks <= 12:  # 3 months
            intensity = 'Intensive'
            hours_per_week = 15
            description = 'Full-time learning approach for quick transition'
        elif total_weeks <= 24:  # 6 months
            intensity = 'Moderate'
            hours_per_week = 10
            description = 'Balanced approach with part-time learning'
        else:
            intensity = 'Gradual'
            hours_per_week = 5
            description = 'Gradual learning while working or studying'
        
        return {
            'intensity': intensity,
            'recommended_hours_per_week': hours_per_week,
            'description': description,
            'daily_commitment': f"{round(hours_per_week / 7, 1)} hours per day"
        }
    
    def _calculate_readiness_score(self, gap_analysis: Dict[str, Any]) -> float:
        """Calculate overall readiness score (0-100)"""
        
        weights = {
            'core_skills': 0.4,
            'technical_skills': 0.35,
            'soft_skills': 0.15,
            'advanced_skills': 0.1
        }
        
        weighted_score = 0
        total_weight = 0
        
        for category, analysis in gap_analysis.items():
            if category in weights:
                completion = analysis['completion_percentage']
                weight = weights[category]
                weighted_score += completion * weight
                total_weight += weight
        
        return round(weighted_score / total_weight if total_weight > 0 else 0, 1)
    
    def _generate_recommendations(self, gap_analysis: Dict[str, Any], 
                                overall_gaps: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        readiness_level = overall_gaps['readiness_level']
        
        if readiness_level == 'Ready':
            recommendations.append("You're ready to apply for this career! Focus on building a strong portfolio.")
            recommendations.append("Consider applying for internships or entry-level positions.")
        elif readiness_level == 'Nearly Ready':
            recommendations.append("You're close to being ready! Focus on the missing high-priority skills.")
            recommendations.append("Start building projects to demonstrate your skills.")
        elif readiness_level == 'Developing':
            recommendations.append("Focus on building core and technical skills first.")
            recommendations.append("Consider taking structured courses or bootcamps.")
        else:
            recommendations.append("Start with foundation skills and basic concepts.")
            recommendations.append("Consider formal education or comprehensive training programs.")
        
        # Specific skill recommendations
        high_priority_missing = []
        for category, analysis in gap_analysis.items():
            if analysis['priority_level'] == 'High' and analysis['missing_skills']:
                high_priority_missing.extend(analysis['missing_skills'])
        
        if high_priority_missing:
            recommendations.append(f"Prioritize learning: {', '.join(high_priority_missing[:3])}")
        
        return recommendations

def analyze_user_skill_gaps(db: Session, user_profile: Dict[str, Any], 
                          target_careers: List[str]) -> Dict[str, Any]:
    """Analyze skill gaps for multiple target careers"""
    
    analyzer = SkillGapAnalyzer()
    
    # Get user skills from profile
    user_skills = []
    if user_profile.get('skills'):
        user_skills = [skill.strip() for skill in user_profile['skills'].split('|') if skill.strip()]
    
    # Add interests as potential skills
    if user_profile.get('interests'):
        interests = [interest.strip() for interest in user_profile['interests'].split('|') if interest.strip()]
        user_skills.extend(interests)
    
    # Analyze gaps for each target career
    career_analyses = {}
    
    for career in target_careers:
        analysis = analyzer.analyze_skill_gaps(user_skills, career)
        career_analyses[career] = analysis
    
    # Find the most suitable career based on readiness
    best_match = None
    highest_readiness = 0
    
    for career, analysis in career_analyses.items():
        if 'readiness_score' in analysis:
            readiness = analysis['readiness_score']
            if readiness > highest_readiness:
                highest_readiness = readiness
                best_match = career
    
    return {
        'user_skills': user_skills,
        'career_analyses': career_analyses,
        'best_match_career': best_match,
        'overall_recommendations': _generate_overall_recommendations(career_analyses),
        'skill_development_priority': _identify_skill_priorities(career_analyses)
    }

def _generate_overall_recommendations(career_analyses: Dict[str, Any]) -> List[str]:
    """Generate overall recommendations across all careers"""
    
    recommendations = []
    
    # Find common missing skills across careers
    all_missing_skills = []
    for career, analysis in career_analyses.items():
        if 'gap_analysis' in analysis:
            for category, gap_data in analysis['gap_analysis'].items():
                all_missing_skills.extend(gap_data.get('missing_skills', []))
    
    # Find most common missing skills
    from collections import Counter
    skill_counts = Counter(all_missing_skills)
    common_missing = skill_counts.most_common(5)
    
    if common_missing:
        recommendations.append(f"Focus on skills needed across multiple careers: {', '.join([skill for skill, count in common_missing])}")
    
    # Find the most achievable career
    ready_careers = []
    for career, analysis in career_analyses.items():
        if analysis.get('readiness_score', 0) >= 70:
            ready_careers.append(career)
    
    if ready_careers:
        recommendations.append(f"You're nearly ready for: {', '.join(ready_careers)}")
    
    return recommendations

def _identify_skill_priorities(career_analyses: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify priority skills to learn"""
    
    skill_priorities = []
    
    # Aggregate skills by frequency and importance
    skill_importance = {}
    
    for career, analysis in career_analyses.items():
        if 'gap_analysis' in analysis:
            for category, gap_data in analysis['gap_analysis'].items():
                priority = gap_data.get('priority_level', 'Medium')
                weight = {'High': 3, 'Medium': 2, 'Low': 1}.get(priority, 2)
                
                for skill in gap_data.get('missing_skills', []):
                    if skill not in skill_importance:
                        skill_importance[skill] = {'weight': 0, 'careers': [], 'priority': priority}
                    skill_importance[skill]['weight'] += weight
                    skill_importance[skill]['careers'].append(career)
    
    # Sort by importance and create priority list
    sorted_skills = sorted(skill_importance.items(), key=lambda x: x[1]['weight'], reverse=True)
    
    for skill, data in sorted_skills[:10]:  # Top 10 priority skills
        skill_priorities.append({
            'skill': skill,
            'importance_score': data['weight'],
            'relevant_careers': data['careers'],
            'priority_level': data['priority']
        })
    
    return skill_priorities
