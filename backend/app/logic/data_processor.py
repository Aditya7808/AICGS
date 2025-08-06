import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from ..db.base import SessionLocal
from ..models.interaction import CareerOutcome
from ..models.career import Career
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Process and load training data from CSV"""
    
    def __init__(self, csv_path: str = "data.csv"):
        self.csv_path = csv_path
        self.df = None
        
    def load_csv_data(self) -> pd.DataFrame:
        """Load and clean CSV data"""
        try:
            self.df = pd.read_csv(self.csv_path)
            logger.info(f"Loaded {len(self.df)} records from {self.csv_path}")
            return self.df
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        """Clean and standardize the data"""
        if self.df is None:
            self.load_csv_data()
        
        # Handle missing values
        self.df['interests'] = self.df['interests'].fillna('')
        self.df['current_marks_value'] = pd.to_numeric(self.df['current_marks_value'], errors='coerce')
        
        # Standardize categorical values
        self.df['education_level'] = self.df['education_level'].str.strip()
        self.df['next_path'] = self.df['next_path'].str.strip()
        self.df['placement_status'] = self.df['placement_status'].fillna('Unknown')
        
        # Create success indicators
        self.df['is_successful'] = self.df.apply(self._determine_success, axis=1)
        
        logger.info(f"Cleaned data: {len(self.df)} records")
        return self.df
    
    def _determine_success(self, row) -> bool:
        """Determine if outcome is successful based on placement/admission status"""
        if row['next_path'] == 'Job' and row['placement_status'] == 'Placed':
            return True
        elif row['next_path'] == 'Higher Education' and row['admission_status'] in ['Applied', 'Admitted']:
            return True
        elif row['next_path'] == 'Undecided':
            return False  # Neutral, not necessarily unsuccessful
        return False
    
    def extract_unique_careers(self) -> List[Dict[str, Any]]:
        """Extract unique career paths from the data"""
        careers = []
        
        # Extract job roles
        job_data = self.df[
            (self.df['next_path'] == 'Job') & 
            (self.df['next_role'].notna()) & 
            (self.df['company_name'].notna())
        ]
        
        for _, row in job_data.iterrows():
            career_name = row['next_role']
            if career_name and career_name.strip():
                careers.append({
                    'name': career_name.strip(),
                    'category': self._determine_career_category(career_name),
                    'company_examples': [row['company_name']] if row['company_name'] else [],
                    'education_requirements': row['education_level'],
                    'skills_from_interests': row['interests'],
                    'success_rate': 1.0 if row['placement_status'] == 'Placed' else 0.0
                })
        
        # Group by career name and aggregate data
        career_dict = {}
        for career in careers:
            name = career['name']
            if name not in career_dict:
                career_dict[name] = {
                    'name': name,
                    'category': career['category'],
                    'companies': set(),
                    'education_levels': set(),
                    'interests': set(),
                    'success_count': 0,
                    'total_count': 0
                }
            
            career_dict[name]['companies'].update(career['company_examples'])
            career_dict[name]['education_levels'].add(career['education_requirements'])
            if career['skills_from_interests']:
                interests = [i.strip() for i in career['skills_from_interests'].split('|')]
                career_dict[name]['interests'].update(interests)
            career_dict[name]['success_count'] += career['success_rate']
            career_dict[name]['total_count'] += 1
        
        # Convert sets to lists and calculate success rates
        unique_careers = []
        for career_data in career_dict.values():
            unique_careers.append({
                'name': career_data['name'],
                'category': career_data['category'],
                'top_companies': list(career_data['companies'])[:5],
                'education_requirements': list(career_data['education_levels']),
                'related_interests': list(career_data['interests']),
                'success_rate': career_data['success_count'] / career_data['total_count'] if career_data['total_count'] > 0 else 0.0,
                'sample_size': career_data['total_count']
            })
        
        return unique_careers
    
    def _determine_career_category(self, career_name: str) -> str:
        """Categorize career based on role name"""
        career_name = career_name.lower()
        
        if any(term in career_name for term in ['software', 'developer', 'engineer', 'programmer', 'tech']):
            return 'Technology'
        elif any(term in career_name for term in ['analyst', 'data', 'research']):
            return 'Analytics & Research'
        elif any(term in career_name for term in ['manager', 'management', 'lead']):
            return 'Management'
        elif any(term in career_name for term in ['design', 'architect']):
            return 'Design & Architecture'
        elif any(term in career_name for term in ['finance', 'bank', 'investment']):
            return 'Finance'
        elif any(term in career_name for term in ['doctor', 'medical', 'health']):
            return 'Healthcare'
        elif any(term in career_name for term in ['teacher', 'education', 'professor']):
            return 'Education'
        else:
            return 'Other'
    
    def create_training_features(self) -> pd.DataFrame:
        """Create feature vectors for machine learning"""
        if self.df is None:
            self.clean_data()
        
        # Create feature columns
        features_df = self.df.copy()
        
        # Encode categorical variables
        features_df['education_level_encoded'] = pd.Categorical(features_df['education_level']).codes
        features_df['residence_encoded'] = pd.Categorical(features_df['residence']).codes
        features_df['family_background_encoded'] = pd.Categorical(features_df['family_background']).codes
        
        # Create interest vectors (simplified - could use TF-IDF)
        all_interests = set()
        for interests_str in features_df['interests'].fillna(''):
            if interests_str:
                interests = [i.strip() for i in interests_str.split('|')]
                all_interests.update(interests)
        
        # Create binary interest features
        for interest in all_interests:
            features_df[f'interest_{interest.lower().replace(" ", "_")}'] = features_df['interests'].apply(
                lambda x: 1 if interest in str(x) else 0
            )
        
        # Normalize academic scores
        features_df['normalized_marks'] = features_df['current_marks_value'] / 100.0
        
        return features_df
    
    def load_to_database(self, db: Session) -> Dict[str, int]:
        """Load processed data to database"""
        if self.df is None:
            self.clean_data()
        
        loaded_counts = {'career_outcomes': 0, 'careers': 0}
        
        # Load career outcomes
        for _, row in self.df.iterrows():
            career_outcome = CareerOutcome(
                education_level=row.get('education_level', ''),
                course_of_study=row.get('current_course_of_study', ''),
                institution_type=row.get('current_institution', ''),
                marks_type=row.get('current_marks_type', ''),
                marks_value=row.get('current_marks_value'),
                residence_type=row.get('residence', ''),
                family_background=row.get('family_background', ''),
                interests=row.get('interests', ''),
                next_path=row.get('next_path', ''),
                company_name=row.get('company_name'),
                job_role=row.get('next_role'),
                placement_status=row.get('placement_status', ''),
                next_course=row.get('next_course'),
                next_institution=row.get('next_institution'),
                admission_status=row.get('admission_status'),
                is_successful_outcome=row.get('is_successful', False)
            )
            db.add(career_outcome)
            loaded_counts['career_outcomes'] += 1
        
        # Load unique careers
        unique_careers = self.extract_unique_careers()
        for career_data in unique_careers:
            # Check if career already exists
            existing = db.query(Career).filter(Career.name == career_data['name']).first()
            if not existing:
                career = Career(
                    name=career_data['name'],
                    category=career_data['category'],
                    description_en=f"Career in {career_data['category']} field",
                    description_hi=f"{career_data['category']} क्षेत्र में करियर",
                    required_skills=','.join(career_data['related_interests'][:5]),
                    interests=','.join(career_data['related_interests'][:5]),
                    placement_success_rate=career_data['success_rate'],
                    top_companies=career_data['top_companies'],
                    typical_job_roles=[career_data['name']]
                )
                db.add(career)
                loaded_counts['careers'] += 1
        
        try:
            db.commit()
            logger.info(f"Loaded to database: {loaded_counts}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error loading to database: {e}")
            raise
        
        return loaded_counts

def load_training_data(csv_path: str = "data.csv") -> Dict[str, int]:
    """Main function to load training data"""
    db = SessionLocal()
    try:
        processor = DataProcessor(csv_path)
        return processor.load_to_database(db)
    finally:
        db.close()
