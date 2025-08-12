"""
Context-Aware Skills Translation Framework (CAST-F)
===================================================

A comprehensive multilingual NLP framework for career guidance
that preserves cultural context and reduces bias in translations.

Components:
- Multilingual NLP Engine (15+ Indian languages)
- Cultural Context Preservation 
- Cross-Cultural Skills Mapping
- Bias Detection and Reduction
"""

from .core import CASTFramework, TranslationContext, TranslationResult
from .multilingual_engine import MultilingualNLPEngine
from .cultural_context import CulturalContextPreserver
from .skills_mapper import CrossCulturalSkillsMapper
from .bias_detector import BiasDetectionEngine

__version__ = "1.0.0"
__author__ = "CareerBuddy AI Team"

__all__ = [
    "CASTFramework",
    "TranslationContext",
    "TranslationResult",
    "MultilingualNLPEngine", 
    "CulturalContextPreserver",
    "CrossCulturalSkillsMapper",
    "BiasDetectionEngine"
]
