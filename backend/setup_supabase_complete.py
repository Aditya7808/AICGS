#!/usr/bin/env python3
"""
Complete Supabase Setup Script for CareerBuddy
This script creates all necessary tables, indexes, and sample data in Supabase
"""

import os
import sys
import logging
from supabase import create_client, Client
from sqlalchemy import create_engine, text
from datetime import datetime
import json

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.config import settings
from app.db.supabase_client import supabase_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY', 
        'SUPABASE_SERVICE_ROLE_KEY',
        'DATABASE_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not getattr(settings, var.lower(), None):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.error("Please create a .env file with the required Supabase configuration")
        return False
    
    return True

def create_database_schema(engine):
    """Create the complete database schema"""
    
    schema_sql = """
    -- Enable UUID extension
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Profiles table (linked to Supabase auth.users)
    CREATE TABLE IF NOT EXISTS profiles (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        full_name VARCHAR(255),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        is_active BOOLEAN DEFAULT true
    );
    
    -- User Profiles with multi-dimensional data
    CREATE TABLE IF NOT EXISTS user_profiles (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        user_id UUID NOT NULL UNIQUE REFERENCES profiles(id),
        age INTEGER,
        education_level VARCHAR(100) NOT NULL,
        location VARCHAR(200) NOT NULL,
        cultural_context VARCHAR(100) NOT NULL,
        family_background VARCHAR(100) NOT NULL,
        language_preference VARCHAR(10) DEFAULT 'en',
        economic_context VARCHAR(100) NOT NULL,
        financial_constraints TEXT,
        geographic_constraints VARCHAR(200) NOT NULL,
        urban_rural_type VARCHAR(20) DEFAULT 'urban',
        infrastructure_level VARCHAR(20) DEFAULT 'good',
        family_expectations VARCHAR(200) NOT NULL,
        peer_influence_score DECIMAL(3,2) DEFAULT 0.5,
        community_values TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Career Preferences
    CREATE TABLE IF NOT EXISTS career_preferences (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES profiles(id),
        career_goals TEXT DEFAULT '',
        preferred_industries TEXT[] DEFAULT '{}',
        work_environment_preference VARCHAR(50) DEFAULT 'office',
        salary_expectations VARCHAR(100) DEFAULT '',
        work_life_balance_priority INTEGER DEFAULT 5,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- User Skills and Interests
    CREATE TABLE IF NOT EXISTS user_skills_interests (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES profiles(id),
        technical_skills TEXT[] DEFAULT '{}',
        soft_skills TEXT[] DEFAULT '{}',
        interests TEXT[] DEFAULT '{}',
        learning_preferences TEXT[] DEFAULT '{}',
        personality_traits JSONB DEFAULT '{}',
        skill_assessments JSONB DEFAULT '{}',
        interest_strength_scores JSONB DEFAULT '{}',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Careers table
    CREATE TABLE IF NOT EXISTS careers (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        description_en TEXT NOT NULL,
        description_hi TEXT,
        category VARCHAR(100),
        subcategory VARCHAR(100),
        required_skills TEXT[] DEFAULT '{}',
        interests TEXT[] DEFAULT '{}',
        min_education_level VARCHAR(100),
        preferred_subjects TEXT[] DEFAULT '{}',
        local_demand VARCHAR(50) DEFAULT 'Medium',
        average_salary_range VARCHAR(100),
        growth_prospects VARCHAR(50) DEFAULT 'Good',
        work_environment VARCHAR(100),
        typical_career_path TEXT[] DEFAULT '{}',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Career Opportunities
    CREATE TABLE IF NOT EXISTS career_opportunities (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        career_id UUID REFERENCES careers(id),
        user_id UUID REFERENCES profiles(id),
        opportunity_title VARCHAR(255) NOT NULL,
        company_name VARCHAR(200),
        location VARCHAR(200),
        employment_type VARCHAR(50),
        experience_level VARCHAR(50),
        salary_range VARCHAR(100),
        job_description TEXT,
        required_skills TEXT[] DEFAULT '{}',
        application_deadline DATE,
        application_url VARCHAR(500),
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Recommendation Feedback
    CREATE TABLE IF NOT EXISTS recommendation_feedback (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES profiles(id),
        career_id UUID REFERENCES careers(id),
        recommendation_type VARCHAR(50) NOT NULL,
        feedback_rating INTEGER CHECK (feedback_rating >= 1 AND feedback_rating <= 5),
        feedback_comments TEXT,
        is_helpful BOOLEAN,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- User Interactions for analytics
    CREATE TABLE IF NOT EXISTS user_interactions (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES profiles(id),
        interaction_type VARCHAR(100) NOT NULL,
        interaction_data JSONB DEFAULT '{}',
        session_id VARCHAR(100),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Assessment History
    CREATE TABLE IF NOT EXISTS assessment_history (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES profiles(id),
        assessment_type VARCHAR(100) NOT NULL,
        responses JSONB NOT NULL,
        results JSONB NOT NULL,
        completion_time DECIMAL(10,2),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Career Goals
    CREATE TABLE IF NOT EXISTS career_goals (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES profiles(id),
        career_id UUID REFERENCES careers(id),
        goal_type VARCHAR(50) DEFAULT 'primary',
        timeline VARCHAR(50) DEFAULT '1_year',
        priority INTEGER DEFAULT 1,
        status VARCHAR(50) DEFAULT 'active',
        progress_percentage DECIMAL(5,2) DEFAULT 0.0,
        completed_skills TEXT[] DEFAULT '{}',
        next_action TEXT,
        links JSONB DEFAULT '[]',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Skill Progress
    CREATE TABLE IF NOT EXISTS skill_progress (
        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES profiles(id),
        skill_name VARCHAR(200) NOT NULL,
        current_level VARCHAR(50) NOT NULL,
        target_level VARCHAR(50) NOT NULL,
        proficiency_score DECIMAL(5,2) DEFAULT 0.0,
        time_invested_hours DECIMAL(10,2) DEFAULT 0.0,
        progress_history JSONB DEFAULT '[]',
        last_practice_date TIMESTAMP WITH TIME ZONE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        UNIQUE(user_id, skill_name)
    );
    
    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
    CREATE INDEX IF NOT EXISTS idx_career_preferences_user_id ON career_preferences(user_id);
    CREATE INDEX IF NOT EXISTS idx_user_skills_interests_user_id ON user_skills_interests(user_id);
    CREATE INDEX IF NOT EXISTS idx_career_opportunities_career_id ON career_opportunities(career_id);
    CREATE INDEX IF NOT EXISTS idx_career_opportunities_user_id ON career_opportunities(user_id);
    CREATE INDEX IF NOT EXISTS idx_recommendation_feedback_user_id ON recommendation_feedback(user_id);
    CREATE INDEX IF NOT EXISTS idx_user_interactions_user_id ON user_interactions(user_id);
    CREATE INDEX IF NOT EXISTS idx_assessment_history_user_id ON assessment_history(user_id);
    CREATE INDEX IF NOT EXISTS idx_career_goals_user_id ON career_goals(user_id);
    CREATE INDEX IF NOT EXISTS idx_skill_progress_user_id ON skill_progress(user_id);
    CREATE INDEX IF NOT EXISTS idx_careers_category ON careers(category);
    CREATE INDEX IF NOT EXISTS idx_careers_subcategory ON careers(subcategory);
    
    -- Create a view for complete user profiles
    CREATE OR REPLACE VIEW user_complete_profiles AS
    SELECT 
        p.id,
        p.email,
        p.full_name,
        p.created_at,
        p.is_active,
        up.age,
        up.education_level,
        up.location,
        up.cultural_context,
        up.family_background,
        up.language_preference,
        up.economic_context,
        up.financial_constraints,
        up.geographic_constraints,
        up.urban_rural_type,
        up.infrastructure_level,
        up.family_expectations,
        up.peer_influence_score,
        up.community_values,
        cp.career_goals,
        cp.preferred_industries,
        cp.work_environment_preference,
        cp.salary_expectations,
        cp.work_life_balance_priority,
        usi.technical_skills,
        usi.soft_skills,
        usi.interests,
        usi.learning_preferences,
        usi.personality_traits,
        usi.skill_assessments,
        usi.interest_strength_scores
    FROM profiles p
    LEFT JOIN user_profiles up ON p.id = up.user_id
    LEFT JOIN career_preferences cp ON p.id = cp.user_id
    LEFT JOIN user_skills_interests usi ON p.id = usi.user_id;
    
    -- Enable Row Level Security (RLS) for user data
    ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
    ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
    ALTER TABLE career_preferences ENABLE ROW LEVEL SECURITY;
    ALTER TABLE user_skills_interests ENABLE ROW LEVEL SECURITY;
    ALTER TABLE recommendation_feedback ENABLE ROW LEVEL SECURITY;
    ALTER TABLE user_interactions ENABLE ROW LEVEL SECURITY;
    ALTER TABLE assessment_history ENABLE ROW LEVEL SECURITY;
    ALTER TABLE career_goals ENABLE ROW LEVEL SECURITY;
    ALTER TABLE skill_progress ENABLE ROW LEVEL SECURITY;
    
    -- Create RLS policies (users can only access their own data)
    CREATE POLICY IF NOT EXISTS "Users can view own profile" ON profiles FOR ALL USING (auth.uid()::text = id::text);
    CREATE POLICY IF NOT EXISTS "Users can manage own user_profile" ON user_profiles FOR ALL USING (auth.uid()::text = user_id::text);
    CREATE POLICY IF NOT EXISTS "Users can manage own career_preferences" ON career_preferences FOR ALL USING (auth.uid()::text = user_id::text);
    CREATE POLICY IF NOT EXISTS "Users can manage own skills_interests" ON user_skills_interests FOR ALL USING (auth.uid()::text = user_id::text);
    CREATE POLICY IF NOT EXISTS "Users can manage own feedback" ON recommendation_feedback FOR ALL USING (auth.uid()::text = user_id::text);
    CREATE POLICY IF NOT EXISTS "Users can manage own interactions" ON user_interactions FOR ALL USING (auth.uid()::text = user_id::text);
    CREATE POLICY IF NOT EXISTS "Users can manage own assessments" ON assessment_history FOR ALL USING (auth.uid()::text = user_id::text);
    CREATE POLICY IF NOT EXISTS "Users can manage own goals" ON career_goals FOR ALL USING (auth.uid()::text = user_id::text);
    CREATE POLICY IF NOT EXISTS "Users can manage own skill progress" ON skill_progress FOR ALL USING (auth.uid()::text = user_id::text);
    """
    
    try:
        with engine.connect() as conn:
            # Execute schema creation
            statements = schema_sql.split(';')
            for statement in statements:
                if statement.strip():
                    conn.execute(text(statement))
            conn.commit()
        logger.info("Database schema created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating database schema: {e}")
        return False

def create_sample_data():
    """Create sample careers and other data"""
    try:
        supabase = create_client(settings.supabase_url, settings.supabase_service_role_key)
        
        # Sample careers data
        sample_careers = [
            {
                "name": "Software Developer",
                "description_en": "Develops software applications and systems using various programming languages and frameworks.",
                "description_hi": "विभिन्न प्रोग्रामिंग भाषाओं और फ्रेमवर्क का उपयोग करके सॉफ्टवेयर एप्लिकेशन और सिस्टम विकसित करता है।",
                "category": "Technology",
                "subcategory": "Software Development",
                "required_skills": ["Programming", "Problem Solving", "Debugging", "Version Control"],
                "interests": ["Technology", "Innovation", "Logic", "Creativity"],
                "min_education_level": "Bachelor's Degree",
                "preferred_subjects": ["Computer Science", "Mathematics", "Engineering"],
                "local_demand": "High",
                "average_salary_range": "5-12 LPA",
                "growth_prospects": "Excellent",
                "work_environment": "Office/Remote",
                "typical_career_path": ["Junior Developer", "Senior Developer", "Tech Lead", "Engineering Manager"]
            },
            {
                "name": "Data Scientist",
                "description_en": "Analyzes complex data to help businesses make informed decisions using statistical methods and machine learning.",
                "description_hi": "सांख्यिकीय विधियों और मशीन लर्निंग का उपयोग करके व्यवसायों को सूचित निर्णय लेने में मदद करने के लिए जटिल डेटा का विश्लेषण करता है।",
                "category": "Technology",
                "subcategory": "Data Science",
                "required_skills": ["Python", "Statistics", "Machine Learning", "Data Visualization", "SQL"],
                "interests": ["Mathematics", "Analysis", "Research", "Technology"],
                "min_education_level": "Bachelor's Degree",
                "preferred_subjects": ["Statistics", "Mathematics", "Computer Science"],
                "local_demand": "Very High",
                "average_salary_range": "8-20 LPA",
                "growth_prospects": "Excellent",
                "work_environment": "Office/Remote",
                "typical_career_path": ["Junior Data Analyst", "Data Scientist", "Senior Data Scientist", "Lead Data Scientist"]
            },
            {
                "name": "UI/UX Designer",
                "description_en": "Creates user-friendly and visually appealing designs for websites, applications, and digital products.",
                "description_hi": "वेबसाइट, एप्लिकेशन और डिजिटल उत्पादों के लिए उपयोगकर्ता-अनुकूल और दृश्य रूप से आकर्षक डिजाइन बनाता है।",
                "category": "Design",
                "subcategory": "User Experience",
                "required_skills": ["Design Thinking", "Figma", "Adobe Creative Suite", "Prototyping", "User Research"],
                "interests": ["Design", "Art", "Psychology", "Technology"],
                "min_education_level": "Bachelor's Degree",
                "preferred_subjects": ["Design", "Psychology", "Computer Science"],
                "local_demand": "High",
                "average_salary_range": "4-10 LPA",
                "growth_prospects": "Good",
                "work_environment": "Office/Remote",
                "typical_career_path": ["Junior Designer", "UI/UX Designer", "Senior Designer", "Design Lead"]
            },
            {
                "name": "Digital Marketing Specialist",
                "description_en": "Develops and executes marketing strategies across digital channels to promote products and services.",
                "description_hi": "उत्पादों और सेवाओं को बढ़ावा देने के लिए डिजिटल चैनलों में मार्केटिंग रणनीति विकसित और निष्पादित करता है।",
                "category": "Marketing",
                "subcategory": "Digital Marketing",
                "required_skills": ["SEO", "Social Media Marketing", "Content Marketing", "Analytics", "PPC"],
                "interests": ["Marketing", "Communication", "Creativity", "Technology"],
                "min_education_level": "Bachelor's Degree",
                "preferred_subjects": ["Marketing", "Business", "Communications"],
                "local_demand": "High",
                "average_salary_range": "3-8 LPA",
                "growth_prospects": "Good",
                "work_environment": "Office",
                "typical_career_path": ["Marketing Assistant", "Digital Marketing Specialist", "Marketing Manager", "Marketing Director"]
            },
            {
                "name": "Business Analyst",
                "description_en": "Analyzes business processes and requirements to improve efficiency and drive business solutions.",
                "description_hi": "दक्षता में सुधार और व्यावसायिक समाधान चलाने के लिए व्यावसायिक प्रक्रियाओं और आवश्यकताओं का विश्लेषण करता है।",
                "category": "Business",
                "subcategory": "Analysis",
                "required_skills": ["Business Analysis", "Requirements Gathering", "Documentation", "Process Mapping"],
                "interests": ["Business", "Analysis", "Problem Solving", "Communication"],
                "min_education_level": "Bachelor's Degree",
                "preferred_subjects": ["Business", "Economics", "Management"],
                "local_demand": "High",
                "average_salary_range": "4-10 LPA",
                "growth_prospects": "Good",
                "work_environment": "Office",
                "typical_career_path": ["Junior Analyst", "Business Analyst", "Senior Analyst", "Lead Analyst"]
            }
        ]
        
        # Check if careers already exist
        existing_careers = supabase.table("careers").select("id").limit(1).execute()
        
        if not existing_careers.data:
            # Insert sample careers
            result = supabase.table("careers").insert(sample_careers).execute()
            logger.info(f"Created {len(result.data)} sample careers")
        else:
            logger.info("Sample careers already exist, skipping creation")
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
        return False

def main():
    """Main setup function"""
    logger.info("Starting Supabase setup for CareerBuddy...")
    
    # Check environment variables
    if not check_environment():
        sys.exit(1)
    
    try:
        # Initialize Supabase manager
        supabase_manager.initialize()
        logger.info("Supabase connection established")
        
        # Create database engine for schema creation
        engine = create_engine(settings.database_url)
        
        # Create schema
        if not create_database_schema(engine):
            logger.error("Failed to create database schema")
            sys.exit(1)
        
        # Create sample data
        if not create_sample_data():
            logger.error("Failed to create sample data")
            sys.exit(1)
        
        logger.info("✅ Supabase setup completed successfully!")
        logger.info("Your CareerBuddy application is now ready to use with Supabase PostgreSQL")
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
