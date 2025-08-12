#!/usr/bin/env python3
"""
Simplified Supabase Verification and Data Setup
This script verifies the database connection and inserts sample data using the REST API
"""

import os
import sys
import asyncio
import logging
from typing import Dict, Any

# Add the parent directory to the path so we can import from app
sys.path.append('/home/amartya/Desktop/aicgs/careerbuddy/backend')

from app.db.supabase_client import get_supabase_client
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """Test basic Supabase connection"""
    try:
        supabase = get_supabase_client()
        
        # Test a simple query
        result = supabase.table("profiles").select("count").execute()
        logger.info("✅ Supabase connection successful!")
        return True
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return False

def verify_tables():
    """Verify that required tables exist"""
    supabase = get_supabase_client()
    
    required_tables = [
        "profiles",
        "user_profiles", 
        "career_opportunities",
        "education_pathways",
        "user_interactions",
        "recommendation_analytics"
    ]
    
    results = {}
    for table in required_tables:
        try:
            result = supabase.table(table).select("count").execute()
            results[table] = "✅ EXISTS"
            logger.info(f"✅ Table '{table}' exists")
        except Exception as e:
            results[table] = f"❌ MISSING: {e}"
            logger.error(f"❌ Table '{table}' missing or inaccessible: {e}")
    
    return results

def insert_sample_data():
    """Insert sample data using REST API"""
    supabase = get_supabase_client()
    
    # Sample career opportunities
    career_opportunities = [
        {
            "title": "Software Engineer",
            "company": "Tech Corp",
            "description": "Develop web applications using modern technologies",
            "required_skills": ["Python", "JavaScript", "React"],
            "experience_level": "Mid-level",
            "location": "San Francisco, CA",
            "salary_range": "$80k-120k",
            "job_type": "Full-time",
            "industry": "Technology",
            "is_active": True
        },
        {
            "title": "Data Scientist", 
            "company": "Data Inc",
            "description": "Analyze large datasets to derive business insights",
            "required_skills": ["Python", "R", "SQL", "Machine Learning"],
            "experience_level": "Senior",
            "location": "New York, NY", 
            "salary_range": "$100k-150k",
            "job_type": "Full-time",
            "industry": "Technology",
            "is_active": True
        }
    ]
    
    # Sample education pathways
    education_pathways = [
        {
            "name": "Full Stack Web Development Bootcamp",
            "description": "Intensive program covering frontend and backend development",
            "duration_months": 6,
            "difficulty_level": "Intermediate",
            "prerequisites": ["Basic programming knowledge"],
            "skills_gained": ["React", "Node.js", "MongoDB", "JavaScript"],
            "career_outcomes": ["Junior Developer", "Frontend Developer", "Backend Developer"],
            "provider": "TechEd Academy",
            "cost_range": "$8k-12k",
            "is_active": True
        },
        {
            "name": "Data Science Certificate",
            "description": "Comprehensive data science program with hands-on projects", 
            "duration_months": 9,
            "difficulty_level": "Advanced",
            "prerequisites": ["Statistics", "Basic Python"],
            "skills_gained": ["Python", "Machine Learning", "Data Analysis", "SQL"],
            "career_outcomes": ["Data Scientist", "Data Analyst", "ML Engineer"],
            "provider": "University Online",
            "cost_range": "$5k-8k",
            "is_active": True
        }
    ]
    
    try:
        # Insert career opportunities
        result = supabase.table("career_opportunities").insert(career_opportunities).execute()
        logger.info(f"✅ Inserted {len(result.data)} career opportunities")
    except Exception as e:
        logger.warning(f"⚠️  Career opportunities may already exist or table not ready: {e}")
    
    try:
        # Insert education pathways
        result = supabase.table("education_pathways").insert(education_pathways).execute()
        logger.info(f"✅ Inserted {len(result.data)} education pathways")
    except Exception as e:
        logger.warning(f"⚠️  Education pathways may already exist or table not ready: {e}")

def main():
    """Main setup function"""
    print("\n" + "="*50)
    print("🚀 CareerBuddy Supabase Verification")
    print("="*50)
    
    # Test connection
    print("\n1. Testing Supabase connection...")
    if not test_connection():
        print("❌ Please check your Supabase credentials in .env file")
        return
    
    # Verify tables
    print("\n2. Verifying database tables...")
    table_results = verify_tables()
    
    missing_tables = [table for table, status in table_results.items() if "MISSING" in status]
    if missing_tables:
        print(f"\n⚠️  Missing tables: {missing_tables}")
        print("\n📋 MANUAL SETUP REQUIRED:")
        print("1. Go to your Supabase dashboard")
        print("2. Navigate to SQL Editor")
        print("3. Copy and paste the contents of 'SUPABASE_MANUAL_SCHEMA_SETUP.sql'")
        print("4. Run the SQL script")
        print("5. Run this verification script again")
        return
    
    print("✅ All required tables exist!")
    
    # Insert sample data
    print("\n3. Inserting sample data...")
    insert_sample_data()
    
    print("\n" + "="*50)
    print("🎉 Supabase setup verification complete!")
    print("="*50)
    print("✅ Your CareerBuddy backend is ready to use!")
    print("\nNext steps:")
    print("1. Start your backend: uvicorn app.main:app --reload")
    print("2. Visit http://localhost:8000/docs to test the API")
    print("3. Test user registration and login endpoints")

if __name__ == "__main__":
    main()
