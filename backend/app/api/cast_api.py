"""
CAST Framework API Endpoints
============================

REST API endpoints for the Context-Aware Skills Translation Framework
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging

from ..logic.cast_integration import CASTIntegratedMatcher
from ..core.config import get_settings

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/cast", tags=["CAST Framework"])

# Initialize CAST Framework
cast_matcher = None

def get_cast_matcher() -> CASTIntegratedMatcher:
    """Get CAST matcher instance"""
    global cast_matcher
    if cast_matcher is None:
        settings = get_settings()
        cast_config = {
            "multilingual": {
                "preferred_model": "hybrid",
                "min_quality_threshold": 0.7
            },
            "cultural": {
                "preserve_context": True,
                "adaptation_level": "high"
            },
            "skills_mapping": {
                "use_traditional_bridge": True,
                "cultural_weighting": True
            },
            "bias_detection": {
                "sensitivity_level": "high",
                "auto_mitigation": True
            }
        }
        cast_matcher = CASTIntegratedMatcher(cast_config)
    return cast_matcher

# Pydantic models for request/response

class TranslationRequest(BaseModel):
    """Request model for content translation"""
    content: str = Field(..., description="Content to translate")
    source_language: str = Field(default="en", description="Source language code")
    target_language: str = Field(..., description="Target language code")
    cultural_region: str = Field(default="general", description="Cultural region for adaptation")
    content_type: str = Field(default="general", description="Type of content (career, skill, etc.)")
    preserve_cultural_nuances: bool = Field(default=True, description="Whether to preserve cultural context")

class TranslationResponse(BaseModel):
    """Response model for translation"""
    original_text: str
    translated_text: str
    confidence_score: float
    cultural_adaptations: List[str]
    bias_warnings: List[str]
    alternative_translations: List[str]
    language: str
    cultural_region: str

class SkillMappingRequest(BaseModel):
    """Request model for skill mapping"""
    skills: List[str] = Field(..., description="Skills to map and translate")
    source_language: str = Field(default="en", description="Source language")
    target_language: str = Field(..., description="Target language")
    cultural_context: str = Field(default="general", description="Cultural context")
    target_industry: str = Field(default="general", description="Target industry")

class SkillMappingResponse(BaseModel):
    """Response model for skill mapping"""
    mapped_skills: List[Dict[str, Any]]
    skill_gaps: List[str]
    cultural_alignment: float
    industry_relevance: float
    recommendations: List[str]
    enhanced_skills: List[Dict[str, Any]]

class BiasAnalysisRequest(BaseModel):
    """Request model for bias analysis"""
    content: str = Field(..., description="Content to analyze for bias")
    cultural_context: str = Field(default="general", description="Cultural context")
    content_type: str = Field(default="general", description="Type of content")

class BiasAnalysisResponse(BaseModel):
    """Response model for bias analysis"""
    overall_bias_score: float
    detected_biases: List[Dict[str, Any]]
    bias_categories: Dict[str, float]
    risk_level: str
    mitigation_strategies: List[str]
    warnings: List[str]

class MultilingualRecommendationsRequest(BaseModel):
    """Request model for multilingual career recommendations"""
    user_data: Dict[str, Any] = Field(..., description="User profile data")
    target_language: str = Field(default="en", description="Target language")
    cultural_region: str = Field(default="general", description="Cultural region")
    max_recommendations: int = Field(default=10, description="Maximum number of recommendations")

class MultilingualRecommendationsResponse(BaseModel):
    """Response model for multilingual recommendations"""
    recommendations: List[Dict[str, Any]]
    total_count: int
    language: str
    cultural_region: str
    processing_time: float

@router.post("/translate", response_model=TranslationResponse)
async def translate_content(
    request: TranslationRequest,
    matcher: CASTIntegratedMatcher = Depends(get_cast_matcher)
):
    """
    Translate career-related content with cultural awareness
    """
    try:
        from ..logic.cast_framework.core import TranslationContext
        
        # Create translation context
        context = TranslationContext(
            source_language=request.source_language,
            target_language=request.target_language,
            cultural_region=request.cultural_region,
            content_type=request.content_type,
            user_demographics={},
            preserve_cultural_nuances=request.preserve_cultural_nuances
        )
        
        # Perform translation
        result = await matcher.cast_framework.translate_career_content(
            request.content, context
        )
        
        return TranslationResponse(
            original_text=result.original_text,
            translated_text=result.translated_text,
            confidence_score=result.confidence_score,
            cultural_adaptations=result.cultural_adaptations,
            bias_warnings=result.bias_warnings,
            alternative_translations=result.alternative_translations,
            language=request.target_language,
            cultural_region=request.cultural_region
        )
        
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@router.post("/map-skills", response_model=SkillMappingResponse)
async def map_skills(
    request: SkillMappingRequest,
    matcher: CASTIntegratedMatcher = Depends(get_cast_matcher)
):
    """
    Map and translate skills across cultural contexts
    """
    try:
        # Analyze skill portfolio
        analysis = await matcher.cast_framework.skills_mapper.analyze_skill_portfolio(
            request.skills,
            request.cultural_context,
            request.target_industry
        )
        
        return SkillMappingResponse(**analysis)
        
    except Exception as e:
        logger.error(f"Skill mapping failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Skill mapping failed: {str(e)}")

@router.post("/analyze-bias", response_model=BiasAnalysisResponse)
async def analyze_bias(
    request: BiasAnalysisRequest,
    matcher: CASTIntegratedMatcher = Depends(get_cast_matcher)
):
    """
    Analyze content for bias and cultural sensitivity issues
    """
    try:
        # Create mock context for bias analysis
        class MockContext:
            def __init__(self):
                self.cultural_region = request.cultural_context
                self.target_language = "en"
                self.content_type = request.content_type
        
        context = MockContext()
        
        # Perform bias analysis
        analysis = await matcher.cast_framework.bias_detector.analyze_content(
            request.content, context
        )
        
        return BiasAnalysisResponse(**analysis)
        
    except Exception as e:
        logger.error(f"Bias analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bias analysis failed: {str(e)}")

@router.post("/recommendations", response_model=MultilingualRecommendationsResponse)
async def get_multilingual_recommendations(
    request: MultilingualRecommendationsRequest,
    matcher: CASTIntegratedMatcher = Depends(get_cast_matcher)
):
    """
    Get culturally-aware, multilingual career recommendations
    """
    try:
        import time
        start_time = time.time()
        
        # Get multilingual recommendations
        recommendations = await matcher.get_multilingual_career_recommendations(
            db_session=None,  # Using Supabase, not SQLAlchemy
            user_data=request.user_data,
            target_language=request.target_language,
            cultural_region=request.cultural_region
        )
        
        # Limit results
        limited_recommendations = recommendations[:request.max_recommendations]
        
        # Convert to response format
        recommendation_dicts = []
        for rec in limited_recommendations:
            rec_dict = {
                "career_name": rec.career_name,
                "translated_career_name": rec.translated_career_name,
                "description": rec.description,
                "translated_description": rec.translated_description,
                "skills_required": rec.skills_required,
                "translated_skills": rec.translated_skills,
                "cultural_adaptations": rec.cultural_adaptations,
                "confidence_score": rec.confidence_score,
                "language": rec.language,
                "cultural_region": rec.cultural_region
            }
            recommendation_dicts.append(rec_dict)
        
        processing_time = time.time() - start_time
        
        return MultilingualRecommendationsResponse(
            recommendations=recommendation_dicts,
            total_count=len(recommendations),
            language=request.target_language,
            cultural_region=request.cultural_region,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Multilingual recommendations failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Recommendations failed: {str(e)}")

@router.get("/languages")
async def get_supported_languages(
    matcher: CASTIntegratedMatcher = Depends(get_cast_matcher)
):
    """
    Get list of supported languages
    """
    try:
        languages = matcher.get_supported_languages()
        return {
            "supported_languages": languages,
            "count": len(languages)
        }
    except Exception as e:
        logger.error(f"Failed to get languages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get languages: {str(e)}")

@router.get("/cultural-regions")
async def get_cultural_regions(
    matcher: CASTIntegratedMatcher = Depends(get_cast_matcher)
):
    """
    Get list of supported cultural regions
    """
    try:
        regions = matcher.get_cultural_regions()
        return {
            "cultural_regions": regions,
            "count": len(regions)
        }
    except Exception as e:
        logger.error(f"Failed to get regions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get regions: {str(e)}")

@router.get("/framework-info")
async def get_framework_info(
    matcher: CASTIntegratedMatcher = Depends(get_cast_matcher)
):
    """
    Get information about the CAST Framework
    """
    try:
        info = matcher.get_framework_statistics()
        return info
    except Exception as e:
        logger.error(f"Failed to get framework info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get framework info: {str(e)}")

@router.post("/validate-translation")
async def validate_translation_quality(
    original_content: str,
    translated_content: str,
    source_language: str,
    target_language: str,
    matcher: CASTIntegratedMatcher = Depends(get_cast_matcher)
):
    """
    Validate the quality of a translation
    """
    try:
        validation = await matcher.validate_translation_quality(
            original_content, translated_content, source_language, target_language
        )
        return validation
    except Exception as e:
        logger.error(f"Translation validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@router.delete("/cache")
async def clear_translation_cache(
    matcher: CASTIntegratedMatcher = Depends(get_cast_matcher)
):
    """
    Clear the translation cache
    """
    try:
        matcher.clear_translation_cache()
        return {"message": "Translation cache cleared successfully"}
    except Exception as e:
        logger.error(f"Failed to clear cache: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")

# Health check endpoint
@router.get("/health")
async def health_check():
    """
    Health check for CAST Framework
    """
    return {
        "status": "healthy",
        "framework": "Context-Aware Skills Translation Framework (CAST-F)",
        "version": "1.0.0",
        "components": [
            "MultilingualNLPEngine",
            "CulturalContextPreserver", 
            "CrossCulturalSkillsMapper",
            "BiasDetectionEngine"
        ]
    }
