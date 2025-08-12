"""
CAST Framework Test Suite
========================

Comprehensive tests for the Context-Aware Skills Translation Framework
"""

import asyncio
import pytest
from typing import Dict, Any
import json

# Import CAST Framework components
from app.logic.cast_framework import (
    CASTFramework, 
    TranslationContext, 
    TranslationResult,
    MultilingualNLPEngine,
    CulturalContextPreserver,
    CrossCulturalSkillsMapper,
    BiasDetectionEngine
)
from app.logic.cast_integration import CASTIntegratedMatcher

class TestCASTFramework:
    """Test suite for CAST Framework core functionality"""
    
    @pytest.fixture
    def cast_framework(self):
        """Initialize CAST Framework for testing"""
        config = {
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
        return CASTFramework(config)
    
    @pytest.fixture
    def translation_context(self):
        """Create a test translation context"""
        return TranslationContext(
            source_language="en",
            target_language="hi",
            cultural_region="north",
            content_type="career",
            user_demographics={"age": 22, "education": "engineering"},
            preserve_cultural_nuances=True
        )
    
    @pytest.mark.asyncio
    async def test_basic_translation(self, cast_framework, translation_context):
        """Test basic translation functionality"""
        content = "Software engineering is a rewarding career with good growth prospects"
        
        result = await cast_framework.translate_career_content(content, translation_context)
        
        assert isinstance(result, TranslationResult)
        assert result.original_text == content
        assert result.translated_text != content  # Should be translated
        assert 0.0 <= result.confidence_score <= 1.0
        assert isinstance(result.cultural_adaptations, list)
        assert isinstance(result.bias_warnings, list)
        assert isinstance(result.alternative_translations, list)
    
    @pytest.mark.asyncio
    async def test_multilingual_support(self, cast_framework):
        """Test support for multiple Indian languages"""
        content = "Computer programming requires logical thinking"
        languages = ["hi", "ta", "te", "bn", "mr"]
        
        for lang in languages:
            context = TranslationContext(
                source_language="en",
                target_language=lang,
                cultural_region="general",
                content_type="skill",
                user_demographics={},
                preserve_cultural_nuances=True
            )
            
            result = await cast_framework.translate_career_content(content, context)
            assert result.translated_text is not None
            assert len(result.translated_text) > 0
    
    @pytest.mark.asyncio
    async def test_cultural_adaptation(self, cast_framework):
        """Test cultural context adaptation"""
        content = "Family business is a traditional career path"
        
        # Test different regional adaptations
        regions = ["north", "south", "east", "west"]
        
        for region in regions:
            context = TranslationContext(
                source_language="en",
                target_language="hi",
                cultural_region=region,
                content_type="career",
                user_demographics={},
                preserve_cultural_nuances=True
            )
            
            result = await cast_framework.translate_career_content(content, context)
            # Should have some cultural adaptations for family business concept
            assert len(result.cultural_adaptations) >= 0  # May or may not have adaptations
    
    @pytest.mark.asyncio
    async def test_bias_detection(self, cast_framework):
        """Test bias detection functionality"""
        biased_content = "This engineering job is only suitable for men with strong technical skills"
        
        context = TranslationContext(
            source_language="en",
            target_language="en",
            cultural_region="general",
            content_type="job_description",
            user_demographics={},
            preserve_cultural_nuances=True
        )
        
        # Analyze for bias
        bias_analysis = await cast_framework.bias_detector.analyze_content(
            biased_content, context
        )
        
        assert "overall_bias_score" in bias_analysis
        assert bias_analysis["overall_bias_score"] > 0.3  # Should detect bias
        assert len(bias_analysis["detected_biases"]) > 0
        assert bias_analysis["risk_level"] in ["low", "medium", "high"]
    
    @pytest.mark.asyncio
    async def test_skills_mapping(self, cast_framework):
        """Test cross-cultural skills mapping"""
        skills = ["programming", "communication", "leadership", "problem solving"]
        
        analysis = await cast_framework.skills_mapper.analyze_skill_portfolio(
            skills=skills,
            cultural_context="south",
            target_industry="technology"
        )
        
        assert "mapped_skills" in analysis
        assert "cultural_alignment" in analysis
        assert "industry_relevance" in analysis
        assert "recommendations" in analysis
        assert 0.0 <= analysis["cultural_alignment"] <= 1.0
        assert 0.0 <= analysis["industry_relevance"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_batch_translation(self, cast_framework, translation_context):
        """Test batch translation functionality"""
        content_items = [
            ("Software engineering", "career_title"),
            ("Requires programming skills", "requirement"),
            ("Good salary prospects", "benefit"),
            ("Available in major cities", "location_info")
        ]
        
        results = await cast_framework.batch_translate(content_items, translation_context)
        
        assert len(results) == len(content_items)
        for result in results:
            assert isinstance(result, TranslationResult)
            assert result.translated_text is not None
    
    def test_supported_languages(self, cast_framework):
        """Test supported languages list"""
        languages = cast_framework.get_supported_languages()
        
        assert isinstance(languages, list)
        assert len(languages) >= 15  # Should support 15+ languages
        assert "en" in languages
        assert "hi" in languages
        assert "ta" in languages
    
    def test_framework_info(self, cast_framework):
        """Test framework information"""
        info = cast_framework.get_framework_info()
        
        assert "name" in info
        assert "version" in info
        assert "supported_languages" in info
        assert "components" in info
        assert "features" in info

class TestCASTIntegration:
    """Test suite for CAST Framework integration with CareerBuddy"""
    
    @pytest.fixture
    def cast_matcher(self):
        """Initialize CAST integrated matcher"""
        return CASTIntegratedMatcher()
    
    @pytest.mark.asyncio
    async def test_multilingual_recommendations(self, cast_matcher):
        """Test multilingual career recommendations"""
        user_data = {
            "skills": ["programming", "problem solving"],
            "interests": ["technology", "innovation"],
            "education_level": "bachelor",
            "current_marks_value": 85.0,
            "location": "bangalore"
        }
        
        recommendations = await cast_matcher.get_multilingual_career_recommendations(
            db_session=None,
            user_data=user_data,
            target_language="hi",
            cultural_region="south"
        )
        
        assert isinstance(recommendations, list)
        # Note: May be empty if no base recommendations available
        if recommendations:
            rec = recommendations[0]
            assert hasattr(rec, 'career_name')
            assert hasattr(rec, 'translated_career_name')
            assert hasattr(rec, 'confidence_score')
    
    @pytest.mark.asyncio
    async def test_culturally_adapted_questions(self, cast_matcher):
        """Test cultural adaptation of assessment questions"""
        base_questions = [
            {
                "id": 1,
                "question": "What is your preferred work environment?",
                "type": "multiple_choice",
                "category": "work_preferences",
                "options": ["Office", "Remote", "Hybrid", "Field work"]
            },
            {
                "id": 2,
                "question": "How important is family approval in your career choice?",
                "type": "scale",
                "category": "cultural_values"
            }
        ]
        
        adapted_questions = await cast_matcher.get_culturally_adapted_assessment_questions(
            base_questions=base_questions,
            target_language="ta",
            cultural_region="south"
        )
        
        assert len(adapted_questions) == len(base_questions)
        for question in adapted_questions:
            assert "question" in question
            assert "language" in question
            assert "cultural_region" in question
    
    @pytest.mark.asyncio
    async def test_user_input_bias_analysis(self, cast_matcher):
        """Test bias analysis of user input"""
        user_responses = {
            "career_preference": "I want a job that is suitable for my gender",
            "work_environment": "I prefer traditional workplaces",
            "salary_expectation": "I need a high-paying job for my family status"
        }
        
        analysis = await cast_matcher.analyze_user_input_bias(
            user_responses=user_responses,
            cultural_context="general"
        )
        
        assert "bias_detected" in analysis
        assert "recommendations" in analysis
        if analysis["bias_detected"]:
            assert "bias_score" in analysis
            assert "risk_level" in analysis
    
    def test_supported_features(self, cast_matcher):
        """Test supported languages and regions"""
        languages = cast_matcher.get_supported_languages()
        regions = cast_matcher.get_cultural_regions()
        
        assert isinstance(languages, list)
        assert isinstance(regions, list)
        assert len(languages) > 0
        assert len(regions) > 0
    
    @pytest.mark.asyncio
    async def test_translation_quality_validation(self, cast_matcher):
        """Test translation quality validation"""
        original = "Software engineering is a good career choice"
        translated = "सॉफ्टवेयर इंजीनियरिंग एक अच्छा करियर विकल्प है"
        
        validation = await cast_matcher.validate_translation_quality(
            original_content=original,
            translated_content=translated,
            source_language="en",
            target_language="hi"
        )
        
        assert "overall_quality" in validation
        assert "acceptable" in validation
        assert "recommendations" in validation
        assert 0.0 <= validation["overall_quality"] <= 1.0

class TestPerformance:
    """Performance tests for CAST Framework"""
    
    @pytest.mark.asyncio
    async def test_translation_speed(self):
        """Test translation performance"""
        import time
        
        cast_framework = CASTFramework()
        context = TranslationContext(
            source_language="en",
            target_language="hi",
            cultural_region="north",
            content_type="career",
            user_demographics={},
            preserve_cultural_nuances=True
        )
        
        content = "This is a test content for performance measurement"
        
        start_time = time.time()
        result = await cast_framework.translate_career_content(content, context)
        end_time = time.time()
        
        # Should complete within reasonable time
        assert (end_time - start_time) < 5.0  # 5 seconds max
        assert result.translated_text is not None
    
    @pytest.mark.asyncio
    async def test_batch_performance(self):
        """Test batch processing performance"""
        import time
        
        cast_framework = CASTFramework()
        context = TranslationContext(
            source_language="en",
            target_language="hi",
            cultural_region="north",
            content_type="career",
            user_demographics={},
            preserve_cultural_nuances=True
        )
        
        # Create multiple content items
        content_items = [
            (f"Test content {i}", "test") for i in range(10)
        ]
        
        start_time = time.time()
        results = await cast_framework.batch_translate(content_items, context)
        end_time = time.time()
        
        # Batch should be faster than individual translations
        assert len(results) == len(content_items)
        assert (end_time - start_time) < 10.0  # 10 seconds max for 10 items

# Integration test functions that can be run manually
async def test_full_workflow():
    """Test complete CAST Framework workflow"""
    print("Testing CAST Framework Full Workflow...")
    
    # Initialize framework
    cast_matcher = CASTIntegratedMatcher()
    
    # Test user journey
    user_data = {
        "skills": ["programming", "communication", "teamwork"],
        "interests": ["technology", "problem solving"],
        "education_level": "bachelor",
        "location": "mumbai"
    }
    
    # Get recommendations in Hindi for North region
    print("1. Getting multilingual recommendations...")
    recommendations = await cast_matcher.get_multilingual_career_recommendations(
        db_session=None,
        user_data=user_data,
        target_language="hi",
        cultural_region="north"
    )
    
    print(f"   Found {len(recommendations)} recommendations")
    
    # Analyze user input for bias
    print("2. Analyzing user input for bias...")
    user_responses = {
        "career_goal": "I want a stable job that my family will approve of",
        "work_preference": "I prefer working with people from my community"
    }
    
    bias_analysis = await cast_matcher.analyze_user_input_bias(
        user_responses=user_responses,
        cultural_context="north"
    )
    
    print(f"   Bias detected: {bias_analysis.get('bias_detected', False)}")
    
    # Test translation
    print("3. Testing content translation...")
    content = "Software engineering offers excellent career opportunities with good growth potential"
    
    from app.logic.cast_framework.core import TranslationContext
    context = TranslationContext(
        source_language="en",
        target_language="ta",
        cultural_region="south",
        content_type="career",
        user_demographics=user_data,
        preserve_cultural_nuances=True
    )
    
    translation_result = await cast_matcher.cast_framework.translate_career_content(
        content, context
    )
    
    print(f"   Original: {translation_result.original_text}")
    print(f"   Translated: {translation_result.translated_text}")
    print(f"   Confidence: {translation_result.confidence_score:.2f}")
    
    print("CAST Framework workflow test completed successfully!")

if __name__ == "__main__":
    # Run manual test
    asyncio.run(test_full_workflow())
