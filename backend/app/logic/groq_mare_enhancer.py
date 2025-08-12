"""
Groq LLM Integration for Enhanced MARE Suggestions
==================================================

Provides AI-powered insights and suggestions for the final stage of MARE recommendations
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
from groq import Groq

logger = logging.getLogger(__name__)

@dataclass
class GroqSuggestion:
    """Enhanced suggestion from Groq LLM"""
    career_title: str
    personalized_insight: str
    actionable_steps: List[str]
    skill_development_plan: List[str]
    cultural_considerations: str
    timeline_suggestion: str
    confidence_score: float

class GroqMAREEnhancer:
    """Groq LLM enhancer for MARE recommendations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq client"""
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.warning("GROQ_API_KEY not found. Groq enhancements will be disabled.")
            self.client = None
        else:
            try:
                self.client = Groq(api_key=self.api_key)
                logger.info("Groq client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                self.client = None
    
    def is_available(self) -> bool:
        """Check if Groq service is available"""
        return self.client is not None
    
    async def enhance_mare_recommendations(
        self,
        user_profile: Dict[str, Any],
        recommendations: List[Dict[str, Any]],
        limit: int = 3
    ) -> List[GroqSuggestion]:
        """
        Generate enhanced suggestions for top MARE recommendations using Groq LLM
        
        Args:
            user_profile: User's complete profile from MARE
            recommendations: Top recommendations from MARE engine
            limit: Number of recommendations to enhance
            
        Returns:
            List of enhanced suggestions with personalized insights
        """
        if not self.is_available():
            logger.warning("Groq not available, returning empty suggestions")
            return []
        
        try:
            # Take top recommendations based on limit
            top_recommendations = recommendations[:limit]
            enhanced_suggestions = []
            
            for recommendation in top_recommendations:
                suggestion = await self._generate_personalized_suggestion(
                    user_profile, recommendation
                )
                if suggestion:
                    enhanced_suggestions.append(suggestion)
            
            return enhanced_suggestions
            
        except Exception as e:
            logger.error(f"Error enhancing recommendations with Groq: {e}")
            return []
    
    async def _generate_personalized_suggestion(
        self,
        user_profile: Dict[str, Any],
        recommendation: Dict[str, Any]
    ) -> Optional[GroqSuggestion]:
        """Generate a personalized suggestion for a single recommendation"""
        
        try:
            # Create a comprehensive prompt for Groq
            prompt = self._create_enhancement_prompt(user_profile, recommendation)
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Updated to newer model
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert career counselor specializing in Indian job markets and cultural contexts. 
                        Provide personalized, actionable career guidance that considers cultural, economic, and social factors.
                        Always be encouraging, practical, and sensitive to diverse backgrounds."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500,
                top_p=0.9
            )
            
            # Parse the response
            content = response.choices[0].message.content
            return self._parse_groq_response(content, recommendation)
            
        except Exception as e:
            logger.error(f"Error generating suggestion for {recommendation.get('title', 'Unknown')}: {e}")
            return None
    
    def _create_enhancement_prompt(
        self,
        user_profile: Dict[str, Any],
        recommendation: Dict[str, Any]
    ) -> str:
        """Create a detailed prompt for Groq LLM"""
        
        prompt = f"""
Based on the following user profile and career recommendation, provide personalized career guidance:

USER PROFILE:
- Age: {user_profile.get('age', 'Not specified')}
- Education: {user_profile.get('education_level', 'Not specified')}
- Location: {user_profile.get('location', 'Not specified')}
- Cultural Context: {user_profile.get('cultural_context', 'Not specified')}
- Family Background: {user_profile.get('family_background', 'Not specified')}
- Economic Context: {user_profile.get('economic_context', 'Not specified')}
- Skills: {', '.join(user_profile.get('skills', []))}
- Interests: {', '.join(user_profile.get('interests', []))}
- Career Goals: {user_profile.get('career_goals', 'Not specified')}
- Family Expectations: {user_profile.get('family_expectations', 'Not specified')}
- Geographic Constraints: {user_profile.get('geographic_constraints', 'Not specified')}
- Financial Constraints: {user_profile.get('financial_constraints', 'Not specified')}

RECOMMENDED CAREER:
- Title: {recommendation.get('title', 'Not specified')}
- Industry: {recommendation.get('industry', 'Not specified')}
- Overall Score: {recommendation.get('overall_score', 0):.2f}
- Key Strengths: {recommendation.get('explanation', {}).get('key_strengths', 'Not specified')}

Please provide a comprehensive response in the following JSON format:
{{
    "personalized_insight": "A detailed, encouraging insight about why this career fits the user's profile, considering their cultural and personal context",
    "actionable_steps": [
        "Immediate step 1 (next 1-3 months)",
        "Short-term step 2 (3-6 months)",
        "Medium-term step 3 (6-12 months)"
    ],
    "skill_development_plan": [
        "Priority skill 1 with specific learning resources",
        "Priority skill 2 with specific learning resources",
        "Priority skill 3 with specific learning resources"
    ],
    "cultural_considerations": "How this career aligns with or challenges cultural expectations, and how to navigate family/social dynamics",
    "timeline_suggestion": "Realistic timeline for transitioning into this career considering the user's current situation",
    "confidence_score": 0.85
}}

Focus on:
1. Cultural sensitivity and family dynamics
2. Practical, actionable advice
3. Consideration of economic and geographic constraints
4. Specific skill development recommendations
5. Encouragement and motivation
"""
        
        return prompt
    
    def _parse_groq_response(
        self,
        content: str,
        recommendation: Dict[str, Any]
    ) -> Optional[GroqSuggestion]:
        """Parse Groq response into GroqSuggestion object"""
        
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                parsed_data = json.loads(json_str)
            else:
                # Fallback: try to parse the entire content as JSON
                parsed_data = json.loads(content)
            
            return GroqSuggestion(
                career_title=recommendation.get('title', 'Unknown Career'),
                personalized_insight=parsed_data.get('personalized_insight', ''),
                actionable_steps=parsed_data.get('actionable_steps', []),
                skill_development_plan=parsed_data.get('skill_development_plan', []),
                cultural_considerations=parsed_data.get('cultural_considerations', ''),
                timeline_suggestion=parsed_data.get('timeline_suggestion', ''),
                confidence_score=float(parsed_data.get('confidence_score', 0.7))
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Groq response: {e}")
            # Fallback: create a basic suggestion
            return GroqSuggestion(
                career_title=recommendation.get('title', 'Unknown Career'),
                personalized_insight=content[:300] + "..." if len(content) > 300 else content,
                actionable_steps=["Review the detailed guidance provided", "Consult with career counselors"],
                skill_development_plan=["Focus on core skills", "Continuous learning"],
                cultural_considerations="Consider family and cultural expectations",
                timeline_suggestion="Plan for 6-12 months transition period",
                confidence_score=0.6
            )
        except Exception as e:
            logger.error(f"Error parsing Groq response: {e}")
            return None
    
    async def generate_career_pathway_summary(
        self,
        user_profile: Dict[str, Any],
        enhanced_suggestions: List[GroqSuggestion]
    ) -> Optional[str]:
        """Generate an overall career pathway summary"""
        
        if not self.is_available() or not enhanced_suggestions:
            return None
        
        try:
            career_titles = [suggestion.career_title for suggestion in enhanced_suggestions]
            
            prompt = f"""
Based on the user profile and top career recommendations, provide a comprehensive career pathway summary:

USER PROFILE:
- Age: {user_profile.get('age')}
- Education: {user_profile.get('education_level')}
- Location: {user_profile.get('location')}
- Cultural Context: {user_profile.get('cultural_context')}
- Career Goals: {user_profile.get('career_goals')}

TOP CAREER RECOMMENDATIONS:
{', '.join(career_titles)}

Provide a 2-3 paragraph summary that:
1. Highlights common themes across the recommendations
2. Provides strategic advice for career development
3. Addresses potential challenges and how to overcome them
4. Considers cultural and family factors
5. Offers encouragement and motivation

Keep it personalized, actionable, and culturally sensitive.
"""
            
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a wise and experienced career mentor who understands Indian culture and values."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating career pathway summary: {e}")
            return None

# Global instance
groq_enhancer = GroqMAREEnhancer()

# Export for use in other modules
__all__ = ['GroqMAREEnhancer', 'GroqSuggestion', 'groq_enhancer']
