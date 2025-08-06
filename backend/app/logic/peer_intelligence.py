from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from ..db.crud import (
    get_career_outcomes_by_profile, get_user_profile, get_careers,
    get_user_interactions, create_user_profile
)
from ..models.user import UserProfile
from ..models.career import Career
from ..models.interaction import CareerOutcome, UserInteraction
from .feature_engineering import FeatureEngineer
from .enhanced_matcher import safe_get_attr, safe_float
import numpy as np
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)

class PeerIntelligenceSystem:
    """Advanced peer intelligence system for career guidance"""
    
    def __init__(self):
        self.feature_engineer = FeatureEngineer()
    
    def find_similar_students(self, db: Session, user_profile: Dict[str, Any], 
                            limit: int = 50) -> List[Dict[str, Any]]:
        """Find students with similar academic and demographic profiles"""
        
        similar_students = []
        
        # Get career outcomes data (our training data represents students)
        outcomes = get_career_outcomes_by_profile(
            db,
            user_profile.get('education_level', ''),
            user_profile.get('residence_type', ''),
            user_profile.get('family_background', ''),
            safe_float(user_profile.get('current_marks_value', 0)) - 15  # Allow 15-point range
        )
        
        user_marks = safe_float(user_profile.get('current_marks_value', 0))
        user_interests = set(user_profile.get('interests', '').lower().split('|'))
        
        for outcome in outcomes:
            # Calculate similarity score
            similarity_score = self._calculate_student_similarity(user_profile, outcome)
            
            if similarity_score > 0.3:  # Minimum similarity threshold
                student_data = {
                    'student_id': f"outcome_{outcome.id}",
                    'similarity_score': similarity_score,
                    'education_level': safe_get_attr(outcome, 'education_level', ''),
                    'course_of_study': safe_get_attr(outcome, 'course_of_study', ''),
                    'institution': safe_get_attr(outcome, 'institution_type', ''),
                    'academic_performance': safe_float(safe_get_attr(outcome, 'marks_value', 0)),
                    'residence_type': safe_get_attr(outcome, 'residence_type', ''),
                    'family_background': safe_get_attr(outcome, 'family_background', ''),
                    'interests': safe_get_attr(outcome, 'interests', ''),
                    'career_path': safe_get_attr(outcome, 'next_path', ''),
                    'job_role': safe_get_attr(outcome, 'job_role', ''),
                    'company': safe_get_attr(outcome, 'company_name', ''),
                    'placement_status': safe_get_attr(outcome, 'placement_status', ''),
                    'next_course': safe_get_attr(outcome, 'next_course', ''),
                    'next_institution': safe_get_attr(outcome, 'next_institution', ''),
                    'is_successful': safe_get_attr(outcome, 'is_successful_outcome', False),
                    'match_reasons': self._get_similarity_reasons(user_profile, outcome)
                }
                similar_students.append(student_data)
        
        # Sort by similarity score
        similar_students.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similar_students[:limit]
    
    def _calculate_student_similarity(self, user_profile: Dict[str, Any], 
                                    student_outcome: CareerOutcome) -> float:
        """Calculate similarity between user and a student outcome"""
        
        similarity_factors = []
        
        # Academic performance similarity (40% weight)
        user_marks = safe_float(user_profile.get('current_marks_value', 0))
        student_marks = safe_float(safe_get_attr(student_outcome, 'marks_value', 0))
        
        if user_marks > 0 and student_marks > 0:
            marks_diff = abs(user_marks - student_marks)
            marks_similarity = max(0, 1 - (marks_diff / 50.0))  # Normalize to 0-1
            similarity_factors.append(('academic', marks_similarity, 0.4))
        
        # Education level similarity (20% weight)
        user_education = user_profile.get('education_level', '').lower()
        student_education = safe_get_attr(student_outcome, 'education_level', '').lower()
        education_similarity = 1.0 if user_education == student_education else 0.5
        similarity_factors.append(('education', education_similarity, 0.2))
        
        # Demographics similarity (20% weight)
        demo_similarity = 0.0
        if user_profile.get('residence_type', '') == safe_get_attr(student_outcome, 'residence_type', ''):
            demo_similarity += 0.5
        if user_profile.get('family_background', '') == safe_get_attr(student_outcome, 'family_background', ''):
            demo_similarity += 0.5
        similarity_factors.append(('demographics', demo_similarity, 0.2))
        
        # Interest similarity (20% weight)
        user_interests = set(user_profile.get('interests', '').lower().split('|'))
        student_interests = set(safe_get_attr(student_outcome, 'interests', '').lower().split('|'))
        
        if user_interests and student_interests:
            interest_overlap = len(user_interests.intersection(student_interests))
            interest_similarity = interest_overlap / max(len(user_interests), len(student_interests))
        else:
            interest_similarity = 0.5  # Neutral if no interest data
        
        similarity_factors.append(('interests', interest_similarity, 0.2))
        
        # Calculate weighted similarity
        total_similarity = sum(score * weight for _, score, weight in similarity_factors)
        return min(total_similarity, 1.0)
    
    def _get_similarity_reasons(self, user_profile: Dict[str, Any], 
                              student_outcome: CareerOutcome) -> List[str]:
        """Get reasons why this student is similar"""
        reasons = []
        
        # Academic similarity
        user_marks = safe_float(user_profile.get('current_marks_value', 0))
        student_marks = safe_float(safe_get_attr(student_outcome, 'marks_value', 0))
        if abs(user_marks - student_marks) <= 10:
            reasons.append(f"Similar academic performance ({student_marks:.1f}%)")
        
        # Education level
        if user_profile.get('education_level', '') == safe_get_attr(student_outcome, 'education_level', ''):
            reasons.append("Same education level")
        
        # Location
        if user_profile.get('residence_type', '') == safe_get_attr(student_outcome, 'residence_type', ''):
            reasons.append("Same residence type")
        
        # Family background
        if user_profile.get('family_background', '') == safe_get_attr(student_outcome, 'family_background', ''):
            reasons.append("Similar family background")
        
        # Interests
        user_interests = set(user_profile.get('interests', '').lower().split('|'))
        student_interests = set(safe_get_attr(student_outcome, 'interests', '').lower().split('|'))
        common_interests = user_interests.intersection(student_interests)
        if common_interests:
            reasons.append(f"Shared interests: {', '.join(list(common_interests)[:3])}")
        
        return reasons
    
    def get_success_stories(self, db: Session, user_profile: Dict[str, Any], 
                          career_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get success stories from similar students"""
        
        similar_students = self.find_similar_students(db, user_profile, limit=100)
        
        # Filter for successful outcomes
        success_stories = []
        for student in similar_students:
            if student['is_successful'] and student['career_path'] in ['Job', 'Higher Education']:
                
                # If specific career requested, filter for it
                if career_name and student['job_role']:
                    if career_name.lower() not in student['job_role'].lower():
                        continue
                
                story = {
                    'student_profile': {
                        'education_level': student['education_level'],
                        'academic_performance': student['academic_performance'],
                        'residence_type': student['residence_type'],
                        'family_background': student['family_background'],
                        'interests': student['interests']
                    },
                    'career_outcome': {
                        'path_type': student['career_path'],
                        'job_role': student['job_role'],
                        'company': student['company'],
                        'course': student['next_course'],
                        'institution': student['next_institution']
                    },
                    'similarity_score': student['similarity_score'],
                    'match_reasons': student['match_reasons'],
                    'success_factors': self._identify_success_factors(student),
                    'inspiration_message': self._generate_inspiration_message(student, user_profile)
                }
                success_stories.append(story)
        
        # Sort by similarity and return top stories
        success_stories.sort(key=lambda x: x['similarity_score'], reverse=True)
        return success_stories[:10]
    
    def _identify_success_factors(self, student_data: Dict[str, Any]) -> List[str]:
        """Identify factors that contributed to student's success"""
        factors = []
        
        if student_data['academic_performance'] > 80:
            factors.append("Strong academic performance")
        
        if student_data['company'] and 'IIT' in student_data.get('institution', ''):
            factors.append("Premier institution background")
        
        if student_data['job_role'] and any(term in student_data['job_role'].lower() 
                                          for term in ['engineer', 'developer', 'analyst']):
            factors.append("Technical skills focus")
        
        if student_data['family_background'] == 'Lower Income' and student_data['is_successful']:
            factors.append("Overcame economic challenges")
        
        return factors
    
    def _generate_inspiration_message(self, student_data: Dict[str, Any], 
                                    user_profile: Dict[str, Any]) -> str:
        """Generate inspirational message based on student success"""
        
        if student_data['career_path'] == 'Job':
            return f"A student with similar background ({student_data['academic_performance']:.1f}% marks) successfully got placed as {student_data['job_role']} at {student_data['company']}"
        elif student_data['career_path'] == 'Higher Education':
            return f"A similar student gained admission to {student_data['next_course']} at {student_data['next_institution']}"
        else:
            return "Similar students have found success in their chosen paths"
    
    def get_popular_choices_among_peers(self, db: Session, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get popular career choices among similar students"""
        
        similar_students = self.find_similar_students(db, user_profile, limit=200)
        
        # Count career choices
        career_counts = Counter()
        career_details = defaultdict(lambda: {
            'students': [],
            'success_rate': 0,
            'companies': set(),
            'avg_performance': 0
        })
        
        for student in similar_students:
            if student['job_role'] and student['career_path'] == 'Job':
                career_name = student['job_role']
                career_counts[career_name] += 1
                
                career_details[career_name]['students'].append(student)
                if student['company']:
                    career_details[career_name]['companies'].add(student['company'])
        
        # Calculate statistics for each popular career
        popular_careers = []
        for career_name, count in career_counts.most_common(10):
            students = career_details[career_name]['students']
            success_count = sum(1 for s in students if s['is_successful'])
            success_rate = success_count / len(students) if students else 0
            
            avg_performance = sum(s['academic_performance'] for s in students) / len(students)
            
            popular_career = {
                'career_name': career_name,
                'popularity_count': count,
                'popularity_percentage': (count / len(similar_students)) * 100,
                'success_rate': success_rate,
                'avg_academic_performance': avg_performance,
                'top_companies': list(career_details[career_name]['companies'])[:5],
                'sample_students': len(students),
                'recommendation_strength': self._calculate_recommendation_strength(
                    count, success_rate, avg_performance
                )
            }
            popular_careers.append(popular_career)
        
        return popular_careers
    
    def _calculate_recommendation_strength(self, popularity_count: int, 
                                         success_rate: float, avg_performance: float) -> str:
        """Calculate recommendation strength based on peer data"""
        
        if popularity_count >= 5 and success_rate >= 0.8 and avg_performance >= 75:
            return "Highly Recommended"
        elif popularity_count >= 3 and success_rate >= 0.6:
            return "Recommended"
        elif popularity_count >= 2:
            return "Consider"
        else:
            return "Limited Data"
    
    def get_peer_comparison(self, db: Session, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed peer comparison and positioning"""
        
        similar_students = self.find_similar_students(db, user_profile, limit=100)
        
        if not similar_students:
            return {"error": "No similar students found for comparison"}
        
        user_marks = safe_float(user_profile.get('current_marks_value', 0))
        
        # Academic positioning
        better_performers = [s for s in similar_students if s['academic_performance'] > user_marks]
        same_performers = [s for s in similar_students if abs(s['academic_performance'] - user_marks) <= 2]
        
        # Career path analysis
        job_seekers = [s for s in similar_students if s['career_path'] == 'Job']
        higher_ed_seekers = [s for s in similar_students if s['career_path'] == 'Higher Education']
        
        # Success analysis
        successful_students = [s for s in similar_students if s['is_successful']]
        
        comparison = {
            'total_similar_students': len(similar_students),
            'academic_positioning': {
                'percentile': ((len(similar_students) - len(better_performers)) / len(similar_students)) * 100,
                'better_performers': len(better_performers),
                'similar_performers': len(same_performers),
                'your_performance': user_marks
            },
            'career_path_distribution': {
                'job_seekers': len(job_seekers),
                'higher_education_seekers': len(higher_ed_seekers),
                'job_percentage': (len(job_seekers) / len(similar_students)) * 100,
                'higher_ed_percentage': (len(higher_ed_seekers) / len(similar_students)) * 100
            },
            'success_metrics': {
                'successful_students': len(successful_students),
                'success_rate': (len(successful_students) / len(similar_students)) * 100,
                'avg_successful_performance': sum(s['academic_performance'] for s in successful_students) / len(successful_students) if successful_students else 0
            },
            'insights': self._generate_peer_insights(similar_students, user_profile)
        }
        
        return comparison
    
    def _generate_peer_insights(self, similar_students: List[Dict[str, Any]], 
                              user_profile: Dict[str, Any]) -> List[str]:
        """Generate insights based on peer analysis"""
        insights = []
        
        user_marks = safe_float(user_profile.get('current_marks_value', 0))
        successful_students = [s for s in similar_students if s['is_successful']]
        
        if successful_students:
            avg_successful_marks = sum(s['academic_performance'] for s in successful_students) / len(successful_students)
            
            if user_marks >= avg_successful_marks:
                insights.append(f"Your performance ({user_marks:.1f}%) is above the average of successful similar students ({avg_successful_marks:.1f}%)")
            else:
                insights.append(f"Consider improving performance - successful similar students average {avg_successful_marks:.1f}%")
        
        # Most common career paths
        job_roles = [s['job_role'] for s in similar_students if s['job_role'] and s['is_successful']]
        if job_roles:
            most_common_role = Counter(job_roles).most_common(1)[0]
            insights.append(f"Most successful career choice among peers: {most_common_role[0]} ({most_common_role[1]} students)")
        
        # Background-specific insights
        family_bg = user_profile.get('family_background', '')
        same_bg_students = [s for s in successful_students if s['family_background'] == family_bg]
        if same_bg_students:
            insights.append(f"{len(same_bg_students)} students from {family_bg} background have succeeded in similar paths")
        
        return insights

def get_peer_intelligence_report(db: Session, user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive peer intelligence report"""
    
    peer_system = PeerIntelligenceSystem()
    
    # Get all peer intelligence data
    similar_students = peer_system.find_similar_students(db, user_profile, limit=50)
    success_stories = peer_system.get_success_stories(db, user_profile)
    popular_choices = peer_system.get_popular_choices_among_peers(db, user_profile)
    peer_comparison = peer_system.get_peer_comparison(db, user_profile)
    
    report = {
        'report_type': 'peer_intelligence',
        'user_profile_summary': {
            'education_level': user_profile.get('education_level', ''),
            'academic_performance': user_profile.get('current_marks_value', 0),
            'residence_type': user_profile.get('residence_type', ''),
            'family_background': user_profile.get('family_background', ''),
            'interests': user_profile.get('interests', '')
        },
        'similar_students_found': len(similar_students),
        'success_stories': success_stories,
        'popular_career_choices': popular_choices,
        'peer_comparison': peer_comparison,
        'key_insights': {
            'top_recommendation': popular_choices[0] if popular_choices else None,
            'success_rate_peers': peer_comparison.get('success_metrics', {}).get('success_rate', 0),
            'most_common_path': 'Job' if len([s for s in similar_students if s['career_path'] == 'Job']) > len([s for s in similar_students if s['career_path'] == 'Higher Education']) else 'Higher Education'
        },
        'generated_at': f"{type(peer_system).__name__} Analysis"
    }
    
    return report
