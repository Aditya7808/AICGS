#!/usr/bin/env python3
"""
MARE Supabase Setup Script
Sets up the Supabase database for MARE system
"""

import os
import sys
from pathlib import Path
import logging
from supabase import create_client, Client
from typing import Optional

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_supabase_database():
    """Set up Supabase database with MARE schema"""
    
    # Get environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Use service role key for admin operations
    
    if not supabase_url or not supabase_key:
        print("❌ Missing required environment variables:")
        print("   - SUPABASE_URL")
        print("   - SUPABASE_SERVICE_ROLE_KEY")
        print("\nPlease set these in your .env file or environment")
        return False
    
    try:
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print(f"✅ Connected to Supabase: {supabase_url}")
        
        # Get the directory of this script
        script_dir = Path(__file__).parent
        schema_file = script_dir / "db" / "mare_schema_supabase.sql"
        
        if not schema_file.exists():
            print(f"❌ Schema file not found: {schema_file}")
            print("Please make sure mare_schema_supabase.sql exists in the db/ directory")
            return False
        
        print(f"📁 Reading schema from: {schema_file}")
        
        # Read schema file
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Execute schema using Supabase RPC (for complex SQL)
        print("🚀 Executing schema setup...")
        
        # Split schema into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements):
            if statement and not statement.startswith('--'):
                try:
                    # Use raw SQL execution through Supabase
                    result = supabase.postgrest.rpc('exec_sql', {'sql': statement}).execute()
                    logger.debug(f"Executed statement {i+1}/{len(statements)}")
                except Exception as e:
                    logger.warning(f"Statement {i+1} failed (may be expected): {str(e)[:100]}")
                    continue
        
        print("✅ Database schema setup completed!")
        
        # Verify setup by checking tables
        try:
            tables = supabase.table('user_profiles').select('count').execute()
            print("📊 Schema verification successful")
        except Exception as e:
            print(f"⚠️  Schema verification warning: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        return False

def test_database_connection():
    """Test the database connection and basic queries"""
    
    try:
        from app.db.mare_crud_supabase import get_mare_crud_supabase
        
        print("🧪 Testing database connection...")
        crud = get_mare_crud_supabase()
        
        # Test getting career opportunities
        opportunities = crud.get_career_opportunities(limit=5)
        print(f"✅ Successfully retrieved {len(opportunities)} career opportunities")
        
        # Test analytics query
        analytics = crud.get_recommendation_analytics(30)
        print(f"✅ Analytics query successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

def setup_environment():
    """Check and setup environment configuration"""
    
    env_file = Path(".env")
    example_file = Path(".env.example")
    
    if not env_file.exists():
        if example_file.exists():
            print("📄 Copying .env.example to .env")
            with open(example_file) as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print("⚠️  Please update the .env file with your Supabase credentials")
            return False
        else:
            print("❌ No .env.example file found")
            return False
    
    # Load environment variables
    try:
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print("✅ Environment variables loaded")
        return True
    except Exception as e:
        print(f"❌ Error loading environment: {e}")
        return False

def main():
    """Main setup function"""
    
    print("🚀 MARE Supabase Database Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("app"):
        print("❌ Please run this script from the backend directory")
        print("Current directory:", os.getcwd())
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Environment setup failed")
        print("Please ensure you have:")
        print("1. A .env file with your Supabase credentials")
        print("2. SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY set")
        sys.exit(1)
    
    # Setup database
    print("\n" + "=" * 40)
    if not setup_supabase_database():
        print("\n❌ Database setup failed")
        sys.exit(1)
    
    # Test connection
    print("\n" + "=" * 40)
    if test_database_connection():
        print("\n🎉 MARE Supabase setup completed successfully!")
        print("\nNext steps:")
        print("1. Verify your .env file has correct Supabase credentials")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Start the server: uvicorn app.main:app --reload")
        print("4. Test the API at: http://localhost:8000/docs")
    else:
        print("\n⚠️  Setup completed but database test failed")
        print("Please check your Supabase connection and credentials")

if __name__ == "__main__":
    main()
