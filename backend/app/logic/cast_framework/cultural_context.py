"""
Cultural Context Preservation Module
===================================

Preserves and adapts cultural context in career guidance translations
to maintain relevance and appropriateness across different Indian cultures.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re
import json

logger = logging.getLogger(__name__)

@dataclass
class CulturalElement:
    """Represents a cultural element in content"""
    text: str
    element_type: str  # 'concept', 'practice', 'value', 'institution'
    cultural_weight: float  # 0-1, importance of cultural adaptation
    region_specific: bool
    alternatives: List[str]  # Alternative expressions in different cultures

@dataclass
class CulturalAnalysis:
    """Result of cultural content analysis"""
    elements: List[CulturalElement]
    cultural_density: float  # How culturally specific the content is
    adaptation_priority: List[str]  # Elements that need adaptation first
    regional_markers: List[str]  # Regional/cultural markers found
    recommendations: List[str]  # Adaptation recommendations

class CulturalContextPreserver:
    """
    Analyzes and preserves cultural context in career guidance content
    
    Features:
    - Cultural element detection
    - Regional adaptation
    - Context-aware translation adjustments
    - Cultural sensitivity validation
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize cultural context preserver"""
        self.config = config
        
        # Cultural knowledge bases
        self.cultural_concepts = self._load_cultural_concepts()
        self.regional_variations = self._load_regional_variations()
        self.career_cultural_map = self._load_career_cultural_mapping()
        
        # Cultural sensitivity rules
        self.sensitivity_rules = self._load_sensitivity_rules()
        
        logger.info("Cultural Context Preserver initialized")
    
    def _load_cultural_concepts(self) -> Dict[str, Any]:
        """Load cultural concepts and their mappings"""
        return {
            # Educational concepts
            "joint_family": {
                "type": "social_structure",
                "weight": 0.9,
                "regions": ["north", "central", "east"],
                "adaptations": {
                    "south": "extended_family",
                    "west": "family_support_system"
                },
                "career_relevance": ["family_business", "traditional_roles", "location_preference"]
            },
            
            "arranged_marriage": {
                "type": "social_practice",
                "weight": 0.8,
                "regions": ["all"],
                "adaptations": {
                    "urban": "family_assisted_marriage",
                    "modern": "family_introduction"
                },
                "career_relevance": ["work_life_balance", "location_stability", "traditional_gender_roles"]
            },
            
            "guru_shishya": {
                "type": "educational_tradition",
                "weight": 0.85,
                "regions": ["all"],
                "adaptations": {
                    "modern": "mentorship",
                    "corporate": "apprenticeship"
                },
                "career_relevance": ["skill_learning", "career_guidance", "professional_development"]
            },
            
            "dharma": {
                "type": "philosophical_concept",
                "weight": 0.9,
                "regions": ["all"],
                "adaptations": {
                    "secular": "duty_and_purpose",
                    "professional": "work_ethics"
                },
                "career_relevance": ["career_purpose", "work_satisfaction", "ethical_considerations"]
            },
            
            # Regional concepts
            "jugaad": {
                "type": "innovation_approach",
                "weight": 0.7,
                "regions": ["north", "west"],
                "adaptations": {
                    "south": "innovative_problem_solving",
                    "formal": "resource_optimization"
                },
                "career_relevance": ["entrepreneurship", "problem_solving", "resourcefulness"]
            },
            
            "community_hierarchy": {
                "type": "social_structure",
                "weight": 0.8,
                "regions": ["all"],
                "adaptations": {
                    "modern": "professional_hierarchy",
                    "urban": "organizational_structure"
                },
                "career_relevance": ["workplace_dynamics", "career_progression", "respect_for_authority"]
            }
        }
    
    def _load_regional_variations(self) -> Dict[str, Any]:
        """Load regional cultural variations"""
        return {
            "north": {
                "values": ["family_honor", "traditional_roles", "hierarchy_respect"],
                "career_preferences": ["government_jobs", "family_business", "stable_employment"],
                "communication_style": "direct_respectful",
                "decision_making": "family_consensus"
            },
            
            "south": {
                "values": ["education_excellence", "merit_based", "innovation"],
                "career_preferences": ["technology", "education", "research"],
                "communication_style": "formal_courteous",
                "decision_making": "informed_individual"
            },
            
            "west": {
                "values": ["entrepreneurship", "business_acumen", "pragmatism"],
                "career_preferences": ["business", "finance", "trade"],
                "communication_style": "business_oriented",
                "decision_making": "opportunity_driven"
            },
            
            "east": {
                "values": ["intellectual_pursuit", "cultural_preservation", "social_service"],
                "career_preferences": ["arts", "literature", "social_work"],
                "communication_style": "intellectual_discourse",
                "decision_making": "philosophical_consideration"
            },
            
            "northeast": {
                "values": ["community_solidarity", "nature_harmony", "unique_identity"],
                "career_preferences": ["government_service", "agriculture", "tourism"],
                "communication_style": "community_focused",
                "decision_making": "community_welfare"
            }
        }
    
    def _load_career_cultural_mapping(self) -> Dict[str, Any]:
        """Load mapping between careers and cultural contexts"""
        return {
            "engineering": {
                "cultural_perceptions": {
                    "traditional": "prestigious_stable_career",
                    "modern": "innovation_technology_driver",
                    "family_view": "secure_respectable_profession"
                },
                "regional_preferences": {
                    "south": "high_preference",
                    "west": "medium_preference", 
                    "north": "medium_preference",
                    "east": "medium_preference"
                },
                "cultural_barriers": ["gender_stereotypes", "family_expectations"],
                "cultural_enablers": ["social_respect", "economic_security"]
            },
            
            "medicine": {
                "cultural_perceptions": {
                    "traditional": "noble_service_profession",
                    "modern": "high_status_career",
                    "family_view": "most_prestigious_option"
                },
                "regional_preferences": {
                    "all": "high_preference"
                },
                "cultural_barriers": ["extreme_competition", "long_study_duration"],
                "cultural_enablers": ["social_respect", "family_pride", "service_orientation"]
            },
            
            "teaching": {
                "cultural_perceptions": {
                    "traditional": "guru_respected_position",
                    "modern": "stable_government_job",
                    "family_view": "respectable_for_women"
                },
                "regional_preferences": {
                    "all": "medium_preference"
                },
                "cultural_barriers": ["low_pay_perception", "work_pressure"],
                "cultural_enablers": ["social_respect", "job_security", "vacation_time"]
            },
            
            "business": {
                "cultural_perceptions": {
                    "traditional": "family_business_continuation",
                    "modern": "entrepreneurial_opportunity",
                    "family_view": "risky_but_rewarding"
                },
                "regional_preferences": {
                    "west": "high_preference",
                    "north": "medium_preference",
                    "south": "medium_preference",
                    "east": "low_preference"
                },
                "cultural_barriers": ["risk_aversion", "family_pressure_for_stability"],
                "cultural_enablers": ["independence", "wealth_potential", "family_business_tradition"]
            },
            
            "arts": {
                "cultural_perceptions": {
                    "traditional": "cultural_preservation_role",
                    "modern": "creative_expression_field",
                    "family_view": "unstable_career_choice"
                },
                "regional_preferences": {
                    "east": "high_preference",
                    "south": "medium_preference",
                    "all": "low_traditional_acceptance"
                },
                "cultural_barriers": ["financial_instability", "family_disapproval", "social_perception"],
                "cultural_enablers": ["cultural_value", "personal_fulfillment", "unique_talent"]
            }
        }
    
    def _load_sensitivity_rules(self) -> Dict[str, Any]:
        """Load cultural sensitivity rules"""
        return {
            "gender_sensitivity": {
                "avoid_terms": ["only_for_men", "only_for_women", "not_suitable_for_girls"],
                "replace_with": ["suitable_for_all", "open_to_everyone", "inclusive_opportunity"],
                "context_awareness": "gender_neutral_language"
            },
            
            "caste_sensitivity": {
                "avoid_terms": ["caste_based_preference", "traditional_occupation", "hereditary_profession"],
                "replace_with": ["merit_based_selection", "skill_based_opportunity", "open_profession"],
                "context_awareness": "merit_based_language"
            },
            
            "religious_sensitivity": {
                "avoid_terms": ["religious_requirement", "community_specific"],
                "replace_with": ["open_to_all", "inclusive_opportunity"],
                "context_awareness": "secular_language"
            },
            
            "economic_sensitivity": {
                "avoid_terms": ["only_for_rich", "expensive_career", "poor_family_limitation"],
                "replace_with": ["scholarship_available", "financial_support_options", "accessible_with_planning"],
                "context_awareness": "economic_inclusion"
            }
        }
    
    async def analyze_content(
        self,
        content: str,
        language: str,
        cultural_region: str
    ) -> Dict[str, Any]:
        """
        Analyze content for cultural elements
        
        Args:
            content: Text content to analyze
            language: Source language
            cultural_region: Cultural region context
            
        Returns:
            Cultural analysis results
        """
        try:
            # Detect cultural elements
            cultural_elements = self._detect_cultural_elements(content, language)
            
            # Calculate cultural density
            cultural_density = self._calculate_cultural_density(cultural_elements, content)
            
            # Identify adaptation priorities
            adaptation_priority = self._prioritize_adaptations(cultural_elements, cultural_region)
            
            # Find regional markers
            regional_markers = self._find_regional_markers(content, language)
            
            # Generate recommendations
            recommendations = self._generate_adaptation_recommendations(
                cultural_elements, cultural_region
            )
            
            return {
                "elements": [elem.__dict__ for elem in cultural_elements],
                "cultural_density": cultural_density,
                "adaptation_priority": adaptation_priority,
                "regional_markers": regional_markers,
                "recommendations": recommendations,
                "adaptations": [f"Adapt {elem.text} for {cultural_region}" for elem in cultural_elements if elem.region_specific]
            }
            
        except Exception as e:
            logger.error(f"Cultural analysis failed: {str(e)}")
            return {
                "elements": [],
                "cultural_density": 0.0,
                "adaptation_priority": [],
                "regional_markers": [],
                "recommendations": [],
                "adaptations": []
            }
    
    def _detect_cultural_elements(self, content: str, language: str) -> List[CulturalElement]:
        """Detect cultural elements in content"""
        elements = []
        content_lower = content.lower()
        
        # Check for known cultural concepts
        for concept, details in self.cultural_concepts.items():
            # Simple keyword matching (in production, use NLP)
            if concept.replace("_", " ") in content_lower:
                element = CulturalElement(
                    text=concept.replace("_", " "),
                    element_type=details["type"],
                    cultural_weight=details["weight"],
                    region_specific=len(details["regions"]) < 5,  # Not all regions
                    alternatives=list(details.get("adaptations", {}).values())
                )
                elements.append(element)
        
        # Check for career-related cultural markers
        for career, details in self.career_cultural_map.items():
            if career in content_lower:
                element = CulturalElement(
                    text=career,
                    element_type="career_concept",
                    cultural_weight=0.7,
                    region_specific=len(details["regional_preferences"]) > 1,
                    alternatives=[]
                )
                elements.append(element)
        
        return elements
    
    def _calculate_cultural_density(self, elements: List[CulturalElement], content: str) -> float:
        """Calculate how culturally dense the content is"""
        if not elements:
            return 0.0
        
        # Weight by cultural importance and frequency
        total_weight = sum(elem.cultural_weight for elem in elements)
        content_length = len(content.split())
        
        # Normalize by content length
        density = min(total_weight / max(content_length / 10, 1), 1.0)
        return density
    
    def _prioritize_adaptations(
        self,
        elements: List[CulturalElement],
        cultural_region: str
    ) -> List[str]:
        """Prioritize which elements need adaptation first"""
        priority_list = []
        
        # Sort by cultural weight and region specificity
        sorted_elements = sorted(
            elements,
            key=lambda x: (x.cultural_weight, x.region_specific),
            reverse=True
        )
        
        for element in sorted_elements:
            # Check if adaptation is needed for this region
            if element.region_specific:
                priority_list.append(element.text)
        
        return priority_list
    
    def _find_regional_markers(self, content: str, language: str) -> List[str]:
        """Find regional cultural markers in content"""
        markers = []
        content_lower = content.lower()
        
        # Check for regional value indicators
        for region, details in self.regional_variations.items():
            for value in details["values"]:
                if value.replace("_", " ") in content_lower:
                    markers.append(f"{region}:{value}")
        
        return markers
    
    def _generate_adaptation_recommendations(
        self,
        elements: List[CulturalElement],
        cultural_region: str
    ) -> List[str]:
        """Generate recommendations for cultural adaptation"""
        recommendations = []
        
        # Check regional variations
        if cultural_region in self.regional_variations:
            region_info = self.regional_variations[cultural_region]
            
            # Communication style adaptation
            comm_style = region_info["communication_style"]
            recommendations.append(f"Adapt communication style to: {comm_style}")
            
            # Career preference alignment
            career_prefs = region_info["career_preferences"]
            recommendations.append(f"Emphasize relevant career areas: {', '.join(career_prefs[:3])}")
            
            # Decision making approach
            decision_style = region_info["decision_making"]
            recommendations.append(f"Frame advice for {decision_style} approach")
        
        # Element-specific recommendations
        for element in elements:
            if element.alternatives:
                recommendations.append(
                    f"Consider alternative framing for '{element.text}': {element.alternatives[0]}"
                )
        
        return recommendations
    
    async def adapt_translation(
        self,
        translation: str,
        cultural_analysis: Dict[str, Any],
        context: Any  # TranslationContext from core.py
    ) -> str:
        """
        Adapt translation based on cultural analysis
        
        Args:
            translation: Base translation
            cultural_analysis: Results from analyze_content
            context: Translation context
            
        Returns:
            Culturally adapted translation
        """
        try:
            adapted_text = translation
            
            # Apply cultural adaptations
            for adaptation in cultural_analysis.get("adaptations", []):
                adapted_text = await self._apply_cultural_adaptation(
                    adapted_text, adaptation, context
                )
            
            # Apply sensitivity rules
            adapted_text = self._apply_sensitivity_rules(adapted_text, context)
            
            # Apply regional customizations
            adapted_text = self._apply_regional_customizations(
                adapted_text, context.cultural_region, context.target_language
            )
            
            return adapted_text
            
        except Exception as e:
            logger.error(f"Cultural adaptation failed: {str(e)}")
            return translation
    
    async def _apply_cultural_adaptation(
        self,
        text: str,
        adaptation: str,
        context: Any
    ) -> str:
        """Apply specific cultural adaptation"""
        # Parse adaptation instruction
        if "Adapt" in adaptation and "for" in adaptation:
            # Extract element and region
            parts = adaptation.split(" for ")
            if len(parts) == 2:
                element = parts[0].replace("Adapt ", "").strip()
                region = parts[1].strip()
                
                # Find appropriate cultural replacement
                if element in self.cultural_concepts:
                    concept = self.cultural_concepts[element]
                    if region in concept.get("adaptations", {}):
                        replacement = concept["adaptations"][region]
                        text = text.replace(element, replacement)
        
        return text
    
    def _apply_sensitivity_rules(self, text: str, context: Any) -> str:
        """Apply cultural sensitivity rules"""
        adapted_text = text
        
        # Apply each sensitivity rule
        for rule_category, rules in self.sensitivity_rules.items():
            for avoid_term in rules["avoid_terms"]:
                if avoid_term.replace("_", " ") in adapted_text.lower():
                    # Find appropriate replacement
                    replace_terms = rules["replace_with"]
                    if replace_terms:
                        replacement = replace_terms[0].replace("_", " ")
                        adapted_text = re.sub(
                            re.escape(avoid_term.replace("_", " ")),
                            replacement,
                            adapted_text,
                            flags=re.IGNORECASE
                        )
        
        return adapted_text
    
    def _apply_regional_customizations(
        self,
        text: str,
        cultural_region: str,
        target_language: str
    ) -> str:
        """Apply region-specific customizations"""
        if cultural_region not in self.regional_variations:
            return text
        
        region_info = self.regional_variations[cultural_region]
        
        # Adjust communication style
        comm_style = region_info["communication_style"]
        
        if comm_style == "formal_courteous":
            # Add polite markers appropriate for the language
            if target_language in ["ta", "te", "kn", "ml"]:  # South Indian languages
                text = self._add_formal_markers_south(text, target_language)
        elif comm_style == "direct_respectful":
            # Adjust for North Indian communication patterns
            if target_language in ["hi", "pa", "ur"]:  # North Indian languages
                text = self._add_respectful_markers_north(text, target_language)
        
        return text
    
    def _add_formal_markers_south(self, text: str, language: str) -> str:
        """Add formal courtesy markers for South Indian languages"""
        # Add appropriate honorifics and polite forms
        # This would be language-specific in production
        return text  # Simplified for now
    
    def _add_respectful_markers_north(self, text: str, language: str) -> str:
        """Add respectful markers for North Indian languages"""
        # Add appropriate respectful forms
        # This would be language-specific in production
        return text  # Simplified for now
    
    def validate_cultural_appropriateness(
        self,
        content: str,
        target_culture: str,
        content_type: str
    ) -> Dict[str, Any]:
        """
        Validate if content is culturally appropriate
        
        Returns:
            Validation results with warnings and suggestions
        """
        try:
            warnings = []
            suggestions = []
            
            # Check for cultural sensitivity violations
            for rule_category, rules in self.sensitivity_rules.items():
                for avoid_term in rules["avoid_terms"]:
                    if avoid_term.replace("_", " ") in content.lower():
                        warnings.append(f"Potentially insensitive term: {avoid_term}")
                        suggestions.append(f"Consider using: {rules['replace_with'][0]}")
            
            # Check cultural alignment
            if target_culture in self.regional_variations:
                region_info = self.regional_variations[target_culture]
                
                # Check career preference alignment
                if content_type == "career":
                    career_prefs = region_info["career_preferences"]
                    # Simple check for preference alignment
                    for career in self.career_cultural_map:
                        if career in content.lower():
                            career_info = self.career_cultural_map[career]
                            regional_pref = career_info["regional_preferences"].get(target_culture, "medium")
                            if regional_pref == "low_preference":
                                warnings.append(f"Career '{career}' has low preference in {target_culture}")
                                suggestions.append(f"Highlight alternative aspects or related opportunities")
            
            return {
                "is_appropriate": len(warnings) == 0,
                "warnings": warnings,
                "suggestions": suggestions,
                "cultural_alignment_score": max(0.0, 1.0 - len(warnings) * 0.2)
            }
            
        except Exception as e:
            logger.error(f"Cultural validation failed: {str(e)}")
            return {
                "is_appropriate": True,
                "warnings": [],
                "suggestions": [],
                "cultural_alignment_score": 0.5
            }
