"""
AI Content Generator
Generates B2C and B2B content using OpenRouter API.
"""

from typing import Dict, Optional
import sys
sys.path.insert(0, '..')
from config import (
    B2C_SYSTEM_PROMPT, B2C_USER_PROMPT,
    B2B_SYSTEM_PROMPT, B2B_USER_PROMPT
)
from ai.triage import call_openrouter
from ai.astra_client import query_guidelines


def generate_b2c_content(article: Dict) -> str:
    """
    Generate B2C (patient-facing) content for an article.
    Peter Attia + Eric Topol style, 400-600 words.
    
    Args:
        article: Article dictionary with title, abstract, journal, angle
        
    Returns:
        Generated content string
    """
    # Retrieve RAG context (guidelines/textbooks)
    guidelines = query_guidelines(article.get("title", ""), limit=2)
    guideline_context = "\n".join([f"- {g}" for g in guidelines]) if guidelines else "No specific guideline context available."
    
    user_prompt = B2C_USER_PROMPT.format(
        title=article.get("title", ""),
        journal=article.get("journal", ""),
        abstract=article.get("abstract", "")[:2500],
        angle=article.get("angle", "Key findings and implications"),
        guidelines=guideline_context
    )
    
    content = call_openrouter(B2C_SYSTEM_PROMPT, user_prompt, max_tokens=1000)
    
    if content:
        return content.strip()
    return ""


def generate_b2b_content(article: Dict) -> str:
    """
    Generate B2B (doctor-facing) content for an article.
    JACC editorial style, 300-500 words.
    
    Args:
        article: Article dictionary with title, abstract, journal
        
    Returns:
        Generated content string
    """
    # Retrieve RAG context (guidelines/textbooks)
    guidelines = query_guidelines(article.get("title", ""), limit=3)
    guideline_context = "\n".join([f"- {g}" for g in guidelines]) if guidelines else "No specific guideline context available."
    
    user_prompt = B2B_USER_PROMPT.format(
        title=article.get("title", ""),
        journal=article.get("journal", ""),
        abstract=article.get("abstract", "")[:2500],
        guidelines=guideline_context
    )
    
    content = call_openrouter(B2B_SYSTEM_PROMPT, user_prompt, max_tokens=800)
    
    if content:
        return content.strip()
    return ""


def generate_content(article: Dict) -> Dict:
    """
    Generate content for an article based on its classification.
    
    Args:
        article: Article dictionary with classification field
        
    Returns:
        Article dictionary with generated_content field added
    """
    classification = article.get("classification", "SKIP").upper()
    
    if classification == "B2C":
        article["generated_content"] = generate_b2c_content(article)
    elif classification == "B2B":
        article["generated_content"] = generate_b2b_content(article)
    else:
        article["generated_content"] = ""
    
    return article


def generate_all_content(triaged_articles: Dict[str, list]) -> Dict[str, list]:
    """
    Generate content for all triaged articles.
    
    Args:
        triaged_articles: Dictionary with 'b2c', 'b2b', 'skip' lists
        
    Returns:
        Same structure with generated_content added to each article
    """
    print(f"\n✍️  Generating content...")
    print("-" * 40)
    
    # Generate B2C content
    b2c_count = len(triaged_articles.get("b2c", []))
    if b2c_count > 0:
        print(f"\n📢 Generating B2C content ({b2c_count} articles)...")
        for i, article in enumerate(triaged_articles["b2c"]):
            print(f"  [{i+1}/{b2c_count}] {article.get('title', '')[:45]}...")
            generate_content(article)
            if article.get("generated_content"):
                word_count = len(article["generated_content"].split())
                print(f"       ✓ Generated {word_count} words")
            else:
                print(f"       ✗ Generation failed")
    
    # Generate B2B content
    b2b_count = len(triaged_articles.get("b2b", []))
    if b2b_count > 0:
        print(f"\n👨‍⚕️ Generating B2B content ({b2b_count} articles)...")
        for i, article in enumerate(triaged_articles["b2b"]):
            print(f"  [{i+1}/{b2b_count}] {article.get('title', '')[:45]}...")
            generate_content(article)
            if article.get("generated_content"):
                word_count = len(article["generated_content"].split())
                print(f"       ✓ Generated {word_count} words")
            else:
                print(f"       ✗ Generation failed")
    
    print("-" * 40)
    
    # Count successful generations
    b2c_success = sum(1 for a in triaged_articles.get("b2c", []) if a.get("generated_content"))
    b2b_success = sum(1 for a in triaged_articles.get("b2b", []) if a.get("generated_content"))
    
    print(f"📊 Generated: {b2c_success}/{b2c_count} B2C | {b2b_success}/{b2b_count} B2B\n")
    
    return triaged_articles


if __name__ == "__main__":
    # Test with sample articles
    test_b2c = {
        "title": "Mediterranean Diet Reduces Cardiovascular Events by 30%",
        "journal": "NEJM",
        "abstract": "Background: Diet plays a crucial role in cardiovascular health. Methods: We randomized 7,500 adults to Mediterranean diet vs control. Results: Primary endpoint (MI, stroke, CV death) occurred in 3.8% vs 5.4% (HR 0.70, 95% CI 0.58-0.85). NNT was 63 over 5 years.",
        "classification": "B2C",
        "angle": "Practical dietary advice backed by rigorous evidence"
    }
    
    test_b2b = {
        "title": "FFR-Guided PCI vs Angiography-Guided PCI: 5-Year Outcomes",
        "journal": "JACC Cardiovascular Interventions",
        "abstract": "Background: FFR guidance for intermediate lesions remains debated. Methods: RCT of 1,200 patients with intermediate stenosis. FFR-guided (n=600) vs angio-guided (n=600). Primary: MACE at 5 years. Results: MACE 12.3% vs 18.1% (HR 0.66, p=0.003). TLR 5.2% vs 9.8%.",
        "classification": "B2B",
        "angle": "FFR guidance confirmation"
    }
    
    print("\n=== Testing B2C Generation ===")
    result_b2c = generate_b2c_content(test_b2c)
    if result_b2c:
        print(f"Generated {len(result_b2c.split())} words")
        print(f"\nFirst 200 chars:\n{result_b2c[:200]}...")
    else:
        print("B2C generation failed")
    
    print("\n=== Testing B2B Generation ===")
    result_b2b = generate_b2b_content(test_b2b)
    if result_b2b:
        print(f"Generated {len(result_b2b.split())} words")
        print(f"\nFirst 200 chars:\n{result_b2b[:200]}...")
    else:
        print("B2B generation failed")
