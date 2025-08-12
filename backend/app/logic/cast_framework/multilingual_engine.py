"""
Multilingual NLP Engine for CAST Framework
==========================================

Handles translation and NLP processing for 15+ Indian languages
using state-of-the-art models and techniques.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
import asyncio
import re
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class TranslationModel(Enum):
    """Available translation models"""
    GOOGLE_TRANSLATE = "google"
    INDIC_TRANS = "indictrans"
    MBART = "mbart"
    HYBRID = "hybrid"

@dataclass
class LanguageConfig:
    """Configuration for a specific language"""
    code: str
    name: str
    native_name: str
    script: str
    family: str
    direction: str  # ltr or rtl
    complexity: float  # 0-1 scale
    cultural_weight: float  # importance of cultural context

class MultilingualNLPEngine:
    """
    Advanced multilingual NLP engine optimized for Indian languages
    
    Features:
    - Multi-model translation support
    - Script normalization and processing
    - Language detection
    - Quality assessment
    - Contextual adaptation
    """
    
    def __init__(self, supported_languages: List[str], config: Dict[str, Any]):
        """Initialize the multilingual engine"""
        self.supported_languages = supported_languages
        self.config = config
        
        # Language configurations
        self.language_configs = self._initialize_language_configs()
        
        # Model configurations
        self.preferred_model = config.get('preferred_model', TranslationModel.HYBRID.value)
        self.fallback_models = config.get('fallback_models', [
            TranslationModel.GOOGLE_TRANSLATE.value,
            TranslationModel.INDIC_TRANS.value
        ])
        
        # Quality thresholds
        self.min_quality_threshold = config.get('min_quality_threshold', 0.7)
        
        logger.info(f"Multilingual engine initialized for {len(supported_languages)} languages")
    
    def _initialize_language_configs(self) -> Dict[str, LanguageConfig]:
        """Initialize configurations for all supported languages"""
        configs = {
            "en": LanguageConfig("en", "English", "English", "Latin", "Indo-European", "ltr", 0.3, 0.5),
            "hi": LanguageConfig("hi", "Hindi", "हिन्दी", "Devanagari", "Indo-Aryan", "ltr", 0.7, 0.9),
            "ta": LanguageConfig("ta", "Tamil", "தமிழ்", "Tamil", "Dravidian", "ltr", 0.8, 0.95),
            "te": LanguageConfig("te", "Telugu", "తెలుగు", "Telugu", "Dravidian", "ltr", 0.8, 0.9),
            "bn": LanguageConfig("bn", "Bengali", "বাংলা", "Bengali", "Indo-Aryan", "ltr", 0.7, 0.85),
            "mr": LanguageConfig("mr", "Marathi", "मराठी", "Devanagari", "Indo-Aryan", "ltr", 0.7, 0.9),
            "gu": LanguageConfig("gu", "Gujarati", "ગુજરાતી", "Gujarati", "Indo-Aryan", "ltr", 0.7, 0.85),
            "kn": LanguageConfig("kn", "Kannada", "ಕನ್ನಡ", "Kannada", "Dravidian", "ltr", 0.8, 0.9),
            "ml": LanguageConfig("ml", "Malayalam", "മലയാളം", "Malayalam", "Dravidian", "ltr", 0.8, 0.95),
            "pa": LanguageConfig("pa", "Punjabi", "ਪੰਜਾਬੀ", "Gurmukhi", "Indo-Aryan", "ltr", 0.7, 0.85),
            "or": LanguageConfig("or", "Odia", "ଓଡ଼ିଆ", "Odia", "Indo-Aryan", "ltr", 0.8, 0.9),
            "as": LanguageConfig("as", "Assamese", "অসমীয়া", "Bengali", "Indo-Aryan", "ltr", 0.8, 0.9),
            "ur": LanguageConfig("ur", "Urdu", "اردو", "Arabic", "Indo-Aryan", "rtl", 0.7, 0.9),
            "sd": LanguageConfig("sd", "Sindhi", "سنڌي", "Arabic", "Indo-Aryan", "rtl", 0.8, 0.95),
            "ne": LanguageConfig("ne", "Nepali", "नेपाली", "Devanagari", "Indo-Aryan", "ltr", 0.7, 0.85),
            "gom": LanguageConfig("gom", "Konkani", "कोंकणी", "Devanagari", "Indo-Aryan", "ltr", 0.8, 0.9),
        }
        
        return {lang: configs[lang] for lang in self.supported_languages if lang in configs}
    
    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        variation_index: int = 0
    ) -> str:
        """
        Translate text from source to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            variation_index: For generating alternative translations
            
        Returns:
            Translated text
        """
        try:
            # Validate languages
            if source_lang not in self.language_configs:
                raise ValueError(f"Unsupported source language: {source_lang}")
            if target_lang not in self.language_configs:
                raise ValueError(f"Unsupported target language: {target_lang}")
            
            # Skip translation if same language
            if source_lang == target_lang:
                return text
            
            # Preprocess text
            cleaned_text = self._preprocess_text(text, source_lang)
            
            # Choose translation model based on language pair and variation
            model = self._select_model(source_lang, target_lang, variation_index)
            
            # Perform translation
            translated = await self._translate_with_model(
                cleaned_text, source_lang, target_lang, model
            )
            
            # Post-process translation
            final_translation = self._postprocess_text(translated, target_lang)
            
            # Validate quality
            quality_score = await self._assess_quality(
                cleaned_text, final_translation, source_lang, target_lang
            )
            
            if quality_score < self.min_quality_threshold:
                logger.warning(f"Low quality translation (score: {quality_score})")
                # Try fallback model
                if model != self.fallback_models[0]:
                    fallback_translation = await self._translate_with_model(
                        cleaned_text, source_lang, target_lang, self.fallback_models[0]
                    )
                    return self._postprocess_text(fallback_translation, target_lang)
            
            return final_translation
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            # Return original text as fallback
            return text
    
    def _preprocess_text(self, text: str, language: str) -> str:
        """Preprocess text before translation"""
        try:
            # Remove extra whitespace
            cleaned = re.sub(r'\s+', ' ', text.strip())
            
            # Handle special characters based on script
            lang_config = self.language_configs[language]
            
            if lang_config.script in ["Arabic"]:
                # Handle RTL languages
                cleaned = self._normalize_rtl_text(cleaned)
            elif lang_config.script in ["Devanagari", "Tamil", "Telugu", "Kannada", "Malayalam", "Bengali", "Gujarati", "Odia", "Gurmukhi"]:
                # Handle Indic scripts
                cleaned = self._normalize_indic_text(cleaned, lang_config.script)
            
            return cleaned
            
        except Exception as e:
            logger.warning(f"Text preprocessing failed: {str(e)}")
            return text
    
    def _postprocess_text(self, text: str, language: str) -> str:
        """Post-process translated text"""
        try:
            # Basic cleanup
            cleaned = re.sub(r'\s+', ' ', text.strip())
            
            # Language-specific post-processing
            lang_config = self.language_configs[language]
            
            if lang_config.script == "Arabic":
                cleaned = self._fix_rtl_formatting(cleaned)
            
            # Fix common translation artifacts
            cleaned = self._fix_translation_artifacts(cleaned, language)
            
            return cleaned
            
        except Exception as e:
            logger.warning(f"Text post-processing failed: {str(e)}")
            return text
    
    def _normalize_rtl_text(self, text: str) -> str:
        """Normalize right-to-left text"""
        # Basic RTL normalization
        # Add proper handling for Arabic/Urdu text direction
        return text
    
    def _normalize_indic_text(self, text: str, script: str) -> str:
        """Normalize Indic script text"""
        # Handle zero-width characters, ligatures, etc.
        # Normalize Unicode representation
        normalized = text
        
        # Remove zero-width characters
        normalized = re.sub(r'[\u200b-\u200f\u2060-\u206f\ufeff]', '', normalized)
        
        return normalized
    
    def _fix_rtl_formatting(self, text: str) -> str:
        """Fix RTL text formatting issues"""
        return text
    
    def _fix_translation_artifacts(self, text: str, language: str) -> str:
        """Fix common translation artifacts"""
        # Remove repeated words
        words = text.split()
        cleaned_words = []
        prev_word = ""
        
        for word in words:
            if word != prev_word:
                cleaned_words.append(word)
            prev_word = word
        
        return " ".join(cleaned_words)
    
    def _select_model(self, source_lang: str, target_lang: str, variation_index: int) -> str:
        """Select appropriate translation model"""
        # For Indian language pairs, prefer IndicTrans
        if source_lang in ["hi", "ta", "te", "bn", "mr", "gu", "kn", "ml", "pa", "or", "as", "ur"] and \
           target_lang in ["hi", "ta", "te", "bn", "mr", "gu", "kn", "ml", "pa", "or", "as", "ur", "en"]:
            models = [TranslationModel.INDIC_TRANS.value, TranslationModel.MBART.value, TranslationModel.GOOGLE_TRANSLATE.value]
        else:
            models = [TranslationModel.GOOGLE_TRANSLATE.value, TranslationModel.MBART.value, TranslationModel.INDIC_TRANS.value]
        
        # Select based on variation index
        return models[variation_index % len(models)]
    
    async def _translate_with_model(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        model: str
    ) -> str:
        """Perform translation with specific model"""
        try:
            if model == TranslationModel.GOOGLE_TRANSLATE.value:
                return await self._google_translate(text, source_lang, target_lang)
            elif model == TranslationModel.INDIC_TRANS.value:
                return await self._indic_translate(text, source_lang, target_lang)
            elif model == TranslationModel.MBART.value:
                return await self._mbart_translate(text, source_lang, target_lang)
            else:
                # Fallback to rule-based translation
                return await self._rule_based_translate(text, source_lang, target_lang)
                
        except Exception as e:
            logger.error(f"Model {model} translation failed: {str(e)}")
            return text
    
    async def _google_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Google Translate implementation (mock for now)"""
        # In production, integrate with Google Translate API
        # For now, return a mock translation
        logger.info(f"Mock Google Translate: {source_lang} -> {target_lang}")
        return f"[GT:{target_lang}] {text}"
    
    async def _indic_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """IndicTrans model implementation (mock for now)"""
        # In production, integrate with IndicTrans model
        logger.info(f"Mock IndicTrans: {source_lang} -> {target_lang}")
        return f"[IT:{target_lang}] {text}"
    
    async def _mbart_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """mBART model implementation (mock for now)"""
        # In production, integrate with mBART model
        logger.info(f"Mock mBART: {source_lang} -> {target_lang}")
        return f"[MB:{target_lang}] {text}"
    
    async def _rule_based_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Rule-based translation fallback"""
        # Basic dictionary-based translation for common terms
        
        # Career-related terms dictionary
        career_terms = {
            "en": {
                "engineer": {"hi": "इंजीनियर", "ta": "பொறியாளர்", "te": "ఇంజనీర్"},
                "doctor": {"hi": "डॉक्टर", "ta": "மருத்துவர்", "te": "వైద్యుడు"},
                "teacher": {"hi": "शिक्षक", "ta": "ஆசிரியர்", "te": "ఉపాధ్యాయుడు"},
                "software": {"hi": "सॉफ्टवेयर", "ta": "மென்பொருள்", "te": "సాఫ్ట్‌వేర్"},
                "manager": {"hi": "प्रबंधक", "ta": "மேலாளர்", "te": "మేనేజర్"},
            }
        }
        
        # Simple word replacement
        if source_lang in career_terms and target_lang in career_terms[source_lang].get(text.lower(), {}):
            return career_terms[source_lang][text.lower()][target_lang]
        
        return text
    
    async def _assess_quality(
        self,
        source_text: str,
        translated_text: str,
        source_lang: str,
        target_lang: str
    ) -> float:
        """Assess translation quality"""
        try:
            # Basic quality metrics
            quality_score = 0.8  # Base score
            
            # Length similarity (translations shouldn't be too different in length)
            length_ratio = len(translated_text) / max(len(source_text), 1)
            if 0.5 <= length_ratio <= 2.0:
                quality_score += 0.1
            else:
                quality_score -= 0.2
            
            # Check for untranslated text markers
            if translated_text.startswith('[') and ']' in translated_text:
                quality_score -= 0.3  # Mock translation detected
            
            # Character set validation
            target_config = self.language_configs[target_lang]
            if self._validate_character_set(translated_text, target_config):
                quality_score += 0.1
            else:
                quality_score -= 0.2
            
            return min(max(quality_score, 0.0), 1.0)
            
        except Exception as e:
            logger.warning(f"Quality assessment failed: {str(e)}")
            return 0.5
    
    def _validate_character_set(self, text: str, lang_config: LanguageConfig) -> bool:
        """Validate if text uses appropriate character set for language"""
        # Simplified validation - check if text contains appropriate script characters
        script_ranges = {
            "Latin": r'[a-zA-Z]',
            "Devanagari": r'[\u0900-\u097F]',
            "Tamil": r'[\u0B80-\u0BFF]',
            "Telugu": r'[\u0C00-\u0C7F]',
            "Bengali": r'[\u0980-\u09FF]',
            "Gujarati": r'[\u0A80-\u0AFF]',
            "Kannada": r'[\u0C80-\u0CFF]',
            "Malayalam": r'[\u0D00-\u0D7F]',
            "Gurmukhi": r'[\u0A00-\u0A7F]',
            "Odia": r'[\u0B00-\u0B7F]',
            "Arabic": r'[\u0600-\u06FF]'
        }
        
        if lang_config.script in script_ranges:
            pattern = script_ranges[lang_config.script]
            return bool(re.search(pattern, text))
        
        return True  # Accept by default if no pattern defined
    
    async def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect language of input text
        
        Returns:
            Tuple of (language_code, confidence)
        """
        try:
            # Simple character-based detection
            for lang_code, config in self.language_configs.items():
                if self._validate_character_set(text, config):
                    return lang_code, 0.8
            
            # Default to English if no match
            return "en", 0.5
            
        except Exception as e:
            logger.error(f"Language detection failed: {str(e)}")
            return "en", 0.0
    
    def get_language_info(self, language_code: str) -> Optional[LanguageConfig]:
        """Get information about a language"""
        return self.language_configs.get(language_code)
    
    def get_supported_language_pairs(self) -> List[Tuple[str, str]]:
        """Get all supported language pairs"""
        pairs = []
        for source in self.supported_languages:
            for target in self.supported_languages:
                if source != target:
                    pairs.append((source, target))
        return pairs
