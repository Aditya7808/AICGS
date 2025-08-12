-- ===========================================
-- CareerBuddy Supabase Schema Setup
-- ===========================================
-- Run this in your Supabase SQL Editor
-- Dashboard -> SQL Editor -> New Query

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ===========================================
-- 1. PROFILES TABLE (User Management)
-- ===========================================
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT auth.uid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- RLS Policies for profiles
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Allow users to view their own profile
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

-- Allow users to update their own profile
CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Allow signup process to create profiles
CREATE POLICY "Enable insert during signup" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- ===========================================
-- 2. USER PROFILES TABLE (Extended Info)
-- ===========================================
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    skills TEXT[],
    experience_level VARCHAR(50),
    location VARCHAR(255),
    preferred_industries TEXT[],
    career_goals TEXT,
    education_level VARCHAR(100),
    work_preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    UNIQUE(user_id)
);

-- RLS for user_profiles
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own user_profile" ON user_profiles
    FOR ALL USING (auth.uid() = user_id);

-- ===========================================
-- 3. CAREER OPPORTUNITIES TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS career_opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    description TEXT,
    required_skills TEXT[],
    experience_level VARCHAR(50),
    location VARCHAR(255),
    salary_range VARCHAR(100),
    job_type VARCHAR(50),
    industry VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Public read access for career opportunities
ALTER TABLE career_opportunities ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view active career opportunities" ON career_opportunities
    FOR SELECT USING (is_active = true);

-- ===========================================
-- 4. EDUCATION PATHWAYS TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS education_pathways (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    duration_months INTEGER,
    difficulty_level VARCHAR(50),
    prerequisites TEXT[],
    skills_gained TEXT[],
    career_outcomes TEXT[],
    provider VARCHAR(255),
    cost_range VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Public read access
ALTER TABLE education_pathways ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view active education pathways" ON education_pathways
    FOR SELECT USING (is_active = true);

-- ===========================================
-- 5. USER INTERACTIONS TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS user_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    content_type VARCHAR(50) NOT NULL,
    content_id UUID NOT NULL,
    interaction_type VARCHAR(50) NOT NULL,
    interaction_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    INDEX(user_id, content_type),
    INDEX(content_id, interaction_type)
);

-- RLS for interactions
ALTER TABLE user_interactions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own interactions" ON user_interactions
    FOR ALL USING (auth.uid() = user_id);

-- ===========================================
-- 6. RECOMMENDATION ANALYTICS TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS recommendation_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    recommendation_type VARCHAR(50) NOT NULL,
    content_id UUID NOT NULL,
    relevance_score DECIMAL(5,4),
    algorithm_used VARCHAR(100),
    recommendation_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    INDEX(user_id, recommendation_type),
    INDEX(content_id, relevance_score DESC)
);

-- RLS for analytics
ALTER TABLE recommendation_analytics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own recommendation analytics" ON recommendation_analytics
    FOR SELECT USING (auth.uid() = user_id);

-- Allow system to insert analytics
CREATE POLICY "System can insert analytics" ON recommendation_analytics
    FOR INSERT WITH CHECK (true);

-- ===========================================
-- 7. SAMPLE DATA INSERTION
-- ===========================================

-- Sample Career Opportunities
INSERT INTO career_opportunities (title, company, description, required_skills, experience_level, location, salary_range, job_type, industry) VALUES
('Software Engineer', 'Tech Corp', 'Develop web applications using modern technologies', ARRAY['Python', 'JavaScript', 'React'], 'Mid-level', 'San Francisco, CA', '$80k-120k', 'Full-time', 'Technology'),
('Data Scientist', 'Data Inc', 'Analyze large datasets to derive business insights', ARRAY['Python', 'R', 'SQL', 'Machine Learning'], 'Senior', 'New York, NY', '$100k-150k', 'Full-time', 'Technology'),
('Product Manager', 'StartupXYZ', 'Lead product development and strategy', ARRAY['Product Management', 'Analytics', 'Communication'], 'Senior', 'Austin, TX', '$90k-140k', 'Full-time', 'Technology'),
('UX Designer', 'Design Studio', 'Create user-centered design solutions', ARRAY['Figma', 'User Research', 'Prototyping'], 'Mid-level', 'Los Angeles, CA', '$70k-100k', 'Full-time', 'Design'),
('DevOps Engineer', 'Cloud Solutions', 'Manage infrastructure and deployment pipelines', ARRAY['AWS', 'Docker', 'Kubernetes', 'CI/CD'], 'Senior', 'Seattle, WA', '$110k-160k', 'Full-time', 'Technology');

-- Sample Education Pathways
INSERT INTO education_pathways (name, description, duration_months, difficulty_level, prerequisites, skills_gained, career_outcomes, provider, cost_range) VALUES
('Full Stack Web Development Bootcamp', 'Intensive program covering frontend and backend development', 6, 'Intermediate', ARRAY['Basic programming knowledge'], ARRAY['React', 'Node.js', 'MongoDB', 'JavaScript'], ARRAY['Junior Developer', 'Frontend Developer', 'Backend Developer'], 'TechEd Academy', '$8k-12k'),
('Data Science Certificate', 'Comprehensive data science program with hands-on projects', 9, 'Advanced', ARRAY['Statistics', 'Basic Python'], ARRAY['Python', 'Machine Learning', 'Data Analysis', 'SQL'], ARRAY['Data Scientist', 'Data Analyst', 'ML Engineer'], 'University Online', '$5k-8k'),
('Cloud Architecture Certification', 'Learn cloud infrastructure and architecture patterns', 4, 'Advanced', ARRAY['System Administration', 'Networking'], ARRAY['AWS', 'Azure', 'Cloud Security', 'Architecture'], ARRAY['Cloud Architect', 'DevOps Engineer'], 'Cloud Institute', '$3k-5k'),
('UX/UI Design Course', 'User experience and interface design fundamentals', 8, 'Beginner', ARRAY['Basic computer skills'], ARRAY['Design Thinking', 'Figma', 'User Research', 'Prototyping'], ARRAY['UX Designer', 'UI Designer', 'Product Designer'], 'Design Academy', '$4k-6k'),
('Cybersecurity Bootcamp', 'Hands-on cybersecurity training and certification prep', 12, 'Intermediate', ARRAY['IT fundamentals', 'Networking basics'], ARRAY['Ethical Hacking', 'Security Analysis', 'Risk Management'], ARRAY['Security Analyst', 'Penetration Tester'], 'CyberSec Training', '$10k-15k');

-- ===========================================
-- 8. HELPFUL FUNCTIONS
-- ===========================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_career_opportunities_updated_at BEFORE UPDATE ON career_opportunities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_education_pathways_updated_at BEFORE UPDATE ON education_pathways FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ===========================================
-- SCHEMA SETUP COMPLETE!
-- ===========================================
-- You can now test your API endpoints
