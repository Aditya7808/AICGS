"""
Supabase CRUD Operations for Career Recommendations
Handles career data and recommendations using Supabase
"""

from typing import List, Dict, Any, Optional
import logging
from ..db.supabase_client import get_supabase_client, get_supabase_service_client

logger = logging.getLogger(__name__)

class CareerCRUD:
    """CRUD operations for careers in Supabase"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self.supabase_service = get_supabase_service_client()
    
    async def get_all_careers(self) -> List[Dict[str, Any]]:
        """Get all careers from Supabase"""
        try:
            result = self.supabase.table("careers").select("*").execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting careers: {e}")
            return []
    
    async def get_career_by_id(self, career_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific career by ID"""
        try:
            result = self.supabase.table("careers").select("*").eq("id", career_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error getting career {career_id}: {e}")
            return None
    
    async def search_careers(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search careers with filters"""
        try:
            query = self.supabase.table("careers").select("*")
            
            if filters.get("category"):
                query = query.eq("category", filters["category"])
            
            if filters.get("min_education_level"):
                query = query.eq("min_education_level", filters["min_education_level"])
            
            if filters.get("is_active", True):
                query = query.eq("is_active", True)
            
            result = query.execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error searching careers: {e}")
            return []
    
    async def create_sample_careers(self) -> bool:
        """Create sample career data if none exists"""
        try:
            # Check if careers already exist
            existing = await self.get_all_careers()
            if existing:
                logger.info(f"Found {len(existing)} existing careers, skipping sample creation")
                return True
            
            sample_careers = [
                {
                    "name": "Software Engineer",
                    "category": "Technology",
                    "subcategory": "Software Development",
                    "description_en": "Design, develop, and maintain software applications and systems",
                    "description_hi": "सॉफ्टवेयर एप्लिकेशन और सिस्टम को डिजाइन, विकसित और बनाए रखना",
                    "required_skills": ["Programming", "Problem Solving", "Algorithms"],
                    "interests": ["Technology", "Coding", "Innovation"],
                    "min_education_level": "Bachelor",
                    "preferred_subjects": ["Computer Science", "Mathematics"],
                    "local_demand": "High",
                    "average_salary_range": "5-15 LPA",
                    "growth_prospects": "Excellent",
                    "is_active": True
                },
                {
                    "name": "Data Scientist", 
                    "category": "Technology",
                    "subcategory": "Data Science",
                    "description_en": "Analyze complex data to derive insights and build predictive models",
                    "description_hi": "जटिल डेटा का विश्लेषण करके अंतर्दृष्टि प्राप्त करना और भविष्यवाणी मॉडल बनाना",
                    "required_skills": ["Statistics", "Machine Learning", "Python", "Data Analysis"],
                    "interests": ["Analytics", "Mathematics", "Research"],
                    "min_education_level": "Bachelor",
                    "preferred_subjects": ["Mathematics", "Statistics", "Computer Science"],
                    "local_demand": "Very High",
                    "average_salary_range": "8-20 LPA",
                    "growth_prospects": "Excellent",
                    "is_active": True
                },
                {
                    "name": "Digital Marketing Specialist",
                    "category": "Marketing",
                    "subcategory": "Digital Marketing", 
                    "description_en": "Plan and execute digital marketing campaigns across various platforms",
                    "description_hi": "विभिन्न प्लेटफॉर्म पर डिजिटल मार्केटिंग अभियानों की योजना और क्रियान्वयन",
                    "required_skills": ["Digital Marketing", "Content Creation", "Analytics", "SEO"],
                    "interests": ["Marketing", "Creativity", "Communication"],
                    "min_education_level": "Bachelor",
                    "preferred_subjects": ["Marketing", "Business", "Communication"],
                    "local_demand": "High",
                    "average_salary_range": "3-10 LPA",
                    "growth_prospects": "Good",
                    "is_active": True
                },
                {
                    "name": "Financial Analyst",
                    "category": "Finance",
                    "subcategory": "Investment Analysis",
                    "description_en": "Analyze financial data and market trends to guide investment decisions",
                    "description_hi": "निवेश निर्णयों का मार्गदर्शन करने के लिए वित्तीय डेटा और बाजार रुझानों का विश्लेषण",
                    "required_skills": ["Financial Analysis", "Excel", "Market Research", "Economics"],
                    "interests": ["Finance", "Economics", "Analysis"],
                    "min_education_level": "Bachelor",
                    "preferred_subjects": ["Finance", "Economics", "Mathematics"],
                    "local_demand": "Medium",
                    "average_salary_range": "4-12 LPA",
                    "growth_prospects": "Good",
                    "is_active": True
                },
                {
                    "name": "Graphic Designer",
                    "category": "Design",
                    "subcategory": "Visual Design",
                    "description_en": "Create visual concepts and designs for digital and print media",
                    "description_hi": "डिजिटल और प्रिंट मीडिया के लिए दृश्य अवधारणाओं और डिजाइन बनाना",
                    "required_skills": ["Adobe Creative Suite", "Design Principles", "Typography", "Creativity"],
                    "interests": ["Art", "Design", "Creativity"],
                    "min_education_level": "Diploma",
                    "preferred_subjects": ["Fine Arts", "Design", "Computer Graphics"],
                    "local_demand": "Medium",
                    "average_salary_range": "2-8 LPA",
                    "growth_prospects": "Good",
                    "is_active": True
                }
            ]
            
            result = self.supabase_service.table("careers").insert(sample_careers).execute()
            
            if result.data:
                logger.info(f"Created {len(result.data)} sample careers")
                return True
            else:
                logger.warning("No careers were created")
                return False
                
        except Exception as e:
            logger.error(f"Error creating sample careers: {e}")
            return False

# Create a singleton instance
career_crud = CareerCRUD()
