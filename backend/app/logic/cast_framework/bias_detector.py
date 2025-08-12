"""
Bias Detection and Reduction Module
==================================

Detects and mitigates various forms of bias in career guidance content
to ensure fair and inclusive recommendations across cultural contexts.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import re
import json

logger = logging.getLogger(__name__)

class BiasType(Enum):
    """Types of bias that can be detected"""
    GENDER = "gender"
    CASTE = "caste"
    RELIGION = "religion"
    ECONOMIC = "economic"
    REGIONAL = "regional"
    AGE = "age"
    LANGUAGE = "language"
    CULTURAL = "cultural"
    DISABILITY = "disability"

@dataclass
class BiasIndicator:
    """Represents a detected bias indicator"""
    text_segment: str
    bias_type: BiasType
    confidence: float
    severity: str  # low, medium, high
    context: str
    suggested_replacement: str
    explanation: str

@dataclass
class BiasAnalysis:
    """Result of bias analysis"""
    overall_bias_score: float  # 0-1, higher = more biased
    detected_biases: List[BiasIndicator]
    bias_categories: Dict[str, float]  # bias_type -> score
    risk_level: str  # low, medium, high
    mitigation_strategies: List[str]
    warnings: List[str]

class BiasDetectionEngine:
    """
    Advanced bias detection and mitigation system for career content
    
    Features:
    - Multi-dimensional bias detection
    - Contextual bias analysis
    - Cultural sensitivity scoring
    - Automated mitigation suggestions
    - Intersectional bias consideration
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize bias detection engine"""
        self.config = config
        
        # Load bias detection patterns and rules
        self.bias_patterns = self._load_bias_patterns()
        self.inclusive_language = self._load_inclusive_language_guidelines()
        self.cultural_sensitivity_rules = self._load_cultural_sensitivity_rules()
        self.mitigation_strategies = self._load_mitigation_strategies()
        
        # Bias severity thresholds
        self.severity_thresholds = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.8
        }
        
        logger.info("Bias Detection Engine initialized")
    
    def _load_bias_patterns(self) -> Dict[str, Any]:
        """Load patterns for detecting different types of bias"""
        return {
            BiasType.GENDER: {
                "explicit_patterns": [
                    r"only for (men|boys|males)",
                    r"not suitable for (women|girls|females)",
                    r"(men|women) are better at",
                    r"traditionally (male|female) field",
                    r"(his|her) natural abilities"
                ],
                "implicit_patterns": [
                    r"requires physical strength",  # when not actually required
                    r"emotional nature",
                    r"natural caregiving",
                    r"aggressive leadership",
                    r"technical mindset"
                ],
                "gendered_professions": {
                    "male_coded": ["engineer", "pilot", "surgeon", "ceo", "programmer"],
                    "female_coded": ["nurse", "teacher", "secretary", "social_worker", "hr"]
                },
                "severity_indicators": {
                    "explicit_exclusion": 0.9,
                    "stereotypical_language": 0.7,
                    "gendered_assumptions": 0.5
                }
            },
            
            BiasType.CASTE: {
                "explicit_patterns": [
                    r"upper caste preference",
                    r"caste certificate required",
                    r"traditional occupation",
                    r"hereditary profession",
                    r"family background check"
                ],
                "implicit_patterns": [
                    r"family lineage",
                    r"ancestral profession",
                    r"community connections",
                    r"social standing"
                ],
                "problematic_terms": [
                    "born to be", "natural hierarchy", "traditional role",
                    "community specific", "family trade"
                ],
                "severity_indicators": {
                    "explicit_discrimination": 0.95,
                    "hereditary_assumptions": 0.8,
                    "social_hierarchy": 0.6
                }
            },
            
            BiasType.RELIGION: {
                "explicit_patterns": [
                    r"(hindu|muslim|christian|sikh) only",
                    r"religious requirement",
                    r"faith based selection",
                    r"community specific job"
                ],
                "implicit_patterns": [
                    r"cultural fit",
                    r"traditional values",
                    r"religious observance",
                    r"dietary restrictions"
                ],
                "severity_indicators": {
                    "religious_exclusion": 0.9,
                    "faith_requirements": 0.7,
                    "cultural_assumptions": 0.5
                }
            },
            
            BiasType.ECONOMIC: {
                "explicit_patterns": [
                    r"only for rich families",
                    r"expensive career path",
                    r"requires financial backing",
                    r"not for poor students"
                ],
                "implicit_patterns": [
                    r"family investment needed",
                    r"high upfront costs",
                    r"network connections required",
                    r"elite background"
                ],
                "problematic_assumptions": [
                    "assumes family wealth", "ignores financial aid",
                    "dismisses merit-based opportunities"
                ],
                "severity_indicators": {
                    "economic_exclusion": 0.8,
                    "wealth_assumptions": 0.6,
                    "access_barriers": 0.7
                }
            },
            
            BiasType.REGIONAL: {
                "explicit_patterns": [
                    r"only for (north|south|east|west) indians",
                    r"regional preference",
                    r"local candidates only",
                    r"metropolitan background required"
                ],
                "implicit_patterns": [
                    r"urban mindset",
                    r"cosmopolitan background",
                    r"language proficiency",
                    r"cultural sophistication"
                ],
                "stereotypes": {
                    "rural_negative": ["lacks exposure", "traditional mindset", "limited outlook"],
                    "urban_bias": ["more capable", "better prepared", "modern thinking"]
                },
                "severity_indicators": {
                    "regional_exclusion": 0.8,
                    "urban_bias": 0.6,
                    "cultural_stereotypes": 0.7
                }
            },
            
            BiasType.LANGUAGE: {
                "explicit_patterns": [
                    r"english mandatory",
                    r"native english speaker",
                    r"foreign language required",
                    r"accent neutral"
                ],
                "implicit_patterns": [
                    r"communication skills",  # when it means English proficiency
                    r"global exposure",
                    r"international experience",
                    r"linguistic abilities"
                ],
                "problematic_assumptions": [
                    "english equals intelligence",
                    "local languages less valuable",
                    "accent discrimination"
                ],
                "severity_indicators": {
                    "language_discrimination": 0.8,
                    "accent_bias": 0.7,
                    "multilingual_undervaluation": 0.5
                }
            }
        }
    
    def _load_inclusive_language_guidelines(self) -> Dict[str, Any]:
        """Load guidelines for inclusive language"""
        return {
            "gender_inclusive": {
                "avoid": ["he/she", "his/her", "manpower", "chairman"],
                "use": ["they", "their", "workforce", "chairperson"],
                "neutral_terms": ["person", "individual", "professional", "candidate"]
            },
            
            "ability_inclusive": {
                "avoid": ["normal", "able-bodied", "suffering from", "victim of"],
                "use": ["typical", "non-disabled", "person with", "person who has"],
                "respectful_language": ["person-first language", "avoid pity terms"]
            },
            
            "culturally_inclusive": {
                "avoid": ["exotic", "primitive", "backward", "underdeveloped"],
                "use": ["traditional", "indigenous", "developing", "emerging"],
                "respectful_terms": ["culturally rich", "diverse background", "heritage knowledge"]
            },
            
            "economically_inclusive": {
                "avoid": ["poor", "underprivileged", "disadvantaged", "lower class"],
                "use": ["low-income", "from diverse economic backgrounds", "economically diverse"],
                "opportunity_language": ["financial aid available", "scholarship opportunities", "merit-based"]
            }
        }
    
    def _load_cultural_sensitivity_rules(self) -> Dict[str, Any]:
        """Load cultural sensitivity rules specific to Indian context"""
        return {
            "family_dynamics": {
                "sensitive_topics": ["arranged marriage", "joint family", "family business"],
                "respectful_framing": [
                    "family-supported decisions",
                    "family consultation process",
                    "family business opportunities"
                ],
                "avoid_assumptions": [
                    "individual autonomy",
                    "western family models",
                    "single-person decisions"
                ]
            },
            
            "religious_practices": {
                "neutral_approach": [
                    "respect for diverse practices",
                    "accommodation of religious observances",
                    "inclusive workplace policies"
                ],
                "avoid_generalizations": [
                    "all hindus believe",
                    "muslim restrictions",
                    "christian advantages"
                ]
            },
            
            "regional_diversity": {
                "celebrate_differences": [
                    "regional expertise",
                    "local knowledge",
                    "cultural insights",
                    "linguistic advantages"
                ],
                "avoid_hierarchies": [
                    "advanced regions",
                    "backward areas",
                    "developed vs undeveloped"
                ]
            }
        }
    
    def _load_mitigation_strategies(self) -> Dict[str, Any]:
        """Load strategies for bias mitigation"""
        return {
            BiasType.GENDER: {
                "language_fixes": [
                    "use gender-neutral language",
                    "avoid gendered assumptions",
                    "highlight successful examples from all genders"
                ],
                "content_adjustments": [
                    "emphasize skills over stereotypes",
                    "include diverse role models",
                    "address work-life balance for all"
                ]
            },
            
            BiasType.ECONOMIC: {
                "inclusive_messaging": [
                    "highlight financial aid options",
                    "mention scholarships and grants",
                    "emphasize merit-based opportunities"
                ],
                "barrier_removal": [
                    "provide cost breakdown with alternatives",
                    "suggest budget-friendly pathways",
                    "highlight earning potential"
                ]
            },
            
            BiasType.REGIONAL: {
                "value_diversity": [
                    "celebrate regional strengths",
                    "highlight local opportunities",
                    "emphasize cultural knowledge as asset"
                ],
                "reduce_urban_bias": [
                    "mention rural opportunities",
                    "value traditional knowledge",
                    "include local success stories"
                ]
            },
            
            BiasType.CASTE: {
                "merit_focus": [
                    "emphasize skills and qualifications",
                    "highlight achievement-based selection",
                    "avoid hereditary language"
                ],
                "inclusive_opportunities": [
                    "mention reservation benefits where applicable",
                    "emphasize equal opportunity",
                    "focus on potential rather than background"
                ]
            }
        }
    
    async def analyze_content(
        self,
        content: str,
        context: Any  # TranslationContext from core.py
    ) -> Dict[str, Any]:
        """
        Analyze content for various types of bias
        
        Args:
            content: Content to analyze
            context: Translation/cultural context
            
        Returns:
            Comprehensive bias analysis
        """
        try:
            detected_biases = []
            bias_scores = {}
            
            # Analyze each type of bias
            for bias_type in BiasType:
                bias_indicators = await self._detect_bias_type(
                    content, bias_type, context
                )
                detected_biases.extend(bias_indicators)
                
                # Calculate bias score for this type
                type_score = self._calculate_bias_type_score(bias_indicators)
                bias_scores[bias_type.value] = type_score
            
            # Calculate overall bias score
            overall_score = sum(bias_scores.values()) / len(bias_scores) if bias_scores else 0.0
            
            # Determine risk level
            risk_level = self._determine_risk_level(overall_score)
            
            # Generate mitigation strategies
            mitigation_strategies = self._generate_mitigation_strategies(detected_biases)
            
            # Generate warnings
            warnings = self._generate_warnings(detected_biases, overall_score)
            
            return {
                "overall_bias_score": overall_score,
                "detected_biases": [bias.__dict__ for bias in detected_biases],
                "bias_categories": bias_scores,
                "risk_level": risk_level,
                "mitigation_strategies": mitigation_strategies,
                "warnings": warnings
            }
            
        except Exception as e:
            logger.error(f"Bias analysis failed: {str(e)}")
            return {
                "overall_bias_score": 0.0,
                "detected_biases": [],
                "bias_categories": {},
                "risk_level": "unknown",
                "mitigation_strategies": [],
                "warnings": [f"Bias analysis failed: {str(e)}"]
            }
    
    async def _detect_bias_type(
        self,
        content: str,
        bias_type: BiasType,
        context: Any
    ) -> List[BiasIndicator]:
        """Detect specific type of bias in content"""
        indicators = []
        
        if bias_type not in self.bias_patterns:
            return indicators
        
        patterns = self.bias_patterns[bias_type]
        content_lower = content.lower()
        
        # Check explicit patterns
        for pattern in patterns.get("explicit_patterns", []):
            matches = re.finditer(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                indicator = BiasIndicator(
                    text_segment=match.group(),
                    bias_type=bias_type,
                    confidence=0.9,
                    severity="high",
                    context=f"Explicit {bias_type.value} bias detected",
                    suggested_replacement=self._get_replacement(match.group(), bias_type),
                    explanation=f"Direct {bias_type.value} discrimination language"
                )
                indicators.append(indicator)
        
        # Check implicit patterns
        for pattern in patterns.get("implicit_patterns", []):
            matches = re.finditer(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                # Context-dependent scoring
                confidence = self._assess_implicit_bias_confidence(
                    match.group(), content, bias_type
                )
                if confidence > 0.4:  # Only flag if reasonably confident
                    indicator = BiasIndicator(
                        text_segment=match.group(),
                        bias_type=bias_type,
                        confidence=confidence,
                        severity="medium",
                        context=f"Potential implicit {bias_type.value} bias",
                        suggested_replacement=self._get_replacement(match.group(), bias_type),
                        explanation=f"Language that may perpetuate {bias_type.value} stereotypes"
                    )
                    indicators.append(indicator)
        
        # Check for problematic terms
        problematic_terms = patterns.get("problematic_terms", [])
        for term in problematic_terms:
            if term.lower() in content_lower:
                indicator = BiasIndicator(
                    text_segment=term,
                    bias_type=bias_type,
                    confidence=0.7,
                    severity="medium",
                    context=f"Problematic terminology for {bias_type.value}",
                    suggested_replacement=self._get_replacement(term, bias_type),
                    explanation=f"Term that may reinforce {bias_type.value} bias"
                )
                indicators.append(indicator)
        
        return indicators
    
    def _assess_implicit_bias_confidence(
        self,
        text_segment: str,
        full_content: str,
        bias_type: BiasType
    ) -> float:
        """Assess confidence level for implicit bias detection"""
        # Simple context analysis to reduce false positives
        
        # Look for qualifying language that might reduce bias
        qualifying_terms = ["all", "everyone", "regardless of", "inclusive", "diverse"]
        context_window = self._get_context_window(text_segment, full_content, 50)
        
        has_qualifying_language = any(term in context_window.lower() for term in qualifying_terms)
        
        base_confidence = 0.6
        
        if has_qualifying_language:
            base_confidence -= 0.3  # Reduce confidence if inclusive language present
        
        # Check for reinforcing language
        reinforcing_terms = ["always", "never", "typical", "natural", "inherent"]
        has_reinforcing_language = any(term in context_window.lower() for term in reinforcing_terms)
        
        if has_reinforcing_language:
            base_confidence += 0.2
        
        return max(0.0, min(1.0, base_confidence))
    
    def _get_context_window(self, text_segment: str, full_content: str, window_size: int) -> str:
        """Get context window around a text segment"""
        start_pos = full_content.lower().find(text_segment.lower())
        if start_pos == -1:
            return text_segment
        
        start = max(0, start_pos - window_size)
        end = min(len(full_content), start_pos + len(text_segment) + window_size)
        
        return full_content[start:end]
    
    def _get_replacement(self, problematic_text: str, bias_type: BiasType) -> str:
        """Get suggested replacement for problematic text"""
        # Load replacement mappings
        replacements = {
            BiasType.GENDER: {
                "his": "their",
                "her": "their", 
                "he": "they",
                "she": "they",
                "manpower": "workforce",
                "chairman": "chairperson"
            },
            BiasType.ECONOMIC: {
                "poor": "from diverse economic backgrounds",
                "rich": "well-resourced",
                "expensive": "with various cost options",
                "cheap": "cost-effective"
            },
            BiasType.REGIONAL: {
                "backward": "developing",
                "primitive": "traditional",
                "sophisticated": "experienced",
                "cosmopolitan": "diverse"
            }
        }
        
        if bias_type in replacements:
            bias_replacements = replacements[bias_type]
            text_lower = problematic_text.lower()
            
            for problematic, replacement in bias_replacements.items():
                if problematic in text_lower:
                    return replacement
        
        # Default inclusive replacement
        return f"inclusive alternative to '{problematic_text}'"
    
    def _calculate_bias_type_score(self, bias_indicators: List[BiasIndicator]) -> float:
        """Calculate bias score for a specific bias type"""
        if not bias_indicators:
            return 0.0
        
        # Weight by confidence and severity
        total_score = 0.0
        severity_weights = {"low": 0.3, "medium": 0.6, "high": 1.0}
        
        for indicator in bias_indicators:
            severity_weight = severity_weights.get(indicator.severity, 0.5)
            weighted_score = indicator.confidence * severity_weight
            total_score += weighted_score
        
        # Normalize by number of indicators (with diminishing returns)
        import math
        normalized_score = total_score / (1 + math.log(len(bias_indicators)))
        
        return min(1.0, normalized_score)
    
    def _determine_risk_level(self, overall_score: float) -> str:
        """Determine overall bias risk level"""
        if overall_score >= self.severity_thresholds["high"]:
            return "high"
        elif overall_score >= self.severity_thresholds["medium"]:
            return "medium"
        elif overall_score >= self.severity_thresholds["low"]:
            return "low"
        else:
            return "minimal"
    
    def _generate_mitigation_strategies(self, detected_biases: List[BiasIndicator]) -> List[str]:
        """Generate specific mitigation strategies based on detected biases"""
        strategies = set()
        
        # Group biases by type
        bias_by_type = {}
        for bias in detected_biases:
            if bias.bias_type not in bias_by_type:
                bias_by_type[bias.bias_type] = []
            bias_by_type[bias.bias_type].append(bias)
        
        # Generate strategies for each bias type
        for bias_type, indicators in bias_by_type.items():
            if bias_type in self.mitigation_strategies:
                type_strategies = self.mitigation_strategies[bias_type]
                
                # Add general strategies
                if "language_fixes" in type_strategies:
                    strategies.update(type_strategies["language_fixes"])
                
                if "content_adjustments" in type_strategies:
                    strategies.update(type_strategies["content_adjustments"])
                
                # Add specific strategies based on severity
                high_severity_count = sum(1 for ind in indicators if ind.severity == "high")
                if high_severity_count > 0:
                    strategies.add(f"Priority: Address high-severity {bias_type.value} bias immediately")
        
        return list(strategies)
    
    def _generate_warnings(self, detected_biases: List[BiasIndicator], overall_score: float) -> List[str]:
        """Generate warnings based on bias analysis"""
        warnings = []
        
        # Overall score warnings
        if overall_score >= 0.8:
            warnings.append("HIGH RISK: Content contains significant bias that may cause harm")
        elif overall_score >= 0.6:
            warnings.append("MEDIUM RISK: Content has bias issues that should be addressed")
        elif overall_score >= 0.3:
            warnings.append("LOW RISK: Minor bias concerns detected")
        
        # Specific bias warnings
        high_severity_biases = [b for b in detected_biases if b.severity == "high"]
        if high_severity_biases:
            bias_types = set(b.bias_type.value for b in high_severity_biases)
            warnings.append(f"Explicit bias detected in: {', '.join(bias_types)}")
        
        # Cultural sensitivity warnings
        cultural_biases = [b for b in detected_biases if b.bias_type in [BiasType.CASTE, BiasType.RELIGION, BiasType.REGIONAL]]
        if cultural_biases:
            warnings.append("Cultural sensitivity review recommended")
        
        return warnings
    
    async def mitigate_bias(
        self,
        content: str,
        bias_analysis: Dict[str, Any]
    ) -> str:
        """
        Apply bias mitigation to content
        
        Args:
            content: Original content
            bias_analysis: Results from analyze_content
            
        Returns:
            Content with bias mitigation applied
        """
        try:
            mitigated_content = content
            
            # Apply replacements for detected biases
            for bias_data in bias_analysis.get("detected_biases", []):
                if bias_data["confidence"] > 0.6:  # Only apply high-confidence fixes
                    original_segment = bias_data["text_segment"]
                    replacement = bias_data["suggested_replacement"]
                    
                    # Replace with case preservation
                    mitigated_content = self._replace_preserving_case(
                        mitigated_content, original_segment, replacement
                    )
            
            # Apply general inclusive language improvements
            mitigated_content = self._apply_inclusive_language(mitigated_content)
            
            # Add inclusive disclaimers if needed
            if bias_analysis.get("overall_bias_score", 0) > 0.5:
                mitigated_content = self._add_inclusive_disclaimer(mitigated_content)
            
            return mitigated_content
            
        except Exception as e:
            logger.error(f"Bias mitigation failed: {str(e)}")
            return content
    
    def _replace_preserving_case(self, text: str, original: str, replacement: str) -> str:
        """Replace text while preserving case"""
        # Simple case preservation
        if original.isupper():
            replacement = replacement.upper()
        elif original.istitle():
            replacement = replacement.title()
        elif original.islower():
            replacement = replacement.lower()
        
        return text.replace(original, replacement)
    
    def _apply_inclusive_language(self, content: str) -> str:
        """Apply general inclusive language improvements"""
        inclusive_replacements = {
            # Gender inclusive
            "he/she": "they",
            "his/her": "their",
            "manpower": "workforce",
            "mankind": "humanity",
            
            # Ability inclusive
            "normal": "typical",
            "suffers from": "has",
            "victim of": "person with",
            
            # Culturally inclusive
            "primitive": "traditional",
            "backward": "developing",
            "exotic": "unique"
        }
        
        for original, replacement in inclusive_replacements.items():
            content = re.sub(
                re.escape(original),
                replacement,
                content,
                flags=re.IGNORECASE
            )
        
        return content
    
    def _add_inclusive_disclaimer(self, content: str) -> str:
        """Add inclusive disclaimer to content"""
        disclaimer = "\n\nNote: This guidance is intended for all individuals regardless of gender, background, or personal circumstances. Equal opportunities are available to everyone."
        
        # Only add if not already present
        if "equal opportunities" not in content.lower():
            content += disclaimer
        
        return content
    
    def validate_mitigation_effectiveness(
        self,
        original_content: str,
        mitigated_content: str
    ) -> Dict[str, Any]:
        """
        Validate the effectiveness of bias mitigation
        
        Returns:
            Validation results with before/after comparison
        """
        try:
            # Analyze both versions (simplified context)
            class MockContext:
                def __init__(self):
                    self.cultural_region = "general"
                    self.target_language = "en"
            
            mock_context = MockContext()
            
            # This would normally be async, but simplified for validation
            original_analysis = {
                "overall_bias_score": self._quick_bias_score(original_content),
                "detected_biases": []
            }
            
            mitigated_analysis = {
                "overall_bias_score": self._quick_bias_score(mitigated_content),
                "detected_biases": []
            }
            
            improvement = original_analysis["overall_bias_score"] - mitigated_analysis["overall_bias_score"]
            
            return {
                "effective": improvement > 0.1,
                "improvement_score": improvement,
                "original_bias_score": original_analysis["overall_bias_score"],
                "mitigated_bias_score": mitigated_analysis["overall_bias_score"],
                "percentage_improvement": (improvement / max(original_analysis["overall_bias_score"], 0.01)) * 100
            }
            
        except Exception as e:
            logger.error(f"Mitigation validation failed: {str(e)}")
            return {
                "effective": False,
                "improvement_score": 0.0,
                "error": str(e)
            }
    
    def _quick_bias_score(self, content: str) -> float:
        """Quick bias scoring for validation (simplified)"""
        bias_indicators = 0
        content_lower = content.lower()
        
        # Check for common bias terms
        bias_terms = [
            "only for men", "only for women", "not suitable for",
            "requires physical strength", "natural abilities",
            "traditional role", "family background",
            "expensive career", "only for rich"
        ]
        
        for term in bias_terms:
            if term in content_lower:
                bias_indicators += 1
        
        # Normalize by content length
        words = len(content.split())
        normalized_score = bias_indicators / max(words / 100, 1)
        
        return min(1.0, normalized_score)
