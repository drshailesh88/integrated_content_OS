#!/usr/bin/env python3
"""
Scientific Skills Bridge - Connect 134+ scientific skills to cardiology content workflow.

This module maps scientific skills to cardiology use cases and provides
a unified interface for accessing them from content creation pipelines.

The bridge:
1. Categorizes skills by cardiology relevance
2. Provides skill recommendations based on content type
3. Generates prompts that include relevant skill instructions
4. Tracks skill usage for workflow optimization

Usage:
    from scientific_skills_bridge import ScientificSkillsBridge

    bridge = ScientificSkillsBridge()
    skills = bridge.get_skills_for_topic("SGLT2 clinical trials")
    prompt = bridge.generate_enhanced_prompt("Analyze this trial", skills)
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SKILLS_ROOT = PROJECT_ROOT / "skills"
SCIENTIFIC_SKILLS = SKILLS_ROOT / "scientific"
CARDIOLOGY_SKILLS = SKILLS_ROOT / "cardiology"


@dataclass
class ScientificSkill:
    """Represents a scientific skill and its cardiology relevance."""
    name: str
    category: str
    description: str
    cardiology_relevance: str  # high, medium, low
    use_cases: List[str] = field(default_factory=list)
    skill_path: Optional[Path] = None


# Skills most relevant for cardiology content creation
CARDIOLOGY_RELEVANT_SKILLS = {
    # Database skills - HIGH relevance
    "pubmed-database": {
        "category": "database",
        "relevance": "high",
        "use_cases": [
            "Finding clinical trial evidence",
            "Literature review for content",
            "Validating medical claims",
            "Finding guidelines and recommendations"
        ]
    },
    "clinicaltrials-database": {
        "category": "database",
        "relevance": "high",
        "use_cases": [
            "Finding ongoing trials",
            "Tracking trial results",
            "Identifying study endpoints",
            "Researching treatment efficacy"
        ]
    },
    "drugbank-database": {
        "category": "database",
        "relevance": "high",
        "use_cases": [
            "Drug mechanism information",
            "Drug-drug interactions",
            "Pharmacokinetics data",
            "Side effect profiles"
        ]
    },
    "fda-database": {
        "category": "database",
        "relevance": "high",
        "use_cases": [
            "Drug approval information",
            "Safety warnings and recalls",
            "Label information",
            "Adverse event reports"
        ]
    },
    "clinvar-database": {
        "category": "database",
        "relevance": "medium",
        "use_cases": [
            "Genetic risk factors",
            "Variant-disease associations",
            "Inherited cardiac conditions"
        ]
    },
    "gwas-database": {
        "category": "database",
        "relevance": "medium",
        "use_cases": [
            "Genetic associations with CVD",
            "Risk factor identification",
            "Polygenic risk scores"
        ]
    },
    "openalex-database": {
        "category": "database",
        "relevance": "medium",
        "use_cases": [
            "Academic paper search",
            "Author and institution data",
            "Citation analysis"
        ]
    },

    # Analysis skills - HIGH relevance
    "statsmodels": {
        "category": "analysis",
        "relevance": "high",
        "use_cases": [
            "Statistical analysis of trial data",
            "Regression modeling",
            "Survival analysis",
            "Meta-analysis computations"
        ]
    },
    "scikit-learn": {
        "category": "analysis",
        "relevance": "high",
        "use_cases": [
            "Risk prediction models",
            "Patient clustering",
            "Feature importance analysis",
            "Outcome prediction"
        ]
    },
    "plotly": {
        "category": "visualization",
        "relevance": "high",
        "use_cases": [
            "Interactive data charts",
            "Forest plots for trials",
            "Survival curves",
            "Risk visualization"
        ]
    },
    "matplotlib": {
        "category": "visualization",
        "relevance": "high",
        "use_cases": [
            "Publication-quality figures",
            "Data visualization",
            "Custom charts"
        ]
    },

    # Medical-specific - HIGH relevance
    "pyhealth": {
        "category": "medical",
        "relevance": "high",
        "use_cases": [
            "Healthcare ML models",
            "EHR data analysis",
            "Clinical prediction",
            "Risk stratification"
        ]
    },
    "neurokit2": {
        "category": "medical",
        "relevance": "high",
        "use_cases": [
            "ECG signal analysis",
            "HRV computation",
            "Arrhythmia detection",
            "Cardiac rhythm analysis"
        ]
    },
    "pydicom": {
        "category": "medical",
        "relevance": "medium",
        "use_cases": [
            "Medical imaging analysis",
            "DICOM file handling",
            "Cardiac imaging data"
        ]
    },

    # Writing and documentation - HIGH relevance
    "literature-review": {
        "category": "writing",
        "relevance": "high",
        "use_cases": [
            "Systematic literature review",
            "Evidence synthesis",
            "Research summarization"
        ]
    },
    "peer-review": {
        "category": "writing",
        "relevance": "high",
        "use_cases": [
            "Content quality review",
            "Scientific accuracy check",
            "Methodology critique"
        ]
    },
    "citation-management": {
        "category": "writing",
        "relevance": "high",
        "use_cases": [
            "Reference management",
            "Citation formatting",
            "Bibliography generation"
        ]
    },
    "scientific-writing": {
        "category": "writing",
        "relevance": "high",
        "use_cases": [
            "Academic writing guidance",
            "Research paper structure",
            "Scientific communication"
        ]
    },

    # Data processing - MEDIUM relevance
    "polars": {
        "category": "data",
        "relevance": "medium",
        "use_cases": [
            "Fast data processing",
            "Large dataset handling",
            "Data transformation"
        ]
    },
    "dask": {
        "category": "data",
        "relevance": "medium",
        "use_cases": [
            "Parallel data processing",
            "Out-of-memory computing",
            "Distributed analysis"
        ]
    },

    # Chemical/Drug analysis - MEDIUM relevance
    "rdkit": {
        "category": "chemistry",
        "relevance": "medium",
        "use_cases": [
            "Drug structure analysis",
            "Molecular properties",
            "Chemical similarity"
        ]
    },
    "datamol": {
        "category": "chemistry",
        "relevance": "medium",
        "use_cases": [
            "Molecular data science",
            "Drug discovery data"
        ]
    }
}


class ScientificSkillsBridge:
    """Bridge between scientific skills and cardiology content workflow."""

    def __init__(self):
        self.skills: Dict[str, ScientificSkill] = {}
        self._load_skills()

    def _load_skills(self):
        """Load skill information from SKILL.md files."""
        for skill_name, config in CARDIOLOGY_RELEVANT_SKILLS.items():
            skill_path = SCIENTIFIC_SKILLS / skill_name / "SKILL.md"
            description = ""

            if skill_path.exists():
                try:
                    with open(skill_path, "r") as f:
                        content = f.read()
                        # Extract description from YAML frontmatter
                        if content.startswith("---"):
                            end = content.find("---", 3)
                            if end > 0:
                                for line in content[3:end].split("\n"):
                                    if line.startswith("description:"):
                                        description = line.split(":", 1)[1].strip().strip('"')
                                        break
                except Exception:
                    pass

            self.skills[skill_name] = ScientificSkill(
                name=skill_name,
                category=config["category"],
                description=description or f"Scientific skill for {skill_name}",
                cardiology_relevance=config["relevance"],
                use_cases=config["use_cases"],
                skill_path=skill_path if skill_path.exists() else None
            )

    def get_skills_for_topic(self, topic: str) -> List[ScientificSkill]:
        """
        Get relevant scientific skills for a topic.

        Args:
            topic: Content topic (e.g., "SGLT2 clinical trial analysis")

        Returns:
            List of relevant ScientificSkill objects
        """
        topic_lower = topic.lower()
        relevant = []

        # Keyword matching for skill relevance
        keyword_skill_map = {
            "trial": ["clinicaltrials-database", "statsmodels", "literature-review"],
            "drug": ["drugbank-database", "fda-database", "rdkit"],
            "study": ["pubmed-database", "statsmodels", "literature-review"],
            "data": ["plotly", "matplotlib", "polars", "scikit-learn"],
            "analysis": ["statsmodels", "scikit-learn", "pyhealth"],
            "ecg": ["neurokit2"],
            "heart": ["neurokit2", "pyhealth"],
            "genetic": ["clinvar-database", "gwas-database"],
            "risk": ["scikit-learn", "pyhealth", "statsmodels"],
            "image": ["pydicom", "matplotlib"],
            "chart": ["plotly", "matplotlib"],
            "graph": ["plotly", "matplotlib"],
            "review": ["literature-review", "peer-review", "pubmed-database"],
            "write": ["scientific-writing", "citation-management"],
            "citation": ["citation-management", "pubmed-database"],
            "meta": ["statsmodels", "literature-review"],
            "forest plot": ["plotly", "matplotlib"],
            "survival": ["statsmodels", "scikit-learn"],
            "predict": ["scikit-learn", "pyhealth"],
        }

        matched_skills: Set[str] = set()

        for keyword, skills in keyword_skill_map.items():
            if keyword in topic_lower:
                matched_skills.update(skills)

        # Always include high-relevance skills if few matches
        if len(matched_skills) < 3:
            for name, skill in self.skills.items():
                if skill.cardiology_relevance == "high":
                    matched_skills.add(name)

        for skill_name in matched_skills:
            if skill_name in self.skills:
                relevant.append(self.skills[skill_name])

        # Sort by relevance
        relevance_order = {"high": 0, "medium": 1, "low": 2}
        relevant.sort(key=lambda s: relevance_order.get(s.cardiology_relevance, 3))

        return relevant

    def get_skills_for_content_type(self, content_type: str) -> List[ScientificSkill]:
        """
        Get skills relevant for a specific content type.

        Args:
            content_type: Type of content (youtube, newsletter, carousel, editorial)

        Returns:
            List of relevant ScientificSkill objects
        """
        content_skill_map = {
            "youtube": ["pubmed-database", "clinicaltrials-database", "plotly", "literature-review"],
            "newsletter": ["pubmed-database", "literature-review", "citation-management", "scientific-writing"],
            "carousel": ["plotly", "matplotlib", "pubmed-database", "statsmodels"],
            "editorial": ["literature-review", "peer-review", "citation-management", "statsmodels"],
            "twitter": ["pubmed-database", "clinicaltrials-database"],
            "infographic": ["plotly", "matplotlib", "statsmodels"]
        }

        skill_names = content_skill_map.get(content_type.lower(), [])
        return [self.skills[name] for name in skill_names if name in self.skills]

    def generate_skill_prompt_section(self, skills: List[ScientificSkill]) -> str:
        """
        Generate a prompt section that includes skill instructions.

        Args:
            skills: List of ScientificSkill objects

        Returns:
            Formatted string for prompt enhancement
        """
        if not skills:
            return ""

        sections = []
        sections.append("\n## Available Scientific Skills\n")
        sections.append("You have access to these scientific skills for this task:\n")

        for skill in skills:
            sections.append(f"\n### {skill.name}")
            sections.append(f"Category: {skill.category}")
            sections.append(f"Use cases:")
            for use_case in skill.use_cases[:3]:
                sections.append(f"  - {use_case}")

            if skill.skill_path:
                sections.append(f"Full skill: {skill.skill_path}")

        sections.append("\nUse these skills when appropriate for the task.")
        return "\n".join(sections)

    def get_database_skills(self) -> List[ScientificSkill]:
        """Get all database-related skills."""
        return [s for s in self.skills.values() if s.category == "database"]

    def get_analysis_skills(self) -> List[ScientificSkill]:
        """Get all analysis-related skills."""
        return [s for s in self.skills.values() if s.category in ["analysis", "medical"]]

    def get_visualization_skills(self) -> List[ScientificSkill]:
        """Get all visualization-related skills."""
        return [s for s in self.skills.values() if s.category == "visualization"]

    def get_writing_skills(self) -> List[ScientificSkill]:
        """Get all writing-related skills."""
        return [s for s in self.skills.values() if s.category == "writing"]

    def suggest_workflow(self, task: str) -> Dict[str, List[str]]:
        """
        Suggest a workflow of skills for a complex task.

        Args:
            task: Description of the task

        Returns:
            Dict with workflow phases and recommended skills
        """
        task_lower = task.lower()

        workflow = {
            "research": [],
            "analysis": [],
            "visualization": [],
            "writing": []
        }

        # Research phase
        if any(kw in task_lower for kw in ["trial", "study", "evidence", "research"]):
            workflow["research"] = ["pubmed-database", "clinicaltrials-database", "literature-review"]
        else:
            workflow["research"] = ["pubmed-database"]

        # Analysis phase
        if any(kw in task_lower for kw in ["data", "analysis", "statistical", "predict"]):
            workflow["analysis"] = ["statsmodels", "scikit-learn", "pyhealth"]
        elif "ecg" in task_lower or "heart rate" in task_lower:
            workflow["analysis"] = ["neurokit2"]

        # Visualization phase
        if any(kw in task_lower for kw in ["chart", "graph", "visual", "plot", "infographic"]):
            workflow["visualization"] = ["plotly", "matplotlib"]

        # Writing phase
        if any(kw in task_lower for kw in ["write", "article", "newsletter", "editorial"]):
            workflow["writing"] = ["scientific-writing", "citation-management", "peer-review"]

        return workflow

    def export_skill_catalog(self, output_path: Optional[Path] = None) -> Path:
        """
        Export skill catalog for reference.

        Args:
            output_path: Custom output path

        Returns:
            Path to exported file
        """
        output_path = output_path or (PROJECT_ROOT / "output" / "scientific_skills_catalog.json")

        catalog = {
            "total_skills": len(self.skills),
            "by_category": {},
            "by_relevance": {},
            "skills": []
        }

        for skill in self.skills.values():
            # By category
            if skill.category not in catalog["by_category"]:
                catalog["by_category"][skill.category] = []
            catalog["by_category"][skill.category].append(skill.name)

            # By relevance
            if skill.cardiology_relevance not in catalog["by_relevance"]:
                catalog["by_relevance"][skill.cardiology_relevance] = []
            catalog["by_relevance"][skill.cardiology_relevance].append(skill.name)

            # Full skill info
            catalog["skills"].append({
                "name": skill.name,
                "category": skill.category,
                "relevance": skill.cardiology_relevance,
                "use_cases": skill.use_cases,
                "path": str(skill.skill_path) if skill.skill_path else None
            })

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(catalog, f, indent=2)

        return output_path


def main():
    """CLI for scientific skills bridge."""
    import argparse

    parser = argparse.ArgumentParser(description="Scientific Skills Bridge")
    parser.add_argument("--topic", type=str, help="Get skills for topic")
    parser.add_argument("--content-type", type=str, help="Get skills for content type")
    parser.add_argument("--workflow", type=str, help="Suggest workflow for task")
    parser.add_argument("--catalog", action="store_true", help="Export skill catalog")
    parser.add_argument("--list", action="store_true", help="List all mapped skills")

    args = parser.parse_args()

    bridge = ScientificSkillsBridge()

    if args.list:
        print("\n📚 SCIENTIFIC SKILLS FOR CARDIOLOGY:\n")
        for relevance in ["high", "medium", "low"]:
            skills = [s for s in bridge.skills.values() if s.cardiology_relevance == relevance]
            if skills:
                print(f"\n{relevance.upper()} RELEVANCE:")
                for skill in skills:
                    print(f"  • {skill.name} ({skill.category})")
                    print(f"    {skill.use_cases[0] if skill.use_cases else 'No use cases'}")
        return

    if args.topic:
        print(f"\n🔍 Skills for topic: {args.topic}\n")
        skills = bridge.get_skills_for_topic(args.topic)
        for skill in skills:
            print(f"  • {skill.name} [{skill.cardiology_relevance}]")
            print(f"    Use cases: {', '.join(skill.use_cases[:2])}")
        return

    if args.content_type:
        print(f"\n📝 Skills for {args.content_type} content:\n")
        skills = bridge.get_skills_for_content_type(args.content_type)
        for skill in skills:
            print(f"  • {skill.name}: {skill.use_cases[0] if skill.use_cases else ''}")
        return

    if args.workflow:
        print(f"\n🔧 Suggested workflow for: {args.workflow}\n")
        workflow = bridge.suggest_workflow(args.workflow)
        for phase, skills in workflow.items():
            if skills:
                print(f"  {phase.upper()}: {', '.join(skills)}")
        return

    if args.catalog:
        path = bridge.export_skill_catalog()
        print(f"Catalog exported to: {path}")
        return

    parser.print_help()
    print("\nExamples:")
    print("  python scientific_skills_bridge.py --list")
    print("  python scientific_skills_bridge.py --topic 'SGLT2 trial analysis'")
    print("  python scientific_skills_bridge.py --content-type newsletter")
    print("  python scientific_skills_bridge.py --workflow 'analyze clinical trial data'")


if __name__ == "__main__":
    main()
