"""
Education pathways API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from ..db.base import get_db
from ..models.education import EducationPathway, Course, Institution, InstitutionPathway, AdmissionProcess
from ..models.career import Career

router = APIRouter()

# Pydantic models for requests and responses
class CourseResponse(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    credits: Optional[int] = None
    semester: Optional[int] = None
    description: Optional[str] = None
    topics_covered: Optional[List[str]] = None
    skills_gained: Optional[List[str]] = None
    course_type: Optional[str] = None
    delivery_mode: Optional[str] = None
    assessment_methods: Optional[List[str]] = None
    
    class Config:
        from_attributes = True

class InstitutionResponse(BaseModel):
    id: int
    name: str
    short_name: Optional[str] = None
    institution_type: Optional[str] = None
    category: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    website: Optional[str] = None
    ranking_national: Optional[int] = None
    ranking_global: Optional[int] = None
    facilities: Optional[List[str]] = None
    
    class Config:
        from_attributes = True

class EducationPathwayResponse(BaseModel):
    id: int
    career_id: int
    pathway_name: str
    pathway_type: str
    description: Optional[str] = None
    duration_months: Optional[int] = None
    difficulty_level: Optional[str] = None
    min_education_level: Optional[str] = None
    required_subjects: Optional[List[str]] = None
    min_percentage: Optional[float] = None
    entrance_exams: Optional[List[str]] = None
    estimated_cost_min: Optional[float] = None
    estimated_cost_max: Optional[float] = None
    financial_aid_available: bool = False
    scholarship_opportunities: Optional[List[str]] = None
    average_placement_rate: Optional[float] = None
    average_starting_salary: Optional[float] = None
    top_recruiting_companies: Optional[List[str]] = None
    popularity_score: float = 0.0
    success_rate: float = 0.0
    
    class Config:
        from_attributes = True

class InstitutionPathwayResponse(BaseModel):
    id: int
    institution: InstitutionResponse
    pathway: EducationPathwayResponse
    program_name: Optional[str] = None
    fees_per_year: Optional[float] = None
    duration_years: Optional[float] = None
    entrance_exams_accepted: Optional[List[str]] = None
    cutoff_scores: Optional[Dict[str, Any]] = None
    seats_available: Optional[int] = None
    placement_statistics: Optional[Dict[str, Any]] = None
    application_fee: Optional[float] = None
    
    class Config:
        from_attributes = True

class AdmissionProcessResponse(BaseModel):
    id: int
    process_name: str
    process_type: str
    application_start_date: Optional[str] = None
    application_end_date: Optional[str] = None
    exam_dates: Optional[List[str]] = None
    result_declaration_date: Optional[str] = None
    eligibility_criteria: Optional[Dict[str, Any]] = None
    required_documents: Optional[List[str]] = None
    exam_pattern: Optional[Dict[str, Any]] = None
    syllabus: Optional[Dict[str, Any]] = None
    recommended_preparation_time: Optional[int] = None
    preparation_resources: Optional[Dict[str, Any]] = None
    difficulty_level: Optional[str] = None
    success_tips: Optional[List[str]] = None
    
    class Config:
        from_attributes = True

class EducationPathwaysRequest(BaseModel):
    career_id: int
    education_level: Optional[str] = None  # Filter by education level
    budget_max: Optional[float] = None     # Filter by budget
    location_preference: Optional[str] = None  # Filter by location
    pathway_type: Optional[str] = None     # Filter by pathway type

@router.get("/pathways/{career_id}", response_model=List[EducationPathwayResponse])
async def get_education_pathways(
    career_id: int,
    education_level: Optional[str] = Query(None),
    budget_max: Optional[float] = Query(None),
    pathway_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get education pathways for a specific career
    """
    # Verify career exists
    career = db.query(Career).filter(Career.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    
    # Base query
    query = db.query(EducationPathway).filter(EducationPathway.career_id == career_id)
    
    # Apply filters
    if education_level:
        query = query.filter(EducationPathway.min_education_level == education_level)
    
    if budget_max:
        query = query.filter(EducationPathway.estimated_cost_max <= budget_max)
    
    if pathway_type:
        query = query.filter(EducationPathway.pathway_type == pathway_type)
    
    # Order by popularity and success rate
    pathways = query.order_by(
        EducationPathway.popularity_score.desc(),
        EducationPathway.success_rate.desc()
    ).all()
    
    return pathways

@router.get("/pathways/{pathway_id}/courses", response_model=List[CourseResponse])
async def get_pathway_courses(
    pathway_id: int,
    db: Session = Depends(get_db)
):
    """
    Get courses for a specific education pathway
    """
    # Verify pathway exists
    pathway = db.query(EducationPathway).filter(EducationPathway.id == pathway_id).first()
    if not pathway:
        raise HTTPException(status_code=404, detail="Education pathway not found")
    
    courses = db.query(Course).filter(
        Course.pathway_id == pathway_id
    ).order_by(Course.semester, Course.name).all()
    
    return courses

@router.get("/pathways/{pathway_id}/institutions")
async def get_pathway_institutions(
    pathway_id: int,
    location_filter: Optional[str] = Query(None),
    ranking_min: Optional[int] = Query(None),
    fees_max: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get institutions offering a specific education pathway
    """
    # Verify pathway exists
    pathway = db.query(EducationPathway).filter(EducationPathway.id == pathway_id).first()
    if not pathway:
        raise HTTPException(status_code=404, detail="Education pathway not found")
    
    # Get institution pathway mappings
    institution_pathways = db.query(InstitutionPathway).filter(
        InstitutionPathway.pathway_id == pathway_id
    ).all()
    
    # Build response with complete data
    results = []
    for ip in institution_pathways:
        institution = db.query(Institution).filter(Institution.id == ip.institution_id).first()
        if institution:
            institution_data = {
                "id": institution.id,
                "name": institution.name or "",
                "short_name": institution.short_name or "",
                "institution_type": institution.institution_type or "",
                "category": institution.category or "",
                "city": institution.city or "",
                "state": institution.state or "",
                "website": institution.website or "",
                "ranking_national": institution.ranking_national,
                "ranking_global": institution.ranking_global,
                "facilities": institution.facilities or []
            }
            
            pathway_data = {
                "id": pathway.id,
                "career_id": pathway.career_id,
                "pathway_name": pathway.pathway_name or "",
                "pathway_type": pathway.pathway_type or "",
                "description": pathway.description or "",
                "duration_months": pathway.duration_months,
                "difficulty_level": pathway.difficulty_level or "",
                "min_education_level": pathway.min_education_level or "",
                "required_subjects": pathway.required_subjects or [],
                "min_percentage": pathway.min_percentage,
                "entrance_exams": pathway.entrance_exams or [],
                "estimated_cost_min": pathway.estimated_cost_min,
                "estimated_cost_max": pathway.estimated_cost_max,
                "financial_aid_available": pathway.financial_aid_available or False,
                "scholarship_opportunities": pathway.scholarship_opportunities or [],
                "average_placement_rate": pathway.average_placement_rate,
                "average_starting_salary": pathway.average_starting_salary,
                "top_recruiting_companies": pathway.top_recruiting_companies or [],
                "popularity_score": pathway.popularity_score or 0.0,
                "success_rate": pathway.success_rate or 0.0
            }
            
            results.append({
                "id": ip.id,
                "institution": institution_data,
                "pathway": pathway_data,
                "program_name": ip.program_name or "",
                "fees_per_year": ip.fees_per_year,
                "duration_years": ip.duration_years,
                "entrance_exams_accepted": ip.entrance_exams_accepted or [],
                "cutoff_scores": ip.cutoff_scores or {},
                "seats_available": ip.seats_available,
                "placement_statistics": ip.placement_statistics or {},
                "application_fee": ip.application_fee
            })
    
    return results

@router.get("/institutions/{institution_id}/admission-process", response_model=List[AdmissionProcessResponse])
async def get_admission_processes(
    institution_id: int,
    pathway_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get admission processes for an institution
    """
    # Base query
    query = db.query(AdmissionProcess).join(InstitutionPathway).filter(
        InstitutionPathway.institution_id == institution_id
    )
    
    # Filter by pathway if specified
    if pathway_id:
        query = query.filter(InstitutionPathway.pathway_id == pathway_id)
    
    processes = query.order_by(AdmissionProcess.process_name).all()
    
    return processes

@router.get("/recommendations", response_model=Dict[str, Any])
async def get_personalized_education_recommendations(
    career_ids: List[int] = Query(...),
    current_education: str = Query(...),
    budget_range: str = Query(...),  # "low", "medium", "high"
    location_preference: Optional[str] = Query(None),
    db: Session = Depends(get_db)
    # Note: Authentication can be added later if needed
):
    """
    Get personalized education recommendations based on user profile and preferences
    """
    recommendations = {
        "recommended_pathways": [],
        "budget_analysis": {},
        "timeline_analysis": {},
        "success_probability": {},
        "alternative_options": []
    }
    
    # Budget mapping
    budget_mapping = {
        "low": (0, 200000),      # Up to 2 lakhs
        "medium": (200000, 800000),  # 2-8 lakhs  
        "high": (800000, float('inf'))  # Above 8 lakhs
    }
    
    budget_min, budget_max = budget_mapping.get(budget_range, (0, float('inf')))
    
    for career_id in career_ids:
        # Get pathways for this career
        query = db.query(EducationPathway).filter(EducationPathway.career_id == career_id)
        
        # Filter by budget
        if budget_max != float('inf'):
            query = query.filter(EducationPathway.estimated_cost_max <= budget_max)
        
        pathways = query.order_by(
            EducationPathway.success_rate.desc(),
            EducationPathway.popularity_score.desc()
        ).limit(3).all()
        
        for pathway in pathways:
            # Get top institutions for this pathway
            institutions = db.query(InstitutionPathway).filter(
                InstitutionPathway.pathway_id == pathway.id,
                InstitutionPathway.is_active == True
            ).join(Institution).order_by(
                Institution.ranking_national.asc()
            ).limit(5).all()
            
            pathway_data = {
                "pathway": EducationPathwayResponse.from_orm(pathway),
                "top_institutions": []
            }
            
            for ip in institutions:
                institution = db.query(Institution).filter(Institution.id == ip.institution_id).first()
                if institution:
                    pathway_data["top_institutions"].append({
                        "institution": {
                            "id": institution.id,
                            "name": institution.name,
                            "short_name": institution.short_name,
                            "institution_type": institution.institution_type,
                            "category": institution.category,
                            "city": institution.city,
                            "state": institution.state,
                            "website": institution.website,
                            "ranking_national": institution.ranking_national,
                            "ranking_global": institution.ranking_global,
                            "facilities": institution.facilities
                        },
                        "fees_per_year": ip.fees_per_year,
                        "entrance_exams": ip.entrance_exams_accepted,
                        "placement_rate": 85  # Default value for now
                    })
            
            recommendations["recommended_pathways"].append(pathway_data)
    
    # Budget analysis
    recommendations["budget_analysis"] = {
        "selected_range": budget_range,
        "average_cost": budget_min + (budget_max - budget_min) / 2 if budget_max != float('inf') else budget_min + 400000,
        "cost_breakdown": {
            "tuition_fees": "60-80%",
            "living_expenses": "15-25%", 
            "books_materials": "3-5%",
            "miscellaneous": "5-10%"
        },
        "financial_aid_options": [
            "Merit-based scholarships",
            "Need-based financial aid", 
            "Education loans",
            "Government schemes"
        ]
    }
    
    # Timeline analysis
    recommendations["timeline_analysis"] = {
        "preparation_phase": "6-12 months for entrance exams",
        "application_phase": "3-6 months for applications and admissions",
        "study_duration": "varies by pathway (1-4 years typically)",
        "total_timeline": "2-5 years from start to career entry"
    }
    
    return recommendations

@router.get("/entrance-exams", response_model=List[Dict[str, Any]])
async def get_entrance_exams_info(
    exam_names: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about entrance exams
    """
    # This would typically come from a dedicated entrance exams table
    # For now, we'll return sample data structure
    exams_info = [
        {
            "name": "JEE Main",
            "full_name": "Joint Entrance Examination Main",
            "conducting_authority": "National Testing Agency (NTA)",
            "exam_type": "Computer Based Test",
            "subjects": ["Physics", "Chemistry", "Mathematics"],
            "duration": "3 hours",
            "total_marks": 300,
            "exam_dates": ["January 2025", "April 2025"],
            "application_fee": 650,
            "eligibility": {
                "min_education": "12th with PCM",
                "min_percentage": 75,
                "age_limit": "No age limit",
                "attempts_allowed": "Unlimited"
            },
            "preparation_tips": [
                "Focus on NCERT textbooks",
                "Practice previous year papers",
                "Take mock tests regularly",
                "Strong conceptual understanding"
            ],
            "accepted_by": ["NITs", "IIITs", "CFTIs", "State Engineering Colleges"],
            "difficulty_level": "High"
        },
        {
            "name": "JEE Advanced", 
            "full_name": "Joint Entrance Examination Advanced",
            "conducting_authority": "IIT (Rotating)",
            "exam_type": "Computer Based Test",
            "subjects": ["Physics", "Chemistry", "Mathematics"],
            "duration": "6 hours (2 papers of 3 hours each)",
            "total_marks": 372,
            "exam_dates": ["May 2025"],
            "application_fee": 2800,
            "eligibility": {
                "min_education": "Qualified JEE Main",
                "top_rank_criteria": "Top 2,50,000 in JEE Main",
                "age_limit": "Maximum 5 years gap after 12th",
                "attempts_allowed": "Maximum 2 attempts"
            },
            "preparation_tips": [
                "Deep conceptual understanding",
                "Advanced problem solving",
                "Time management skills", 
                "Previous year analysis"
            ],
            "accepted_by": ["IITs", "IISc", "IISER"],
            "difficulty_level": "Very High"
        }
    ]
    
    if exam_names:
        exams_info = [exam for exam in exams_info if exam["name"] in exam_names]
    
    return exams_info

@router.get("/debug/pathways")
async def debug_pathways(db: Session = Depends(get_db)):
    """Debug endpoint to check pathway data"""
    pathways = db.query(EducationPathway).all()
    return {"count": len(pathways), "pathways": [{"id": p.id, "name": p.pathway_name} for p in pathways]}

@router.get("/debug/institutions")
async def debug_institutions(db: Session = Depends(get_db)):
    """Debug endpoint to check institution data"""
    institutions = db.query(Institution).all()
    return {"count": len(institutions), "institutions": [{"id": i.id, "name": i.name} for i in institutions]}

@router.get("/debug/institution-pathways")
async def debug_institution_pathways(db: Session = Depends(get_db)):
    """Debug endpoint to check institution-pathway data"""
    ips = db.query(InstitutionPathway).all()
    return {"count": len(ips), "mappings": [{"id": ip.id, "institution_id": ip.institution_id, "pathway_id": ip.pathway_id} for ip in ips]}

@router.get("/pathways/{pathway_id}/institutions-simple")
async def get_pathway_institutions_simple(pathway_id: int, db: Session = Depends(get_db)):
    """
    Simple version to test institutions endpoint
    """
    # Get institution pathway mappings
    institution_pathways = db.query(InstitutionPathway).filter(
        InstitutionPathway.pathway_id == pathway_id
    ).all()
    
    return {
        "pathway_id": pathway_id,
        "count": len(institution_pathways),
        "raw_data": [{"id": ip.id, "institution_id": ip.institution_id, "program_name": ip.program_name} for ip in institution_pathways]
    }

@router.get("/pathways/{pathway_id}/institutions-raw")
async def get_pathway_institutions_raw(pathway_id: int, db: Session = Depends(get_db)):
    """
    Raw version to test without complex response structure
    """
    # Get institution pathway mappings
    institution_pathways = db.query(InstitutionPathway).filter(
        InstitutionPathway.pathway_id == pathway_id
    ).all()
    
    results = []
    for ip in institution_pathways:
        institution = db.query(Institution).filter(Institution.id == ip.institution_id).first()
        if institution:
            results.append({
                "ip_id": ip.id,
                "institution_name": institution.name,
                "program_name": ip.program_name,
                "fees": ip.fees_per_year
            })
    
    return {"results": results}

# Existing endpoints below...
