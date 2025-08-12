from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth_supabase, recommend, mare_supabase, progress, education
from .db.supabase_client import supabase_manager
from .logic.data_processor import load_training_data
from .core.config import Settings
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load settings
settings = Settings()

app = FastAPI(title="CareerBuddyAPI", version="2.0.0")

# Configure CORS - more restrictive for production
allowed_origins = [
    'https://aicgs-live.onrender.com'
]

# Add wildcard only in development
if settings.debug:
    allowed_origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers - using Supabase auth
app.include_router(auth_supabase.router)
app.include_router(recommend.router)
app.include_router(mare_supabase.router, prefix="/api/v1", tags=["mare"])
app.include_router(progress.router)
app.include_router(education.router, prefix="/api/education", tags=["education"])

# Include ML routes for skill gap prioritization
try:
    from .api import ml_routes
    app.include_router(ml_routes.router, prefix="/api/v1")
    logger.info("ML Skill Prioritization API included successfully")
except ImportError as e:
    logger.warning(f"ML Skill Prioritization API not available: {e}")
except Exception as e:
    logger.error(f"Failed to include ML Skill Prioritization API: {e}")

# Include CAST Framework router
try:
    from .api import cast_api
    app.include_router(cast_api.router)
    logger.info("CAST Framework API included successfully")
except ImportError as e:
    logger.warning(f"CAST Framework API not available: {e}")
except Exception as e:
    logger.error(f"Failed to include CAST Framework API: {e}")

@app.on_event("startup")
async def startup_event():
    """Initialize Supabase connection and sample data on startup"""
    logger.info("Starting CareerBuddyAPI v2.0 with Supabase...")
    
    try:
        # Initialize Supabase manager
        supabase_manager.initialize()
        logger.info("Supabase connection established successfully")
        
        # Initialize sample data if needed
        await initialize_sample_data()
        logger.info("Sample data initialized")
        
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
        logger.error(f"Startup error: {e}")
        raise e
    
    logger.info("CareerBuddyAPI startup completed")

async def initialize_sample_data():
    """Initialize sample data in Supabase"""
    try:
        from .db.mare_crud_supabase import MAReCRUDSupabase
        
        mare_crud = MAReCRUDSupabase()
        
        # Check if careers exist, if not create sample ones
        careers = mare_crud.supabase.table("careers").select("id").limit(1).execute()
        if not careers.data:
            logger.info("Creating sample careers in Supabase...")
            await create_sample_careers_supabase(mare_crud)
        
        logger.info("Sample data initialization completed")
        
    except Exception as e:
        logger.error(f"Error initializing sample data: {e}")

async def create_sample_careers_supabase(mare_crud):
    """Create sample careers in Supabase"""
    sample_careers = [
        {
            "name": "Software Developer",
            "description_en": "Develops software applications and systems using various programming languages.",
            "description_hi": "विभिन्न प्रोग्रामिंग भाषाओं का उपयोग करके सॉफ्टवेयर एप्लिकेशन और सिस्टम विकसित करता है।",
            "required_skills": "Coding,Problem Solving,Programming,Logic",
            "interests": "Technology,Coding,Innovation",
            "local_demand": "High",
            "category": "Technology",
            "subcategory": "Software Development",
            "min_education_level": "Bachelor's Degree",
            "preferred_subjects": "Computer Science, Mathematics",
            "average_salary_range": "5-12 LPA",
            "growth_prospects": "Excellent"
        },
        {
            "name": "Data Scientist",
            "description_en": "Analyzes complex data to help businesses make informed decisions using statistical methods and machine learning.",
            "description_hi": "सांख्यिकीय विधियों और मशीन लर्निंग का उपयोग करके व्यवसायों को सूचित निर्णय लेने में मदद करने के लिए जटिल डेटा का विश्लेषण करता है।",
            "required_skills": "Analytics,Statistics,Python,Machine Learning,Data Visualization",
            "interests": "Technology,Analysis,Research,Mathematics",
            "local_demand": "High",
            "category": "Technology",
            "subcategory": "Data Science",
            "min_education_level": "Bachelor's Degree",
            "preferred_subjects": "Statistics, Computer Science, Mathematics",
            "average_salary_range": "8-20 LPA",
            "growth_prospects": "Excellent"
        },
        {
            "name": "UI/UX Designer",
            "description_en": "Creates user-friendly and appealing designs for websites and applications.",
            "description_hi": "वेबसाइट और एप्लिकेशन के लिए उपयोगकर्ता-अनुकूल और आकर्षक डिज़ाइन बनाता है।",
            "required_skills": "Design,Creativity,User Research,Prototyping,Figma,Adobe Creative Suite",
            "interests": "Design,Technology,Art,Psychology",
            "local_demand": "High",
            "category": "Design",
            "subcategory": "User Experience",
            "min_education_level": "Bachelor's Degree",
            "preferred_subjects": "Design, Psychology, Computer Science",
            "average_salary_range": "4-10 LPA",
            "growth_prospects": "Good"
        }
    ]
    
    try:
        result = mare_crud.supabase.table("careers").insert(sample_careers).execute()
        logger.info(f"Created {len(result.data)} sample careers")
    except Exception as e:
        logger.error(f"Error creating sample careers: {e}")

@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "message": "CareerBuddy API v2.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms like Render"""
    return {"status": "healthy", "service": "CareerBuddyAPI", "version": "2.0.0"}

@app.get("/api/stats")
async def get_api_stats():
    """Get API statistics from Supabase"""
    try:
        from .db.mare_crud_supabase import MAReCRUDSupabase
        
        mare_crud = MAReCRUDSupabase()
        
        # Get counts from Supabase tables
        stats = {}
        
        # Get careers count
        careers_result = mare_crud.supabase.table("careers").select("id").execute()
        stats["careers"] = len(careers_result.data) if careers_result.data else 0
        
        # Get profiles count
        profiles_result = mare_crud.supabase.table("profiles").select("id").execute()
        stats["profiles"] = len(profiles_result.data) if profiles_result.data else 0
        
        # Get user profiles count
        user_profiles_result = mare_crud.supabase.table("user_profiles").select("id").execute()
        stats["user_profiles"] = len(user_profiles_result.data) if user_profiles_result.data else 0
        
        return {
            "database": "Supabase PostgreSQL",
            "statistics": stats,
            "api_version": "2.0.0"
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {"error": "Unable to fetch statistics", "message": str(e)}
