"""
Cross-Cultural Skills Mapping Module
====================================

Maps skills and competencies across different cultural contexts,
ensuring accurate translation and cultural relevance.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
import json
import re

logger = logging.getLogger(__name__)

@dataclass
class SkillMapping:
    """Represents a skill mapping across cultures"""
    original_skill: str
    mapped_skills: Dict[str, str]  # culture -> skill name
    competency_level: str  # basic, intermediate, advanced, expert
    cultural_context: Dict[str, Any]  # Cultural interpretation variations
    industry_relevance: Dict[str, float]  # industry -> relevance score
    transferability: float  # How transferable this skill is across cultures

@dataclass
class CompetencyProfile:
    """A complete competency profile with cultural adaptations"""
    core_competencies: List[str]
    technical_skills: List[str]
    soft_skills: List[str]
    cultural_skills: List[str]
    regional_variations: Dict[str, List[str]]

class CrossCulturalSkillsMapper:
    """
    Maps skills and competencies across different cultural contexts
    
    Features:
    - Skill taxonomy standardization
    - Cultural competency mapping  
    - Industry-specific skill translation
    - Soft skills cultural adaptation
    - Traditional vs modern skill bridging
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the skills mapper"""
        self.config = config
        
        # Load skill mappings and taxonomies
        self.skill_taxonomy = self._load_skill_taxonomy()
        self.cultural_skill_map = self._load_cultural_skill_mappings()
        self.industry_skills = self._load_industry_skill_requirements()
        self.soft_skills_cultural = self._load_soft_skills_cultural_map()
        self.traditional_modern_bridge = self._load_traditional_modern_bridge()
        
        logger.info("Cross-Cultural Skills Mapper initialized")
    
    def _load_skill_taxonomy(self) -> Dict[str, Any]:
        """Load standardized skill taxonomy"""
        return {
            "technical_skills": {
                "programming": {
                    "subcategories": ["web_development", "mobile_development", "data_science", "ai_ml"],
                    "languages": ["python", "java", "javascript", "c++", "r"],
                    "frameworks": ["react", "django", "tensorflow", "spring"],
                    "cultural_variations": {
                        "global": "software_programming",
                        "india": "computer_programming",
                        "rural": "computer_coding"
                    }
                },
                "engineering": {
                    "subcategories": ["mechanical", "electrical", "civil", "chemical", "computer"],
                    "specializations": ["design", "manufacturing", "research", "consulting"],
                    "cultural_variations": {
                        "traditional": "technical_expertise",
                        "modern": "engineering_innovation",
                        "family_business": "technical_skills_application"
                    }
                },
                "healthcare": {
                    "subcategories": ["clinical", "research", "administration", "technology"],
                    "specializations": ["diagnosis", "treatment", "prevention", "management"],
                    "cultural_variations": {
                        "traditional": "healing_knowledge",
                        "modern": "medical_expertise",
                        "rural": "community_health_skills"
                    }
                }
            },
            
            "soft_skills": {
                "communication": {
                    "aspects": ["verbal", "written", "presentation", "interpersonal"],
                    "cultural_variations": {
                        "hierarchical": "respectful_communication",
                        "collaborative": "team_communication",
                        "formal": "professional_communication",
                        "family_oriented": "relationship_building"
                    }
                },
                "leadership": {
                    "aspects": ["team_management", "decision_making", "strategic_thinking", "motivation"],
                    "cultural_variations": {
                        "traditional": "guidance_and_mentorship",
                        "modern": "innovative_leadership",
                        "collaborative": "facilitative_leadership",
                        "hierarchical": "authoritative_leadership"
                    }
                },
                "problem_solving": {
                    "aspects": ["analytical_thinking", "creativity", "innovation", "resourcefulness"],
                    "cultural_variations": {
                        "jugaad": "innovative_resourcefulness",
                        "systematic": "methodical_problem_solving",
                        "collaborative": "collective_problem_solving",
                        "traditional": "wisdom_based_solutions"
                    }
                }
            },
            
            "cultural_skills": {
                "cross_cultural_competency": {
                    "aspects": ["cultural_awareness", "adaptability", "empathy", "global_mindset"],
                    "importance_by_region": {
                        "metro": 0.9,
                        "urban": 0.7,
                        "semi_urban": 0.5,
                        "rural": 0.3
                    }
                },
                "language_skills": {
                    "aspects": ["multilingual", "translation", "interpretation", "localization"],
                    "regional_value": {
                        "north": ["hindi", "english", "punjabi"],
                        "south": ["english", "tamil", "telugu", "kannada", "malayalam"],
                        "west": ["english", "hindi", "marathi", "gujarati"],
                        "east": ["english", "bengali", "hindi", "assamese"],
                        "northeast": ["english", "hindi", "local_languages"]
                    }
                }
            }
        }
    
    def _load_cultural_skill_mappings(self) -> Dict[str, Any]:
        """Load mappings between skills across cultures"""
        return {
            # Business and entrepreneurship
            "business_acumen": {
                "modern_urban": "strategic_business_thinking",
                "traditional": "trade_and_commerce_understanding", 
                "family_business": "business_heritage_knowledge",
                "rural": "local_market_understanding",
                "regional_variations": {
                    "west": "entrepreneurial_mindset",
                    "north": "business_relationship_management",
                    "south": "analytical_business_approach",
                    "east": "ethical_business_practices"
                }
            },
            
            # Technical and innovation
            "innovation": {
                "traditional": "creative_problem_solving",
                "modern": "disruptive_innovation",
                "rural": "practical_innovation",
                "urban": "technology_innovation",
                "regional_variations": {
                    "north": "jugaad_innovation",
                    "south": "systematic_innovation", 
                    "west": "business_innovation",
                    "east": "social_innovation"
                }
            },
            
            # Social and interpersonal
            "teamwork": {
                "hierarchical": "respectful_collaboration",
                "egalitarian": "peer_collaboration",
                "family_oriented": "collective_responsibility",
                "professional": "structured_teamwork",
                "regional_variations": {
                    "north": "hierarchical_team_dynamics",
                    "south": "merit_based_collaboration",
                    "west": "goal_oriented_teamwork",
                    "east": "consensus_building"
                }
            },
            
            # Educational and learning
            "continuous_learning": {
                "traditional": "guru_shishya_learning",
                "modern": "self_directed_learning",
                "formal": "structured_education",
                "practical": "experiential_learning",
                "regional_variations": {
                    "all": "lifelong_learning_commitment"
                }
            }
        }
    
    def _load_industry_skill_requirements(self) -> Dict[str, Any]:
        """Load industry-specific skill requirements by region"""
        return {
            "information_technology": {
                "core_skills": ["programming", "system_design", "database_management"],
                "emerging_skills": ["ai_ml", "cloud_computing", "cybersecurity"],
                "soft_skills": ["problem_solving", "communication", "teamwork"],
                "regional_demand": {
                    "south": 0.9,
                    "west": 0.8,
                    "north": 0.7,
                    "east": 0.6
                },
                "cultural_adaptations": {
                    "family_concerns": "job_security_and_growth",
                    "location_preference": "remote_work_opportunities",
                    "traditional_values": "technology_for_social_good"
                }
            },
            
            "healthcare": {
                "core_skills": ["medical_knowledge", "patient_care", "diagnosis"],
                "emerging_skills": ["telemedicine", "health_informatics", "precision_medicine"],
                "soft_skills": ["empathy", "communication", "ethical_decision_making"],
                "regional_demand": {
                    "all": 0.9
                },
                "cultural_adaptations": {
                    "service_orientation": "dharmic_service_to_society",
                    "family_pride": "prestigious_profession",
                    "traditional_medicine": "integration_with_ayurveda"
                }
            },
            
            "education": {
                "core_skills": ["subject_expertise", "pedagogy", "curriculum_development"],
                "emerging_skills": ["digital_teaching", "personalized_learning", "assessment_innovation"],
                "soft_skills": ["patience", "communication", "mentoring"],
                "regional_demand": {
                    "all": 0.8
                },
                "cultural_adaptations": {
                    "guru_tradition": "respected_knowledge_transmitter",
                    "social_service": "nation_building_contribution",
                    "stability": "secure_government_employment"
                }
            },
            
            "agriculture": {
                "core_skills": ["crop_management", "soil_science", "irrigation"],
                "emerging_skills": ["precision_agriculture", "sustainable_farming", "agtech"],
                "soft_skills": ["patience", "observation", "adaptation"],
                "regional_demand": {
                    "rural": 0.9,
                    "semi_urban": 0.6,
                    "urban": 0.3
                },
                "cultural_adaptations": {
                    "traditional_knowledge": "integration_with_modern_techniques",
                    "family_occupation": "generational_farming_wisdom",
                    "land_connection": "sustainable_earth_stewardship"
                }
            }
        }
    
    def _load_soft_skills_cultural_map(self) -> Dict[str, Any]:
        """Load cultural interpretations of soft skills"""
        return {
            "respect_for_authority": {
                "positive_framing": {
                    "modern": "professional_hierarchy_understanding",
                    "traditional": "elder_and_mentor_respect",
                    "workplace": "organizational_structure_awareness"
                },
                "regional_importance": {
                    "north": 0.9,
                    "all": 0.8
                },
                "career_relevance": ["management", "traditional_industries", "government"]
            },
            
            "family_orientation": {
                "positive_framing": {
                    "modern": "work_life_balance_prioritization",
                    "professional": "stakeholder_relationship_management",
                    "traditional": "collective_responsibility_understanding"
                },
                "regional_importance": {
                    "all": 0.85
                },
                "career_relevance": ["family_business", "local_employment", "flexible_careers"]
            },
            
            "community_service": {
                "positive_framing": {
                    "modern": "social_responsibility_and_impact",
                    "professional": "corporate_social_responsibility",
                    "traditional": "dharmic_service_orientation"
                },
                "regional_importance": {
                    "east": 0.9,
                    "all": 0.7
                },
                "career_relevance": ["non_profit", "government", "social_enterprises"]
            },
            
            "adaptability": {
                "positive_framing": {
                    "modern": "agile_mindset_and_flexibility",
                    "traditional": "wisdom_in_changing_circumstances",
                    "professional": "change_management_capability"
                },
                "regional_importance": {
                    "metro": 0.9,
                    "urban": 0.8,
                    "rural": 0.6
                },
                "career_relevance": ["technology", "consulting", "startups"]
            }
        }
    
    def _load_traditional_modern_bridge(self) -> Dict[str, Any]:
        """Load mappings between traditional and modern skills"""
        return {
            "handicrafts": {
                "modern_equivalent": ["design_thinking", "manual_dexterity", "attention_to_detail"],
                "industry_applications": ["product_design", "art_therapy", "cultural_preservation"],
                "skill_enhancement": ["digital_design", "e_commerce", "branding"]
            },
            
            "farming": {
                "modern_equivalent": ["project_management", "resource_optimization", "data_analysis"],
                "industry_applications": ["supply_chain", "sustainability", "biotechnology"],
                "skill_enhancement": ["agtech", "business_management", "environmental_science"]
            },
            
            "trading": {
                "modern_equivalent": ["negotiation", "market_analysis", "relationship_building"],
                "industry_applications": ["sales", "business_development", "financial_services"],
                "skill_enhancement": ["digital_marketing", "data_analytics", "global_trade"]
            },
            
            "teaching": {
                "modern_equivalent": ["knowledge_transfer", "mentoring", "curriculum_design"],
                "industry_applications": ["training_and_development", "content_creation", "coaching"],
                "skill_enhancement": ["digital_pedagogy", "learning_technologies", "assessment_design"]
            }
        }
    
    async def map_skill(
        self,
        skill: str,
        source_culture: str,
        target_culture: str
    ) -> str:
        """
        Map a skill from one cultural context to another
        
        Args:
            skill: Skill to map
            source_culture: Source cultural context
            target_culture: Target cultural context
            
        Returns:
            Culturally appropriate skill description
        """
        try:
            skill_lower = skill.lower().replace(" ", "_")
            
            # Check if skill exists in cultural mappings
            if skill_lower in self.cultural_skill_map:
                mapping = self.cultural_skill_map[skill_lower]
                
                # Get region-specific variation if available
                if target_culture in mapping.get("regional_variations", {}):
                    return mapping["regional_variations"][target_culture]
                
                # Get cultural context variation
                if target_culture in mapping:
                    return mapping[target_culture]
            
            # Check if it's a traditional skill that needs modernization
            if skill_lower in self.traditional_modern_bridge:
                bridge = self.traditional_modern_bridge[skill_lower]
                if target_culture in ["modern", "urban", "professional"]:
                    return ", ".join(bridge["modern_equivalent"])
            
            # Check soft skills mapping
            if skill_lower in self.soft_skills_cultural:
                soft_skill = self.soft_skills_cultural[skill_lower]
                if target_culture in soft_skill["positive_framing"]:
                    return soft_skill["positive_framing"][target_culture]
            
            # Default: return original skill with minor formatting
            return skill.replace("_", " ").title()
            
        except Exception as e:
            logger.error(f"Skill mapping failed: {str(e)}")
            return skill
    
    async def analyze_skill_portfolio(
        self,
        skills: List[str],
        cultural_context: str,
        target_industry: str
    ) -> Dict[str, Any]:
        """
        Analyze a complete skill portfolio for cultural relevance
        
        Args:
            skills: List of skills to analyze
            cultural_context: Cultural context (region, traditional/modern etc.)
            target_industry: Target industry
            
        Returns:
            Analysis with recommendations
        """
        try:
            analysis = {
                "mapped_skills": [],
                "skill_gaps": [],
                "cultural_alignment": 0.0,
                "industry_relevance": 0.0,
                "recommendations": [],
                "enhanced_skills": []
            }
            
            # Map each skill
            total_relevance = 0.0
            cultural_scores = []
            
            for skill in skills:
                mapped_skill = await self.map_skill(skill, "general", cultural_context)
                analysis["mapped_skills"].append({
                    "original": skill,
                    "mapped": mapped_skill,
                    "cultural_fit": self._assess_cultural_fit(skill, cultural_context),
                    "industry_relevance": self._assess_industry_relevance(skill, target_industry)
                })
                
                # Calculate scores
                cultural_scores.append(self._assess_cultural_fit(skill, cultural_context))
                total_relevance += self._assess_industry_relevance(skill, target_industry)
            
            # Calculate overall scores
            analysis["cultural_alignment"] = sum(cultural_scores) / len(cultural_scores) if cultural_scores else 0.0
            analysis["industry_relevance"] = total_relevance / len(skills) if skills else 0.0
            
            # Identify skill gaps
            if target_industry in self.industry_skills:
                industry_req = self.industry_skills[target_industry]
                required_skills = set(industry_req["core_skills"] + industry_req["emerging_skills"])
                current_skills = set(skill.lower().replace(" ", "_") for skill in skills)
                gaps = required_skills - current_skills
                analysis["skill_gaps"] = list(gaps)
            
            # Generate recommendations
            analysis["recommendations"] = self._generate_skill_recommendations(
                skills, cultural_context, target_industry, analysis
            )
            
            # Suggest skill enhancements
            analysis["enhanced_skills"] = self._suggest_skill_enhancements(
                skills, cultural_context
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Skill portfolio analysis failed: {str(e)}")
            return {
                "mapped_skills": [],
                "skill_gaps": [],
                "cultural_alignment": 0.0,
                "industry_relevance": 0.0,
                "recommendations": [],
                "enhanced_skills": []
            }
    
    def _assess_cultural_fit(self, skill: str, cultural_context: str) -> float:
        """Assess how well a skill fits the cultural context"""
        skill_lower = skill.lower().replace(" ", "_")
        
        # Check in soft skills cultural mapping
        if skill_lower in self.soft_skills_cultural:
            importance = self.soft_skills_cultural[skill_lower]["regional_importance"]
            return importance.get(cultural_context, importance.get("all", 0.5))
        
        # Check in cultural skill mapping
        if skill_lower in self.cultural_skill_map:
            mapping = self.cultural_skill_map[skill_lower]
            if cultural_context in mapping.get("regional_variations", {}):
                return 0.9
            elif cultural_context in mapping:
                return 0.8
        
        # Default moderate fit
        return 0.6
    
    def _assess_industry_relevance(self, skill: str, industry: str) -> float:
        """Assess skill relevance to target industry"""
        if industry not in self.industry_skills:
            return 0.5
        
        industry_req = self.industry_skills[industry]
        skill_lower = skill.lower().replace(" ", "_")
        
        # Check core skills
        if skill_lower in [s.replace(" ", "_") for s in industry_req["core_skills"]]:
            return 0.9
        
        # Check emerging skills
        if skill_lower in [s.replace(" ", "_") for s in industry_req["emerging_skills"]]:
            return 0.8
        
        # Check soft skills
        if skill_lower in [s.replace(" ", "_") for s in industry_req["soft_skills"]]:
            return 0.7
        
        return 0.3
    
    def _generate_skill_recommendations(
        self,
        skills: List[str],
        cultural_context: str,
        target_industry: str,
        analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations for skill improvement"""
        recommendations = []
        
        # Cultural alignment recommendations
        if analysis["cultural_alignment"] < 0.7:
            recommendations.append(
                f"Consider framing skills in {cultural_context} context for better local relevance"
            )
        
        # Industry relevance recommendations
        if analysis["industry_relevance"] < 0.6:
            recommendations.append(
                f"Develop more {target_industry}-specific skills to improve market fit"
            )
        
        # Skill gap recommendations
        if analysis["skill_gaps"]:
            top_gaps = analysis["skill_gaps"][:3]
            recommendations.append(
                f"Priority skill development areas: {', '.join(top_gaps)}"
            )
        
        # Cultural enhancement recommendations
        if cultural_context in ["traditional", "rural"]:
            recommendations.append(
                "Consider highlighting traditional knowledge as competitive advantage"
            )
        elif cultural_context in ["modern", "urban"]:
            recommendations.append(
                "Emphasize innovation and technology skills for urban market"
            )
        
        return recommendations
    
    def _suggest_skill_enhancements(
        self,
        skills: List[str],
        cultural_context: str
    ) -> List[Dict[str, Any]]:
        """Suggest enhancements for existing skills"""
        enhancements = []
        
        for skill in skills:
            skill_lower = skill.lower().replace(" ", "_")
            
            # Check if traditional skill can be enhanced
            if skill_lower in self.traditional_modern_bridge:
                bridge = self.traditional_modern_bridge[skill_lower]
                enhancements.append({
                    "original_skill": skill,
                    "enhancement_type": "modernization",
                    "suggested_skills": bridge["skill_enhancement"],
                    "industry_applications": bridge["industry_applications"],
                    "description": f"Modernize {skill} with digital and contemporary approaches"
                })
            
            # Check for complementary skills
            if skill_lower in self.cultural_skill_map:
                mapping = self.cultural_skill_map[skill_lower]
                if cultural_context in mapping.get("regional_variations", {}):
                    enhancements.append({
                        "original_skill": skill,
                        "enhancement_type": "cultural_adaptation",
                        "suggested_adaptation": mapping["regional_variations"][cultural_context],
                        "description": f"Frame {skill} in {cultural_context} context"
                    })
        
        return enhancements
    
    def get_skill_taxonomy_info(self, skill_category: str) -> Optional[Dict[str, Any]]:
        """Get information about a skill category"""
        for category, subcategories in self.skill_taxonomy.items():
            if skill_category in subcategories:
                return subcategories[skill_category]
        return None
    
    def get_industry_skill_requirements(self, industry: str) -> Optional[Dict[str, Any]]:
        """Get skill requirements for an industry"""
        return self.industry_skills.get(industry)
    
    def validate_skill_translations(
        self,
        original_skills: List[str],
        translated_skills: List[str],
        cultural_context: str
    ) -> Dict[str, Any]:
        """
        Validate the quality of skill translations
        
        Returns:
            Validation results with quality scores and suggestions
        """
        try:
            if len(original_skills) != len(translated_skills):
                return {
                    "valid": False,
                    "error": "Skill count mismatch",
                    "quality_score": 0.0
                }
            
            validation_results = []
            total_score = 0.0
            
            for orig, trans in zip(original_skills, translated_skills):
                # Check cultural appropriateness
                cultural_fit = self._assess_cultural_fit(trans, cultural_context)
                
                # Check semantic similarity (simplified)
                semantic_similarity = self._calculate_semantic_similarity(orig, trans)
                
                skill_score = (cultural_fit + semantic_similarity) / 2
                total_score += skill_score
                
                validation_results.append({
                    "original": orig,
                    "translated": trans,
                    "cultural_fit": cultural_fit,
                    "semantic_similarity": semantic_similarity,
                    "overall_score": skill_score
                })
            
            average_score = total_score / len(original_skills) if original_skills else 0.0
            
            return {
                "valid": average_score >= 0.6,
                "quality_score": average_score,
                "individual_scores": validation_results,
                "recommendations": self._generate_translation_recommendations(validation_results)
            }
            
        except Exception as e:
            logger.error(f"Skill translation validation failed: {str(e)}")
            return {
                "valid": False,
                "error": str(e),
                "quality_score": 0.0
            }
    
    def _calculate_semantic_similarity(self, skill1: str, skill2: str) -> float:
        """Calculate semantic similarity between skills (simplified)"""
        # Simple word overlap similarity
        words1 = set(skill1.lower().split())
        words2 = set(skill2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _generate_translation_recommendations(
        self,
        validation_results: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate recommendations for improving skill translations"""
        recommendations = []
        
        low_cultural_fit = [r for r in validation_results if r["cultural_fit"] < 0.6]
        low_semantic = [r for r in validation_results if r["semantic_similarity"] < 0.5]
        
        if low_cultural_fit:
            recommendations.append(
                f"Improve cultural adaptation for: {', '.join([r['original'] for r in low_cultural_fit[:3]])}"
            )
        
        if low_semantic:
            recommendations.append(
                f"Review semantic accuracy for: {', '.join([r['original'] for r in low_semantic[:3]])}"
            )
        
        return recommendations
