from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, recommend
from .db.base import create_tables
from .db.crud import create_sample_careers
from .db.base import SessionLocal
from .logic.data_processor import load_training_data
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CareerBuddyAPI", version="2.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev servers
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(recommend.router)

# Import and include progress router
from .api import progress
app.include_router(progress.router)

# Import and include education router
from .api import education
app.include_router(education.router, prefix="/api/education", tags=["education"])

@app.on_event("startup")
async def startup_event():
    """Initialize database and sample data on startup"""
    logger.info("Starting CareerBuddyAPI v2.0...")
    
    # Create tables
    create_tables()
    logger.info("Database tables created successfully")
    
    # Create sample careers if they don't exist
    db = SessionLocal()
    try:
        create_sample_careers(db)
        logger.info("Sample careers initialized")
        
        # Create sample education pathways
        from .db.crud_improved import create_sample_education_pathways
        create_sample_education_pathways(db)
        logger.info("Sample education pathways initialized")
        
        # Load training data from CSV if file exists
        csv_path = "data.csv"
        if os.path.exists(csv_path):
            try:
                loaded_counts = load_training_data(csv_path)
                logger.info(f"Training data loaded: {loaded_counts}")
            except Exception as e:
                logger.error(f"Failed to load training data: {e}")
        else:
            logger.warning(f"Training data file {csv_path} not found")
            
    except Exception as e:
        logger.error(f"Startup error: {e} ")
    finally:
        db.close()
    
    logger.info("CareerBuddyAPI startup completed")

@app.get("/")
async def root():
    return {"message": "Welcome to CareerBuddyAPI v2.0 - Enhanced with AI Recommendations"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

@app.get("/api/stats")
async def get_api_stats():
    """Get API statistics"""
    db = SessionLocal()
    try:
        from .models.user import User, UserProfile
        from .models.career import Career
        from .models.interaction import CareerOutcome, UserInteraction, AssessmentHistory
        
        stats = {
            "users": db.query(User).count(),
            "user_profiles": db.query(UserProfile).count(),
            "careers": db.query(Career).count(),
            "career_outcomes": db.query(CareerOutcome).count(),
            "user_interactions": db.query(UserInteraction).count(),
            "assessments": db.query(AssessmentHistory).count()
        }
        return stats
    finally:
        db.close()
