"""
Core CAST Framework Module
=========================

Main orchestrator for the Context-Aware Skills Translation Framework
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio
import json

from .multilingual_engine import MultilingualNLPEngine
from .cultural_context import CulturalContextPreserver
from .skills_mapper import CrossCulturalSkillsMapper
from .bias_detector import BiasDetectionEngine

logger = logging.getLogger(__name__)

class SupportedLanguage(Enum):
    """Supported Indian languages for translation"""
    ENGLISH = "en"
    HINDI = "hi"
    TAMIL = "ta"
    TELUGU = "te"
    BENGALI = "bn"
    MARATHI = "mr"
    GUJARATI = "gu"
    KANNADA = "kn"
    MALAYALAM = "ml"
    PUNJABI = "pa"
    ODIA = "or"
    ASSAMESE = "as"
    URDU = "ur"
    SINDHI = "sd"
    NEPALI = "ne"
    KONKANI = "gom"

@dataclass
class TranslationContext:
    """Context information for translation"""
    source_language: str
    target_language: str
    cultural_region: str
    content_type: str  # career, skill, education, etc.
    user_demographics: Dict[str, Any]
    preserve_cultural_nuances: bool = True

@dataclass
class TranslationResult:
    """Result of translation operation"""
    original_text: str
    translated_text: str
    confidence_score: float
    cultural_adaptations: List[str]
    bias_warnings: List[str]
    alternative_translations: List[str]
    metadata: Dict[str, Any]

class CASTFramework:
    """
    Main Context-Aware Skills Translation Framework
    
    Orchestrates multilingual translation with cultural context preservation
    and bias detection for career guidance content.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize CAST Framework with configuration"""
        self.config = config or {}
        
        # Initialize component engines
        self.multilingual_engine = MultilingualNLPEngine(
            supported_languages=[lang.value for lang in SupportedLanguage],
            config=self.config.get('multilingual', {})
        )
        
        self.cultural_preserver = CulturalContextPreserver(
            config=self.config.get('cultural', {})
        )
        
        self.skills_mapper = CrossCulturalSkillsMapper(
            config=self.config.get('skills_mapping', {})
        )
        
        self.bias_detector = BiasDetectionEngine(
            config=self.config.get('bias_detection', {})
        )
        
        logger.info("CAST Framework initialized successfully")
    
    async def translate_career_content(
        self,
        content: str,
        context: TranslationContext
    ) -> TranslationResult:
        """
        Translate career-related content with cultural awareness
        
        Args:
            content: Text content to translate
            context: Translation context including languages and cultural info
            
        Returns:
            TranslationResult with translated content and metadata
        """
        try:
            # Step 1: Analyze content for cultural elements
            cultural_analysis = await self.cultural_preserver.analyze_content(
                content, context.source_language, context.cultural_region
            )
            
            # Step 2: Perform base translation
            base_translation = await self.multilingual_engine.translate(
                content,
                source_lang=context.source_language,
                target_lang=context.target_language
            )
            
            # Step 3: Apply cultural adaptations
            culturally_adapted = await self.cultural_preserver.adapt_translation(
                base_translation,
                cultural_analysis,
                context
            )
            
            # Step 4: Detect and mitigate bias
            bias_analysis = await self.bias_detector.analyze_content(
                culturally_adapted,
                context
            )
            
            final_translation = await self.bias_detector.mitigate_bias(
                culturally_adapted,
                bias_analysis
            )
            
            # Step 5: Generate alternative translations
            alternatives = await self._generate_alternatives(
                content, context, num_alternatives=3
            )
            
            # Step 6: Calculate confidence score
            confidence = await self._calculate_confidence(
                content, final_translation, context
            )
            
            return TranslationResult(
                original_text=content,
                translated_text=final_translation,
                confidence_score=confidence,
                cultural_adaptations=cultural_analysis.get('adaptations', []),
                bias_warnings=bias_analysis.get('warnings', []),
                alternative_translations=alternatives,
                metadata={
                    'cultural_analysis': cultural_analysis,
                    'bias_analysis': bias_analysis,
                    'translation_path': f"{context.source_language} -> {context.target_language}",
                    'content_type': context.content_type
                }
            )
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise
    
    async def translate_skills_list(
        self,
        skills: List[str],
        context: TranslationContext
    ) -> List[TranslationResult]:
        """
        Translate and map skills across cultural contexts
        
        Args:
            skills: List of skills to translate
            context: Translation context
            
        Returns:
            List of translation results for each skill
        """
        results = []
        
        for skill in skills:
            # Use skills mapper for specialized skill translation
            mapped_skill = await self.skills_mapper.map_skill(
                skill, context.source_language, context.target_language
            )
            
            # Translate with cultural context
            translation_result = await self.translate_career_content(
                mapped_skill, context
            )
            
            results.append(translation_result)
        
        return results
    
    async def batch_translate(
        self,
        content_items: List[Tuple[str, str]],  # (content, content_type) pairs
        context: TranslationContext
    ) -> List[TranslationResult]:
        """
        Efficiently translate multiple content items in batch
        
        Args:
            content_items: List of (content, content_type) tuples
            context: Translation context
            
        Returns:
            List of translation results
        """
        tasks = []
        
        for content, content_type in content_items:
            # Create context for this specific content
            item_context = TranslationContext(
                source_language=context.source_language,
                target_language=context.target_language,
                cultural_region=context.cultural_region,
                content_type=content_type,
                user_demographics=context.user_demographics,
                preserve_cultural_nuances=context.preserve_cultural_nuances
            )
            
            task = self.translate_career_content(content, item_context)
            tasks.append(task)
        
        # Execute translations concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log errors
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Translation failed for item {i}: {str(result)}")
                # Add fallback result
                content, content_type = content_items[i]
                valid_results.append(TranslationResult(
                    original_text=content,
                    translated_text=content,  # Fallback to original
                    confidence_score=0.0,
                    cultural_adaptations=[],
                    bias_warnings=["Translation failed"],
                    alternative_translations=[],
                    metadata={'error': str(result)}
                ))
            else:
                valid_results.append(result)
        
        return valid_results
    
    async def _generate_alternatives(
        self,
        content: str,
        context: TranslationContext,
        num_alternatives: int = 3
    ) -> List[str]:
        """Generate alternative translations"""
        alternatives = []
        
        # Try different translation approaches
        for i in range(num_alternatives):
            try:
                # Vary translation parameters slightly
                alt_translation = await self.multilingual_engine.translate(
                    content,
                    source_lang=context.source_language,
                    target_lang=context.target_language,
                    variation_index=i
                )
                
                if alt_translation != content and alt_translation not in alternatives:
                    alternatives.append(alt_translation)
                    
            except Exception as e:
                logger.warning(f"Failed to generate alternative {i}: {str(e)}")
        
        return alternatives
    
    async def _calculate_confidence(
        self,
        original: str,
        translated: str,
        context: TranslationContext
    ) -> float:
        """Calculate translation confidence score"""
        try:
            # Factors affecting confidence:
            # 1. Language pair support level
            # 2. Content complexity
            # 3. Cultural adaptation success
            # 4. Bias detection results
            
            base_confidence = 0.8  # Base confidence
            
            # Adjust for language pair
            if context.source_language == "en" or context.target_language == "en":
                base_confidence += 0.1  # English pairs generally more reliable
            
            # Adjust for content length and complexity
            if len(original.split()) > 50:
                base_confidence -= 0.1  # Longer content is harder to translate
            
            # Adjust for special characters or technical terms
            if any(char.isdigit() for char in original):
                base_confidence -= 0.05
            
            return min(max(base_confidence, 0.0), 1.0)
            
        except Exception as e:
            logger.warning(f"Confidence calculation failed: {str(e)}")
            return 0.5  # Default confidence
    
    async def analyze_bias(self, content: str) -> Any:
        """
        Analyze content for bias
        """
        try:
            return await self.bias_detector.analyze_text(content)
        except Exception as e:
            logger.error(f"Bias analysis failed: {str(e)}")
            # Return a basic bias result structure
            return type('BiasResult', (), {
                'overall_bias_score': 0.0,
                'risk_level': 'low',
                'detected_biases': [],
                'bias_categories': {},
                'mitigation_strategies': [],
                'warnings': []
            })()
    
    async def map_cross_cultural_skills(
        self, 
        skills: List[str], 
        source_lang: str, 
        target_lang: str, 
        cultural_region: str
    ) -> Any:
        """
        Map skills across cultures
        """
        try:
            return await self.skills_mapper.map_skills(
                skills, source_lang, target_lang, cultural_region
            )
        except Exception as e:
            logger.error(f"Skills mapping failed: {str(e)}")
            # Return a basic skills mapping result
            return type('SkillsResult', (), {
                'original_skills': skills,
                'mapped_skills': skills,  # Fallback to original
                'traditional_equivalents': {},
                'cultural_adaptations': [],
                'confidence_scores': [0.5] * len(skills)
            })()

    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        return [lang.value for lang in SupportedLanguage]
    
    def get_framework_info(self) -> Dict[str, Any]:
        """Get information about the framework"""
        return {
            'name': 'Context-Aware Skills Translation Framework (CAST-F)',
            'version': '1.0.0',
            'supported_languages': self.get_supported_languages(),
            'components': [
                'MultilingualNLPEngine',
                'CulturalContextPreserver', 
                'CrossCulturalSkillsMapper',
                'BiasDetectionEngine'
            ],
            'features': [
                'Multilingual NLP for 15+ Indian languages',
                'Cultural context preservation',
                'Cross-cultural skills mapping',
                'Bias detection and reduction',
                'Batch translation support',
                'Alternative translation generation'
            ]
        }
