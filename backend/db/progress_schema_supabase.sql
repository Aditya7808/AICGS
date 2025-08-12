-- Progress Tracking Schema for Supabase (PostgreSQL)
-- CareerBuddy Progress Management System

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS assessment_history CASCADE;
DROP TABLE IF EXISTS skill_progress CASCADE;
DROP TABLE IF EXISTS career_goals CASCADE;
DROP TABLE IF EXISTS user_progress CASCADE;

-- User progress tracking (main dashboard metrics)
CREATE TABLE user_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Assessment metrics
    total_assessments_completed INTEGER DEFAULT 0,
    last_assessment_date TIMESTAMPTZ,
    
    -- Goal and skill metrics
    career_goals_set INTEGER DEFAULT 0,
    skills_tracked INTEGER DEFAULT 0,
    
    -- Streaks and engagement
    current_streak_days INTEGER DEFAULT 0,
    longest_streak_days INTEGER DEFAULT 0,
    last_activity_date TIMESTAMPTZ DEFAULT NOW(),
    
    -- Completion scores (0.0 to 1.0)
    profile_completeness DECIMAL(3,2) DEFAULT 0.0 CHECK (profile_completeness >= 0.0 AND profile_completeness <= 1.0),
    skill_development_score DECIMAL(3,2) DEFAULT 0.0 CHECK (skill_development_score >= 0.0 AND skill_development_score <= 1.0),
    career_clarity_score DECIMAL(3,2) DEFAULT 0.0 CHECK (career_clarity_score >= 0.0 AND career_clarity_score <= 1.0),
    
    -- Milestones achieved (JSON array of milestone names)
    milestones_achieved JSONB DEFAULT '[]',
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(user_id)
);

-- Skill progress tracking
CREATE TABLE skill_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Skill information
    skill_name TEXT NOT NULL,
    current_level TEXT NOT NULL CHECK (current_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
    target_level TEXT NOT NULL CHECK (target_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
    
    -- Progress metrics
    proficiency_score DECIMAL(3,2) DEFAULT 0.0 CHECK (proficiency_score >= 0.0 AND proficiency_score <= 1.0),
    time_invested_hours DECIMAL(8,2) DEFAULT 0.0,
    
    -- Timeline
    target_date TIMESTAMPTZ,
    last_practice_date TIMESTAMPTZ,
    
    -- Progress tracking
    progress_history JSONB DEFAULT '[]', -- Array of {date, score, notes}
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(user_id, skill_name)
);

-- Career goals tracking
CREATE TABLE career_goals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Goal information
    career_id INTEGER NOT NULL, -- Reference to career from careers table
    goal_type TEXT NOT NULL CHECK (goal_type IN ('primary', 'secondary', 'exploratory', 'skill_development', 'certification', 'experience')),
    target_timeline TEXT NOT NULL CHECK (target_timeline IN ('3_months', '6_months', '1_year', '2_years', '5_years')),
    priority_level INTEGER NOT NULL CHECK (priority_level >= 1 AND priority_level <= 5),
    
    -- Status and progress
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'paused', 'cancelled')),
    progress_percentage DECIMAL(5,2) DEFAULT 0.0 CHECK (progress_percentage >= 0.0 AND progress_percentage <= 100.0),
    
    -- Required and completed skills
    required_skills TEXT[] DEFAULT '{}',
    completed_skills TEXT[] DEFAULT '{}',
    
    -- Learning plan and milestones
    learning_plan JSONB DEFAULT '[]', -- Array of learning steps
    milestones JSONB DEFAULT '[]',   -- Array of milestone objects
    
    -- Links and resources
    links JSONB DEFAULT '[]', -- Array of helpful links
    
    -- Actions and notes
    next_action TEXT,
    notes TEXT,
    
    -- Timeline
    target_completion_date TIMESTAMPTZ,
    actual_completion_date TIMESTAMPTZ,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Assessment history tracking
CREATE TABLE assessment_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Assessment information
    assessment_type TEXT NOT NULL CHECK (assessment_type IN ('skill', 'personality', 'interest', 'career_fit', 'comprehensive')),
    assessment_name TEXT NOT NULL,
    
    -- Results
    overall_score DECIMAL(5,2),
    detailed_results JSONB DEFAULT '{}', -- Store structured results
    recommendations JSONB DEFAULT '[]', -- Generated recommendations
    
    -- Metadata
    duration_minutes INTEGER,
    completion_rate DECIMAL(3,2) DEFAULT 1.0,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance optimization
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_user_progress_last_activity ON user_progress(last_activity_date);

CREATE INDEX idx_skill_progress_user_id ON skill_progress(user_id);
CREATE INDEX idx_skill_progress_skill_name ON skill_progress(skill_name);
CREATE INDEX idx_skill_progress_level ON skill_progress(current_level, target_level);

CREATE INDEX idx_career_goals_user_id ON career_goals(user_id);
CREATE INDEX idx_career_goals_status ON career_goals(status);
CREATE INDEX idx_career_goals_priority ON career_goals(priority_level);
CREATE INDEX idx_career_goals_career_id ON career_goals(career_id);

CREATE INDEX idx_assessment_history_user_id ON assessment_history(user_id);
CREATE INDEX idx_assessment_history_type ON assessment_history(assessment_type);
CREATE INDEX idx_assessment_history_created_at ON assessment_history(created_at);

-- Enable Row Level Security (RLS)
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE skill_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE career_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessment_history ENABLE ROW LEVEL SECURITY;

-- Create RLS Policies - Users can only access their own data
CREATE POLICY "Users can view own progress" ON user_progress FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own progress" ON user_progress FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own progress" ON user_progress FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own skill_progress" ON skill_progress FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own skill_progress" ON skill_progress FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own skill_progress" ON skill_progress FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own skill_progress" ON skill_progress FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own career_goals" ON career_goals FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own career_goals" ON career_goals FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own career_goals" ON career_goals FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own career_goals" ON career_goals FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own assessment_history" ON assessment_history FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own assessment_history" ON assessment_history FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Triggers for updated_at timestamps
CREATE TRIGGER update_user_progress_updated_at BEFORE UPDATE ON user_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_skill_progress_updated_at BEFORE UPDATE ON skill_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_career_goals_updated_at BEFORE UPDATE ON career_goals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Functions for automatic progress updates
CREATE OR REPLACE FUNCTION update_progress_metrics()
RETURNS TRIGGER AS $$
BEGIN
    -- Update user_progress when skills or goals change
    INSERT INTO user_progress (user_id) 
    VALUES (NEW.user_id)
    ON CONFLICT (user_id) 
    DO UPDATE SET
        career_goals_set = (
            SELECT COUNT(*) FROM career_goals 
            WHERE user_id = NEW.user_id AND status != 'cancelled'
        ),
        skills_tracked = (
            SELECT COUNT(*) FROM skill_progress 
            WHERE user_id = NEW.user_id
        ),
        updated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update progress metrics when skills or goals change
CREATE TRIGGER update_progress_on_skill_change
    AFTER INSERT OR UPDATE OR DELETE ON skill_progress
    FOR EACH ROW EXECUTE FUNCTION update_progress_metrics();

CREATE TRIGGER update_progress_on_goal_change
    AFTER INSERT OR UPDATE OR DELETE ON career_goals
    FOR EACH ROW EXECUTE FUNCTION update_progress_metrics();

-- Views for analytics and reporting
CREATE VIEW user_progress_dashboard AS
SELECT 
    up.user_id,
    up.total_assessments_completed,
    up.last_assessment_date,
    up.career_goals_set,
    up.skills_tracked,
    up.current_streak_days,
    up.longest_streak_days,
    up.profile_completeness,
    up.skill_development_score,
    up.career_clarity_score,
    up.milestones_achieved,
    COUNT(DISTINCT sp.id) as active_skills,
    COUNT(DISTINCT cg.id) as active_goals,
    COALESCE(AVG(sp.proficiency_score), 0) as avg_skill_score,
    COALESCE(AVG(cg.progress_percentage), 0) as avg_goal_progress
FROM user_progress up
LEFT JOIN skill_progress sp ON up.user_id = sp.user_id
LEFT JOIN career_goals cg ON up.user_id = cg.user_id AND cg.status = 'active'
GROUP BY up.user_id, up.total_assessments_completed, up.last_assessment_date, 
         up.career_goals_set, up.skills_tracked, up.current_streak_days, 
         up.longest_streak_days, up.profile_completeness, 
         up.skill_development_score, up.career_clarity_score, up.milestones_achieved;

CREATE VIEW skill_progress_summary AS
SELECT 
    sp.user_id,
    sp.skill_name,
    sp.current_level,
    sp.target_level,
    sp.proficiency_score,
    sp.time_invested_hours,
    sp.target_date,
    sp.last_practice_date,
    sp.created_at,
    sp.updated_at,
    CASE 
        WHEN sp.target_date < NOW() AND sp.current_level != sp.target_level THEN 'overdue'
        WHEN sp.target_date <= NOW() + INTERVAL '30 days' THEN 'due_soon'
        ELSE 'on_track'
    END as timeline_status
FROM skill_progress sp;

-- Sample data for testing (optional)
-- This would be populated by the application in production
