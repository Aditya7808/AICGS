-- Careers Table Schema for Supabase
-- This table stores career opportunities and job information for the recommendation system

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing careers table if it exists
DROP TABLE IF EXISTS careers CASCADE;

-- Create careers table
CREATE TABLE careers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),  -- Technology, Healthcare, Finance, etc.
    subcategory VARCHAR(50),  -- Software Development, Data Science, etc.
    
    -- Descriptions
    description_en VARCHAR(500) NOT NULL,
    description_hi VARCHAR(500) NOT NULL,
    
    -- Requirements
    required_skills TEXT[],  -- Array of required skills
    interests TEXT[],  -- Array of interests
    min_education_level VARCHAR(50),
    preferred_subjects VARCHAR(200),
    
    -- Additional fields that might be referenced
    title VARCHAR(100),  -- Alternative name field
    skills_required TEXT,  -- Alternative to required_skills (comma-separated)
    education_required TEXT,  -- Education requirements
    experience_required TEXT,  -- Experience requirements
    certifications TEXT,  -- Required certifications
    
    -- Academic requirements
    min_percentage_10th DECIMAL(5,2) DEFAULT 0.0,
    min_percentage_12th DECIMAL(5,2) DEFAULT 0.0,
    min_cgpa DECIMAL(3,2) DEFAULT 0.0,
    
    -- Market information
    local_demand VARCHAR(20) DEFAULT 'Medium',  -- High, Medium, Low
    average_salary_range VARCHAR(50),  -- "3-6 LPA", "10-15 LPA"
    growth_prospects VARCHAR(20) DEFAULT 'Good',  -- Excellent, Good, Average
    
    -- Success metrics from training data
    placement_success_rate DECIMAL(5,2) DEFAULT 0.0,
    peer_popularity_score DECIMAL(5,2) DEFAULT 0.0,
    satisfaction_rating DECIMAL(3,2) DEFAULT 0.0,
    
    -- Industry information
    top_companies JSONB,  -- List of companies hiring for this role
    typical_job_roles JSONB,  -- List of typical job titles
    career_progression_path JSONB,  -- Career advancement steps
    
    -- Educational pathways
    recommended_courses JSONB,  -- Degree programs, certifications
    
    -- Status and metadata
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_careers_category ON careers(category);
CREATE INDEX idx_careers_subcategory ON careers(subcategory);
CREATE INDEX idx_careers_min_education_level ON careers(min_education_level);
CREATE INDEX idx_careers_local_demand ON careers(local_demand);
CREATE INDEX idx_careers_is_active ON careers(is_active);
CREATE INDEX idx_careers_required_skills ON careers USING GIN(required_skills);
CREATE INDEX idx_careers_interests ON careers USING GIN(interests);

-- Add RLS (Row Level Security) if needed
ALTER TABLE careers ENABLE ROW LEVEL SECURITY;

-- Create policy to allow read access to all authenticated users
CREATE POLICY "Allow read access to careers" ON careers FOR SELECT TO authenticated USING (true);

-- Create policy to allow insert/update for service role (for data management)
CREATE POLICY "Allow full access to service role" ON careers FOR ALL TO service_role USING (true);
