#!/usr/bin/env python3
"""
Simple test server to verify Supabase connection
"""
from fastapi import FastAPI, HTTPException
import os
import sys
sys.path.insert(0, '.')

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set defaults only if not already set (for testing purposes)
if not os.getenv('SUPABASE_URL'):
    print("⚠️  No SUPABASE_URL found in environment. Please set up your .env file.")
if not os.getenv('SUPABASE_ANON_KEY'):
    print("⚠️  No SUPABASE_ANON_KEY found in environment. Please set up your .env file.")
if not os.getenv('DATABASE_URL'):
    print("⚠️  No DATABASE_URL found in environment. Please set up your .env file.")

app = FastAPI(title="CareerBuddy Test Server", version="2.0.0")

@app.get("/")
async def root():
    return {
        "message": "CareerBuddy API with Supabase - Manual Migration Test",
        "status": "running",
        "database": "Supabase PostgreSQL"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from supabase import create_client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            raise HTTPException(status_code=500, detail="Supabase credentials not configured")
        
        # Test Supabase connection
        supabase = create_client(supabase_url, supabase_key)
        
        # Try to fetch careers table (should exist after manual setup)
        result = supabase.table("careers").select("id,name").limit(1).execute()
        
        careers_count = len(result.data) if result.data else 0
        
        return {
            "status": "healthy",
            "database": "Supabase PostgreSQL",
            "connection": "success",
            "sample_careers": careers_count,
            "supabase_url": supabase_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/test-careers")
async def get_careers():
    """Test endpoint to fetch careers from Supabase"""
    try:
        from supabase import create_client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        supabase = create_client(supabase_url, supabase_key)
        result = supabase.table("careers").select("*").execute()
        
        return {
            "careers": result.data,
            "count": len(result.data) if result.data else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching careers: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003)
