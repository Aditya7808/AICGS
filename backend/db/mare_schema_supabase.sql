-- MARE Database Schema for Supabase (PostgreSQL)
-- Multi-Dimensional Adaptive Recommendation Engine

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS recommendation_feedback CASCADE;
DROP TABLE IF EXISTS career_opportunities CASCADE;
DROP TABLE IF EXISTS user_skills_interests CASCADE;
DROP TABLE IF EXISTS career_preferences CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;

-- Users table (Supabase auth.users integration)
-- Note: In Supabase, user authentication is handled by auth.users table
-- We create a profiles table linked to auth.users
CREATE TABLE profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Multi-dimensional user profiles for MARE
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Personal dimensions
    age INTEGER CHECK (age >= 13 AND age <= 100),
    education_level TEXT NOT NULL,
    location TEXT NOT NULL,
    
    -- Cultural dimensions
    cultural_context TEXT NOT NULL,
    family_background TEXT NOT NULL,
    language_preference TEXT DEFAULT 'en',
    
    -- Economic dimensions
    economic_context TEXT NOT NULL,
    financial_constraints TEXT,
    
    -- Geographic dimensions
    geographic_constraints TEXT NOT NULL,
    urban_rural_type TEXT DEFAULT 'urban' CHECK (urban_rural_type IN ('urban', 'rural', 'semi_urban')),
    infrastructure_level TEXT DEFAULT 'good' CHECK (infrastructure_level IN ('poor', 'fair', 'good', 'excellent')),
    
    -- Social dimensions
    family_expectations TEXT NOT NULL,
    peer_influence_score DECIMAL(3,2) DEFAULT 0.5 CHECK (peer_influence_score >= 0.0 AND peer_influence_score <= 1.0),
    community_values TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(user_id)
);

-- Career preferences and goals
CREATE TABLE career_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Career aspirations
    career_goals TEXT DEFAULT '',
    preferred_industries TEXT[] DEFAULT '{}',
    work_environment_preference TEXT DEFAULT 'office' CHECK (work_environment_preference IN ('office', 'remote', 'hybrid', 'field', 'mixed')),
    salary_expectations TEXT DEFAULT '',
    work_life_balance_priority INTEGER DEFAULT 5 CHECK (work_life_balance_priority >= 1 AND work_life_balance_priority <= 10),
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(user_id)
);

-- Skills and interests with weights
CREATE TABLE user_skills_interests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Skills and interests data
    skills TEXT[] DEFAULT '{}',
    interests TEXT[] DEFAULT '{}',
    skill_weights JSONB DEFAULT '{}',
    interest_weights JSONB DEFAULT '{}',
    
    -- Calculated skill category scores (0.0 to 1.0)
    technical_skills_score DECIMAL(3,2) DEFAULT 0.0,
    creative_skills_score DECIMAL(3,2) DEFAULT 0.0,
    analytical_skills_score DECIMAL(3,2) DEFAULT 0.0,
    communication_skills_score DECIMAL(3,2) DEFAULT 0.0,
    leadership_skills_score DECIMAL(3,2) DEFAULT 0.0,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(user_id)
);

-- Career opportunities database
CREATE TABLE career_opportunities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Basic career information
    title TEXT NOT NULL,
    industry TEXT NOT NULL,
    description TEXT DEFAULT '',
    required_skills TEXT[] DEFAULT '{}',
    preferred_skills TEXT[] DEFAULT '{}',
    
    -- Career characteristics
    experience_level TEXT DEFAULT 'entry' CHECK (experience_level IN ('entry', 'mid', 'senior', 'executive')),
    salary_range_min INTEGER DEFAULT 0,
    salary_range_max INTEGER DEFAULT 0,
    currency TEXT DEFAULT 'INR',
    
    -- Location and availability
    location TEXT DEFAULT '',
    remote_available BOOLEAN DEFAULT FALSE,
    urban_rural_suitability TEXT DEFAULT 'both' CHECK (urban_rural_suitability IN ('urban', 'rural', 'both')),
    
    -- MARE-specific fields
    traditional_modern_spectrum TEXT DEFAULT 'balanced' CHECK (traditional_modern_spectrum IN ('traditional', 'balanced', 'modern')),
    cultural_adaptability_score DECIMAL(3,2) DEFAULT 0.5,
    economic_accessibility_score DECIMAL(3,2) DEFAULT 0.5,
    geographic_flexibility_score DECIMAL(3,2) DEFAULT 0.5,
    family_acceptance_score DECIMAL(3,2) DEFAULT 0.5,
    
    -- Future outlook
    growth_potential_score DECIMAL(3,2) DEFAULT 0.5,
    job_security_score DECIMAL(3,2) DEFAULT 0.5,
    automation_risk_score DECIMAL(3,2) DEFAULT 0.5,
    future_outlook TEXT DEFAULT 'stable' CHECK (future_outlook IN ('declining', 'stable', 'growing', 'booming')),
    
    -- AI/ML Integration
    mare_compatibility_score DECIMAL(3,2) DEFAULT 0.0,
    recommendation_count INTEGER DEFAULT 0,
    positive_feedback_rate DECIMAL(3,2) DEFAULT 0.0,
    
    -- Status and metadata
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Feedback and learning data for MARE
CREATE TABLE recommendation_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    career_opportunity_id UUID REFERENCES career_opportunities(id) ON DELETE CASCADE,
    
    -- Recommendation context
    recommendation_score DECIMAL(4,3) NOT NULL CHECK (recommendation_score >= 0.0 AND recommendation_score <= 1.0),
    
    -- User feedback
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    user_feedback TEXT,
    selected BOOLEAN DEFAULT FALSE,
    time_spent_viewing INTEGER DEFAULT 0, -- seconds
    
    -- Context for learning
    context_snapshot JSONB DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(user_id, career_opportunity_id)
);

-- Indexes for performance optimization
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_location ON user_profiles(location);
CREATE INDEX idx_user_profiles_cultural_context ON user_profiles(cultural_context);
CREATE INDEX idx_user_profiles_economic_context ON user_profiles(economic_context);

CREATE INDEX idx_career_preferences_user_id ON career_preferences(user_id);

CREATE INDEX idx_user_skills_interests_user_id ON user_skills_interests(user_id);

CREATE INDEX idx_career_opportunities_industry ON career_opportunities(industry);
CREATE INDEX idx_career_opportunities_salary ON career_opportunities(salary_range_min, salary_range_max);
CREATE INDEX idx_career_opportunities_active ON career_opportunities(is_active);
CREATE INDEX idx_career_opportunities_mare_score ON career_opportunities(mare_compatibility_score);
CREATE INDEX idx_career_opportunities_location ON career_opportunities(location);

CREATE INDEX idx_recommendation_feedback_user_id ON recommendation_feedback(user_id);
CREATE INDEX idx_recommendation_feedback_career_id ON recommendation_feedback(career_opportunity_id);
CREATE INDEX idx_recommendation_feedback_selected ON recommendation_feedback(selected);
CREATE INDEX idx_recommendation_feedback_rating ON recommendation_feedback(user_rating);
CREATE INDEX idx_recommendation_feedback_created_at ON recommendation_feedback(created_at);

-- Enable Row Level Security (RLS)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE career_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_skills_interests ENABLE ROW LEVEL SECURITY;
ALTER TABLE career_opportunities ENABLE ROW LEVEL SECURITY;
ALTER TABLE recommendation_feedback ENABLE ROW LEVEL SECURITY;

-- Create RLS Policies
-- Profiles: Users can only access their own profile
CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON profiles FOR INSERT WITH CHECK (auth.uid() = id);

-- User profiles: Users can only access their own data
CREATE POLICY "Users can view own user_profile" ON user_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own user_profile" ON user_profiles FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own user_profile" ON user_profiles FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Career preferences: Users can only access their own data
CREATE POLICY "Users can view own career_preferences" ON career_preferences FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own career_preferences" ON career_preferences FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own career_preferences" ON career_preferences FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Skills and interests: Users can only access their own data
CREATE POLICY "Users can view own skills_interests" ON user_skills_interests FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own skills_interests" ON user_skills_interests FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own skills_interests" ON user_skills_interests FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Career opportunities: Everyone can read active opportunities
CREATE POLICY "Anyone can view active career opportunities" ON career_opportunities FOR SELECT USING (is_active = TRUE);

-- Recommendation feedback: Users can only access their own feedback
CREATE POLICY "Users can view own feedback" ON recommendation_feedback FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own feedback" ON recommendation_feedback FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own feedback" ON recommendation_feedback FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_career_preferences_updated_at BEFORE UPDATE ON career_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_skills_interests_updated_at BEFORE UPDATE ON user_skills_interests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_career_opportunities_updated_at BEFORE UPDATE ON career_opportunities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Views for common MARE queries
CREATE VIEW user_complete_profiles AS
SELECT 
    p.id as user_id,
    p.email,
    p.full_name,
    p.created_at as user_created_at,
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
    usi.skills,
    usi.interests,
    usi.skill_weights,
    usi.interest_weights,
    usi.technical_skills_score,
    usi.creative_skills_score,
    usi.analytical_skills_score,
    usi.communication_skills_score,
    usi.leadership_skills_score,
    GREATEST(up.updated_at, cp.updated_at, usi.updated_at) as updated_at
FROM profiles p
LEFT JOIN user_profiles up ON p.id = up.user_id
LEFT JOIN career_preferences cp ON p.id = cp.user_id
LEFT JOIN user_skills_interests usi ON p.id = usi.user_id;

CREATE VIEW recommendation_analytics AS
SELECT 
    rf.user_id,
    rf.career_opportunity_id,
    co.title as career_title,
    co.industry,
    rf.recommendation_score,
    rf.user_rating,
    rf.selected,
    rf.time_spent_viewing,
    CASE 
        WHEN rf.selected = TRUE THEN 'converted'
        WHEN rf.user_rating >= 4 THEN 'positive'
        WHEN rf.user_rating >= 2 THEN 'neutral'
        ELSE 'negative'
    END as conversion
FROM recommendation_feedback rf
JOIN career_opportunities co ON rf.career_opportunity_id = co.id;

-- Sample data insertion (for testing)
-- Note: In production, this would be handled by the application

-- Insert sample career opportunities
INSERT INTO career_opportunities (
    title, industry, description, required_skills, preferred_skills,
    experience_level, salary_range_min, salary_range_max,
    traditional_modern_spectrum, growth_potential_score, job_security_score, future_outlook
) VALUES 
(
    'Software Developer', 'Technology', 
    'Develop web and mobile applications using modern frameworks and technologies.',
    ARRAY['Programming', 'Problem Solving', 'Computer Science Fundamentals'],
    ARRAY['React', 'Node.js', 'Python', 'Git'],
    'entry', 400000, 800000,
    'modern', 0.9, 0.7, 'booming'
),
(
    'Data Analyst', 'Technology', 
    'Analyze business data to derive insights and support decision making.',
    ARRAY['Data Analysis', 'Statistics', 'Excel', 'SQL'],
    ARRAY['Python', 'R', 'Tableau', 'Machine Learning'],
    'entry', 350000, 700000,
    'balanced', 0.8, 0.8, 'growing'
),
(
    'Marketing Executive', 'Marketing', 
    'Plan and execute marketing campaigns to promote products and services.',
    ARRAY['Communication', 'Creativity', 'Market Research'],
    ARRAY['Digital Marketing', 'Social Media', 'Content Writing'],
    'entry', 300000, 600000,
    'balanced', 0.7, 0.6, 'stable'
),
(
    'Agricultural Specialist', 'Agriculture', 
    'Provide technical expertise in crop management and agricultural practices.',
    ARRAY['Agricultural Science', 'Problem Solving', 'Field Work'],
    ARRAY['Soil Science', 'Crop Management', 'Irrigation Systems'],
    'entry', 250000, 450000,
    'traditional', 0.6, 0.8, 'stable'
),
(
    'Teaching Assistant', 'Education',
    'Support classroom instruction and help students with learning activities.',
    ARRAY['Communication', 'Patience', 'Subject Knowledge'],
    ARRAY['Classroom Management', 'Educational Technology', 'Tutoring'],
    'entry', 200000, 400000,
    'traditional', 0.6, 0.9, 'stable'
),
(
    'Digital Marketing Specialist', 'Marketing',
    'Manage online marketing campaigns and social media presence.',
    ARRAY['Digital Marketing', 'Analytics', 'Communication'],
    ARRAY['Google Ads', 'SEO', 'Social Media Management', 'Content Strategy'],
    'entry', 350000, 650000,
    'modern', 0.8, 0.7, 'growing'
);

-- Performance optimization settings
-- These are typically set at the database level in Supabase
