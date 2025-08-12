"""
CAST Framework Integration with CareerBuddy
==========================================

Integrates the Context-Aware Skills Translation Framework with
the existing career recommendation system.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
import asyncio
from dataclasses import dataclass

from .cast_framework import CASTFramework, TranslationContext, TranslationResult
from .enhanced_matcher import get_enhanced_career_recommendations_supabase

logger = logging.getLogger(__name__)

@dataclass
class MultilingualRecommendation:
    """Career recommendation with multilingual support"""
    career_name: str
    translated_career_name: str
    description: str
    translated_description: str
    skills_required: List[str]
    translated_skills: List[str]
    cultural_adaptations: List[str]
    confidence_score: float
    language: str
    cultural_region: str

class CASTIntegratedMatcher:
    """
    Enhanced career matcher with CAST Framework integration
    
    Provides culturally-aware, multilingual career recommendations
    with bias-reduced content.
    """
    
    def __init__(self, cast_config: Optional[Dict[str, Any]] = None):
        """Initialize the integrated matcher"""
        # Initialize CAST Framework
        self.cast_framework = CASTFramework(cast_config)
        
        # Cache for translations to improve performance
        self.translation_cache = {}
        
        logger.info("CAST-Integrated Matcher initialized")
    
    async def get_multilingual_career_recommendations(
        self,
        db_session: Any,
        user_data: Dict[str, Any],
        target_language: str = "en",
        cultural_region: str = "general"
    ) -> List[MultilingualRecommendation]:
        """
        Get career recommendations with multilingual and cultural adaptation
        
        Args:
            db_session: Database session
            user_data: User profile data
            target_language: Target language for recommendations
            cultural_region: Cultural region for context adaptation
            
        Returns:
            List of multilingual career recommendations
        """
        try:
            # Get base recommendations using existing system
            base_recommendations = await get_enhanced_career_recommendations_supabase(user_data)
            
            # Create translation context
            context = TranslationContext(
                source_language="en",  # Assuming base system is in English
                target_language=target_language,
                cultural_region=cultural_region,
                content_type="career",
                user_demographics=user_data,
                preserve_cultural_nuances=True
            )
            
            # Translate and adapt each recommendation
            multilingual_recommendations = []
            
            # Process recommendations in parallel for better performance
            translation_tasks = []
            for rec in base_recommendations[:10]:  # Limit to top 10 for performance
                task = self._translate_recommendation(rec, context)
                translation_tasks.append(task)
            
            translated_results = await asyncio.gather(*translation_tasks, return_exceptions=True)
            
            for i, result in enumerate(translated_results):
                if isinstance(result, Exception):
                    logger.error(f"Translation failed for recommendation {i}: {str(result)}")
                    # Use original recommendation as fallback
                    rec = base_recommendations[i]
                    multilingual_rec = MultilingualRecommendation(
                        career_name=rec.get('career_name', 'Unknown'),
                        translated_career_name=rec.get('career_name', 'Unknown'),
                        description=rec.get('description', ''),
                        translated_description=rec.get('description', ''),
                        skills_required=rec.get('skills_required', []),
                        translated_skills=rec.get('skills_required', []),
                        cultural_adaptations=[],
                        confidence_score=rec.get('overall_score', 0.0),
                        language=target_language,
                        cultural_region=cultural_region
                    )
                else:
                    multilingual_rec = result
                
                multilingual_recommendations.append(multilingual_rec)
            
            return multilingual_recommendations
            
        except Exception as e:
            logger.error(f"Multilingual recommendations failed: {str(e)}")
            return []
    
    async def _translate_recommendation(
        self,
        recommendation: Dict[str, Any],
        context: TranslationContext
    ) -> MultilingualRecommendation:
        """Translate a single career recommendation"""
        try:
            # Extract key information
            career_name = recommendation.get('career_name', '')
            description = recommendation.get('description', '')
            skills_required = recommendation.get('skills_required', [])
            
            # Translate career name
            career_translation = await self._cached_translate(
                career_name, context, "career_title"
            )
            
            # Translate description
            desc_context = TranslationContext(
                source_language=context.source_language,
                target_language=context.target_language,
                cultural_region=context.cultural_region,
                content_type="career_description",
                user_demographics=context.user_demographics,
                preserve_cultural_nuances=context.preserve_cultural_nuances
            )
            
            description_translation = await self._cached_translate(
                description, desc_context, "career_description"
            )
            
            # Translate skills
            translated_skills = []
            if skills_required:
                skills_translations = await self.cast_framework.translate_skills_list(
                    skills_required, context
                )
                translated_skills = [t.translated_text for t in skills_translations]
            
            # Collect cultural adaptations
            cultural_adaptations = []
            if hasattr(career_translation, 'cultural_adaptations'):
                cultural_adaptations.extend(career_translation.cultural_adaptations)
            if hasattr(description_translation, 'cultural_adaptations'):
                cultural_adaptations.extend(description_translation.cultural_adaptations)
            
            # Calculate overall confidence
            confidence_scores = [recommendation.get('overall_score', 0.5)]
            if hasattr(career_translation, 'confidence_score'):
                confidence_scores.append(career_translation.confidence_score)
            if hasattr(description_translation, 'confidence_score'):
                confidence_scores.append(description_translation.confidence_score)
            
            overall_confidence = sum(confidence_scores) / len(confidence_scores)
            
            return MultilingualRecommendation(
                career_name=career_name,
                translated_career_name=getattr(career_translation, 'translated_text', career_name),
                description=description,
                translated_description=getattr(description_translation, 'translated_text', description),
                skills_required=skills_required,
                translated_skills=translated_skills,
                cultural_adaptations=list(set(cultural_adaptations)),  # Remove duplicates
                confidence_score=overall_confidence,
                language=context.target_language,
                cultural_region=context.cultural_region
            )
            
        except Exception as e:
            logger.error(f"Recommendation translation failed: {str(e)}")
            # Return fallback recommendation
            return MultilingualRecommendation(
                career_name=recommendation.get('career_name', 'Unknown'),
                translated_career_name=recommendation.get('career_name', 'Unknown'),
                description=recommendation.get('description', ''),
                translated_description=recommendation.get('description', ''),
                skills_required=recommendation.get('skills_required', []),
                translated_skills=recommendation.get('skills_required', []),
                cultural_adaptations=[],
                confidence_score=recommendation.get('overall_score', 0.0),
                language=context.target_language,
                cultural_region=context.cultural_region
            )
    
    async def _cached_translate(
        self,
        content: str,
        context: TranslationContext,
        content_type: str
    ) -> TranslationResult:
        """Translate content with caching"""
        # Create cache key
        cache_key = f"{content}_{context.source_language}_{context.target_language}_{context.cultural_region}_{content_type}"
        
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]
        
        # Perform translation
        translation_result = await self.cast_framework.translate_career_content(
            content, context
        )
        
        # Cache result
        self.translation_cache[cache_key] = translation_result
        
        return translation_result
    
    async def get_culturally_adapted_assessment_questions(
        self,
        base_questions: List[Dict[str, Any]],
        target_language: str,
        cultural_region: str
    ) -> List[Dict[str, Any]]:
        """
        Adapt assessment questions for cultural context and language
        
        Args:
            base_questions: Original assessment questions
            target_language: Target language
            cultural_region: Cultural region for adaptation
            
        Returns:
            Culturally adapted and translated questions
        """
        try:
            adapted_questions = []
            
            context = TranslationContext(
                source_language="en",
                target_language=target_language,
                cultural_region=cultural_region,
                content_type="assessment_question",
                user_demographics={},
                preserve_cultural_nuances=True
            )
            
            for question in base_questions:
                # Translate question text
                question_text = question.get('question', '')
                translated_result = await self.cast_framework.translate_career_content(
                    question_text, context
                )
                
                # Translate options if present
                translated_options = []
                if 'options' in question:
                    for option in question['options']:
                        option_result = await self.cast_framework.translate_career_content(
                            option, context
                        )
                        translated_options.append(option_result.translated_text)
                
                # Create adapted question
                adapted_question = {
                    'id': question.get('id'),
                    'original_question': question_text,
                    'question': translated_result.translated_text,
                    'type': question.get('type'),
                    'category': question.get('category'),
                    'cultural_adaptations': translated_result.cultural_adaptations,
                    'bias_warnings': translated_result.bias_warnings,
                    'confidence_score': translated_result.confidence_score,
                    'language': target_language,
                    'cultural_region': cultural_region
                }
                
                if translated_options:
                    adapted_question['original_options'] = question.get('options', [])
                    adapted_question['options'] = translated_options
                
                adapted_questions.append(adapted_question)
            
            return adapted_questions
            
        except Exception as e:
            logger.error(f"Question adaptation failed: {str(e)}")
            return base_questions  # Return original questions as fallback
    
    async def analyze_user_input_bias(
        self,
        user_responses: Dict[str, Any],
        cultural_context: str
    ) -> Dict[str, Any]:
        """
        Analyze user input for potential bias and provide guidance
        
        Args:
            user_responses: User's assessment responses
            cultural_context: User's cultural context
            
        Returns:
            Bias analysis and recommendations
        """
        try:
            # Combine all user text responses
            text_responses = []
            for key, value in user_responses.items():
                if isinstance(value, str) and len(value.strip()) > 0:
                    text_responses.append(value)
            
            if not text_responses:
                return {"bias_detected": False, "recommendations": []}
            
            combined_text = " ".join(text_responses)
            
            # Create mock context for bias analysis
            class MockContext:
                def __init__(self):
                    self.cultural_region = cultural_context
                    self.target_language = "en"
                    self.content_type = "user_input"
            
            mock_context = MockContext()
            
            # Analyze for bias
            bias_analysis = await self.cast_framework.bias_detector.analyze_content(
                combined_text, mock_context
            )
            
            # Generate user-friendly recommendations
            recommendations = []
            if bias_analysis.get("overall_bias_score", 0) > 0.3:
                recommendations.append(
                    "Consider exploring career options beyond traditional gender or cultural expectations"
                )
            
            if any("economic" in bias.get("bias_type", "") for bias in bias_analysis.get("detected_biases", [])):
                recommendations.append(
                    "Many career paths offer financial aid and scholarship opportunities"
                )
            
            if any("regional" in bias.get("bias_type", "") for bias in bias_analysis.get("detected_biases", [])):
                recommendations.append(
                    "Consider how your local knowledge and cultural background can be career assets"
                )
            
            return {
                "bias_detected": bias_analysis.get("overall_bias_score", 0) > 0.3,
                "bias_score": bias_analysis.get("overall_bias_score", 0),
                "risk_level": bias_analysis.get("risk_level", "low"),
                "recommendations": recommendations,
                "detailed_analysis": bias_analysis
            }
            
        except Exception as e:
            logger.error(f"User input bias analysis failed: {str(e)}")
            return {"bias_detected": False, "recommendations": [], "error": str(e)}
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return self.cast_framework.get_supported_languages()
    
    def get_cultural_regions(self) -> List[str]:
        """Get list of supported cultural regions"""
        return ["north", "south", "east", "west", "northeast", "central", "metro", "urban", "rural"]
    
    async def validate_translation_quality(
        self,
        original_content: str,
        translated_content: str,
        source_language: str,
        target_language: str
    ) -> Dict[str, Any]:
        """
        Validate the quality of a translation
        
        Returns:
            Quality assessment with scores and recommendations
        """
        try:
            # Basic quality checks
            quality_assessment = {
                "length_ratio": len(translated_content) / max(len(original_content), 1),
                "character_set_valid": True,  # Simplified check
                "semantic_preservation": 0.8,  # Would use more sophisticated methods in production
                "cultural_appropriateness": 0.8,
                "overall_quality": 0.0
            }
            
            # Check length ratio (should be reasonable)
            length_ratio = quality_assessment["length_ratio"]
            if 0.3 <= length_ratio <= 3.0:
                length_score = 1.0
            else:
                length_score = max(0.0, 1.0 - abs(length_ratio - 1.0))
            
            # Calculate overall quality
            quality_assessment["overall_quality"] = (
                length_score * 0.3 +
                quality_assessment["semantic_preservation"] * 0.4 +
                quality_assessment["cultural_appropriateness"] * 0.3
            )
            
            # Generate recommendations
            recommendations = []
            if quality_assessment["overall_quality"] < 0.7:
                recommendations.append("Consider reviewing translation for accuracy")
            
            if length_ratio < 0.3:
                recommendations.append("Translation appears too short; may be missing content")
            elif length_ratio > 3.0:
                recommendations.append("Translation appears too long; may have redundant content")
            
            quality_assessment["recommendations"] = recommendations
            quality_assessment["acceptable"] = quality_assessment["overall_quality"] >= 0.6
            
            return quality_assessment
            
        except Exception as e:
            logger.error(f"Translation quality validation failed: {str(e)}")
            return {
                "overall_quality": 0.0,
                "acceptable": False,
                "error": str(e),
                "recommendations": ["Translation validation failed"]
            }
    
    def clear_translation_cache(self):
        """Clear the translation cache"""
        self.translation_cache.clear()
        logger.info("Translation cache cleared")
    
    def get_framework_statistics(self) -> Dict[str, Any]:
        """Get statistics about the framework usage"""
        return {
            "supported_languages": len(self.get_supported_languages()),
            "cached_translations": len(self.translation_cache),
            "cultural_regions": len(self.get_cultural_regions()),
            "framework_info": self.cast_framework.get_framework_info()
        }
