"""
AI Triage Module
Classifies articles as B2C, B2B, or SKIP using OpenRouter API.
"""

import requests
import json
import re
from typing import Dict, Optional
import sys
sys.path.insert(0, '..')
from config import (
    OPENROUTER_API_KEY, OPENROUTER_BASE_URL, AI_MODEL,
    TRIAGE_SYSTEM_PROMPT, TRIAGE_USER_PROMPT, REQUEST_TIMEOUT
)


def call_openrouter(system_prompt: str, user_prompt: str, max_tokens: int = 500) -> Optional[str]:
    """
    Make a call to OpenRouter API.
    
    Args:
        system_prompt: System prompt for the AI
        user_prompt: User prompt with article content
        max_tokens: Maximum tokens in response
        
    Returns:
        AI response text or None if failed
    """
    if not OPENROUTER_API_KEY:
        print("  ⚠ OPENROUTER_API_KEY not set")
        return None
    
    try:
        response = requests.post(
            OPENROUTER_BASE_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": AI_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.3
            },
            timeout=REQUEST_TIMEOUT * 2  # AI calls can take longer
        )
        response.raise_for_status()
        data = response.json()
        
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        return None
        
    except requests.exceptions.Timeout:
        print("  ⚠ AI request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ⚠ AI request error: {e}")
        return None
    except Exception as e:
        print(f"  ⚠ Unexpected error: {e}")
        return None


def parse_triage_response(response: str) -> Dict:
    """
    Parse the JSON response from triage prompt.
    
    Args:
        response: Raw AI response string
        
    Returns:
        Dictionary with classification, confidence, reasoning, angle
    """
    default_result = {
        "classification": "SKIP",
        "confidence": 1,
        "reasoning": "Failed to parse AI response",
        "angle": ""
    }
    
    if not response:
        return default_result
    
    try:
        # Try to extract JSON from response (handle markdown code blocks)
        json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            result = json.loads(json_str)
            
            # Validate and normalize
            classification = result.get("classification", "SKIP").upper()
            if classification not in ["B2C", "B2B", "SKIP"]:
                classification = "SKIP"
            
            return {
                "classification": classification,
                "confidence": min(max(int(result.get("confidence", 5)), 1), 10),
                "reasoning": result.get("reasoning", ""),
                "angle": result.get("angle", "")
            }
    except (json.JSONDecodeError, ValueError) as e:
        pass
    
    # Fallback: try to find classification in plain text
    response_upper = response.upper()
    if "B2C" in response_upper:
        default_result["classification"] = "B2C"
        default_result["confidence"] = 5
    elif "B2B" in response_upper:
        default_result["classification"] = "B2B"
        default_result["confidence"] = 5
    
    return default_result


def triage_article(article: Dict) -> Dict:
    """
    Classify a single article using AI.
    
    Args:
        article: Article dictionary with title, abstract, journal
        
    Returns:
        Article dictionary with classification fields added
    """
    # Build the prompt
    user_prompt = TRIAGE_USER_PROMPT.format(
        title=article.get("title", ""),
        journal=article.get("journal", ""),
        abstract=article.get("abstract", "")[:2000]  # Limit abstract length
    )
    
    # Call AI
    response = call_openrouter(TRIAGE_SYSTEM_PROMPT, user_prompt, max_tokens=300)
    
    # Parse response
    result = parse_triage_response(response)
    
    # Add to article
    article["classification"] = result["classification"]
    article["confidence"] = result["confidence"]
    article["triage_reasoning"] = result["reasoning"]
    article["angle"] = result["angle"]
    
    return article


def triage_articles(articles: list, min_confidence: int = 5) -> Dict[str, list]:
    """
    Triage multiple articles and group by classification.
    
    Args:
        articles: List of article dictionaries
        min_confidence: Minimum confidence to include (1-10)
        
    Returns:
        Dictionary with 'b2c', 'b2b', 'skip' lists
    """
    print(f"\n🤖 Triaging {len(articles)} articles...")
    print("-" * 40)
    
    results = {
        "b2c": [],
        "b2b": [],
        "skip": []
    }
    
    for i, article in enumerate(articles):
        # Show progress
        print(f"  [{i+1}/{len(articles)}] {article.get('title', '')[:50]}...")
        
        # Triage
        triaged = triage_article(article)
        classification = triaged["classification"].lower()
        
        # Add to appropriate list if meets confidence threshold
        if triaged["confidence"] >= min_confidence:
            results[classification].append(triaged)
        else:
            results["skip"].append(triaged)
        
        # Show result
        symbol = "📢" if classification == "b2c" else "👨‍⚕️" if classification == "b2b" else "⏭"
        print(f"       {symbol} {classification.upper()} (confidence: {triaged['confidence']})")
    
    print("-" * 40)
    print(f"📊 Results: {len(results['b2c'])} B2C | {len(results['b2b'])} B2B | {len(results['skip'])} SKIP\n")
    
    return results


if __name__ == "__main__":
    # Test with a sample article
    test_article = {
        "title": "SGLT2 Inhibitors Reduce Heart Failure Hospitalizations in Diabetic Patients",
        "journal": "NEJM",
        "abstract": "Background: SGLT2 inhibitors have shown cardiovascular benefits. Methods: We conducted a randomized trial of 10,000 patients with type 2 diabetes. Results: The primary endpoint of heart failure hospitalization occurred in 5.3% of the treatment group vs 8.2% in placebo (HR 0.65, 95% CI 0.55-0.77)."
    }
    
    result = triage_article(test_article)
    print(f"\nTest result:")
    print(f"  Classification: {result['classification']}")
    print(f"  Confidence: {result['confidence']}")
    print(f"  Reasoning: {result.get('triage_reasoning', 'N/A')}")
    print(f"  Angle: {result.get('angle', 'N/A')}")
