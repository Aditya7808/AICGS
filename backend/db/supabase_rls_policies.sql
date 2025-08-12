-- Row Level Security (RLS) Policies for CareerBuddy Supabase Database
-- These policies must be applied in the Supabase dashboard or via SQL editor

-- Drop existing policies first to avoid conflicts
DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;
DROP POLICY IF EXISTS "Users can view own profile" ON profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
DROP POLICY IF EXISTS "Users can delete own profile" ON profiles;

-- Enable RLS on profiles table
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Policy to allow authenticated users to insert their own profile
-- The profile id must match the authenticated user's id (auth.uid())
CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT 
    TO authenticated 
    WITH CHECK (auth.uid()::text = id::text);

-- Policy to allow authenticated users to select their own profile
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT 
    TO authenticated 
    USING (auth.uid()::text = id::text);

-- Policy to allow authenticated users to update their own profile
CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE 
    TO authenticated 
    USING (auth.uid()::text = id::text) 
    WITH CHECK (auth.uid()::text = id::text);

-- Policy to allow authenticated users to delete their own profile (optional)
CREATE POLICY "Users can delete own profile" ON profiles
    FOR DELETE 
    TO authenticated 
    USING (auth.uid()::text = id::text);

-- Additional debugging: Check current policies
SELECT 
    schemaname, 
    tablename, 
    policyname, 
    permissive, 
    roles, 
    cmd, 
    qual, 
    with_check 
FROM pg_policies 
WHERE tablename = 'profiles';

-- Check if RLS is enabled
SELECT 
    schemaname, 
    tablename, 
    rowsecurity 
FROM pg_tables 
WHERE tablename = 'profiles';

-- Enable RLS on user_profiles table if it exists
-- ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Policies for user_profiles (if the table exists)
-- CREATE POLICY "Users can insert own user_profile" ON user_profiles
--     FOR INSERT 
--     TO authenticated 
--     WITH CHECK (auth.uid() = user_id);

-- CREATE POLICY "Users can view own user_profile" ON user_profiles
--     FOR SELECT 
--     TO authenticated 
--     USING (auth.uid() = user_id);

-- CREATE POLICY "Users can update own user_profile" ON user_profiles
--     FOR UPDATE 
--     TO authenticated 
--     USING (auth.uid() = user_id) 
--     WITH CHECK (auth.uid() = user_id);

-- CREATE POLICY "Users can delete own user_profile" ON user_profiles
--     FOR DELETE 
--     TO authenticated 
--     USING (auth.uid() = user_id);

-- Note: Apply these policies in your Supabase dashboard SQL editor
-- Make sure to replace any existing conflicting policies first by dropping them:
-- DROP POLICY IF EXISTS "policy_name" ON table_name;
