#!/usr/bin/env python3
"""
Knowledge Synthesizer

Uses an LLM to synthesize retrieved chunks into comprehensive knowledge briefs.

Features:
- Fact-focused synthesis (not creative writing)
- Structured output with sections
- Source tracking for transparency
- Cost-efficient (GPT-4o-mini)

Usage:
    from src.synthesizer import KnowledgeSynthesizer
    
    synthesizer = KnowledgeSynthesizer()
    result = synthesizer.synthesize(query, chunks)
"""

import os
import sys
import json
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:
    print("❌ Error: openai not installed")
    sys.exit(1)

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuration
SYNTHESIS_MODEL = os.getenv("SYNTHESIS_MODEL", "gpt-4o-mini")
MAX_TOKENS = int(os.getenv("SYNTHESIS_MAX_TOKENS", "2048"))
TEMPERATURE = float(os.getenv("SYNTHESIS_TEMPERATURE", "0.1"))


class KnowledgeSynthesizer:
    """Synthesizes knowledge from retrieved chunks."""
    
    def __init__(self, custom_prompt: str = None):
        """
        Initialize the synthesizer.
        
        Args:
            custom_prompt: Optional custom synthesis prompt template
        """
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.custom_prompt = custom_prompt
        print(f"✅ Synthesizer initialized (using {SYNTHESIS_MODEL})")
    
    def _create_default_prompt(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        """Create the default synthesis prompt."""
        
        # Format chunks with source citations
        formatted_chunks = []
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk.get("metadata", {})
            source = metadata.get("source", "Unknown source")
            page = metadata.get("page", "N/A")
            content = chunk.get("content", "")
            
            formatted_chunks.append(
                f"[Source {i}: {source}, page {page}]\n{content}\n"
            )
        
        chunks_text = "\n---\n".join(formatted_chunks)
        
        prompt = f"""You are a knowledge synthesizer. Your task is to synthesize information from retrieved sources into a comprehensive, factual brief.

QUERY: {query}

RETRIEVED SOURCES:
{chunks_text}

YOUR TASK:
Synthesize the above sources into a comprehensive, factual knowledge brief.

STRUCTURE YOUR BRIEF AS FOLLOWS:

## Summary
[2-3 sentence executive summary]

## Key Points
[Main findings and information organized logically]

## Evidence & Details
[Specific data, statistics, and supporting information from sources]

## Practical Applications
[How this information can be applied or used]

## Limitations & Gaps
[What's missing or uncertain in the available information]

## Sources Summary
[Brief list of sources used]

CRITICAL RULES:
1. Extract ONLY facts from the provided sources - no hallucinations
2. Include specific numbers, statistics, and data where available
3. If sources conflict, mention both viewpoints
4. If a section has no information in sources, write "Not covered in provided sources"
5. Use clear, professional language
6. Maintain nuance - avoid oversimplification
7. DO NOT add information beyond what sources state

Generate the synthesis now:"""
        
        return prompt
    
    def synthesize(
        self,
        query: str,
        chunks: List[Dict[str, Any]],
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Synthesize retrieved chunks into a knowledge brief.
        
        Args:
            query: The original query
            chunks: List of retrieved chunks with metadata
            verbose: Print synthesis details
        
        Returns:
            Dict with synthesis, metadata, and cost info
        """
        if not chunks:
            return {
                "query": query,
                "synthesis": "No relevant information found in knowledge base.",
                "sources_used": [],
                "cost_usd": 0,
                "error": "No chunks provided"
            }
        
        if verbose:
            print(f"\n🔬 Synthesizing knowledge for: {query}")
            print(f"   Using {len(chunks)} chunks")
            print("=" * 60)
        
        # Create synthesis prompt
        if self.custom_prompt:
            prompt = self.custom_prompt.format(query=query, chunks=chunks)
        else:
            prompt = self._create_default_prompt(query, chunks)
        
        if verbose:
            print(f"📝 Prompt length: {len(prompt)} characters")
        
        # Call LLM
        try:
            response = self.openai_client.chat.completions.create(
                model=SYNTHESIS_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a knowledge synthesizer. Extract and organize facts from provided sources with high precision."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            
            synthesis = response.choices[0].message.content
            
            # Extract usage info for cost calculation
            usage = response.usage
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens
            
            # Cost calculation (GPT-4o-mini pricing)
            input_cost = (input_tokens / 1_000_000) * 0.15
            output_cost = (output_tokens / 1_000_000) * 0.60
            total_cost = input_cost + output_cost
            
            # Extract unique sources
            sources_used = []
            seen_sources = set()
            for chunk in chunks:
                metadata = chunk.get("metadata", {})
                source = metadata.get("source", "Unknown")
                if source not in seen_sources:
                    sources_used.append({
                        "source": source,
                        "type": metadata.get("type", "unknown"),
                        "year": metadata.get("year"),
                        "page": metadata.get("page")
                    })
                    seen_sources.add(source)
            
            result = {
                "query": query,
                "synthesis": synthesis,
                "sources_used": sources_used,
                "num_chunks": len(chunks),
                "tokens": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens
                },
                "cost_usd": round(total_cost, 6),
                "model": SYNTHESIS_MODEL,
                "timestamp": datetime.now().isoformat()
            }
            
            if verbose:
                print(f"✅ Synthesis complete!")
                print(f"   Input tokens: {input_tokens}")
                print(f"   Output tokens: {output_tokens}")
                print(f"   Cost: ${total_cost:.6f}")
                print(f"   Sources used: {len(sources_used)}")
                print("=" * 60)
            
            return result
        
        except Exception as e:
            print(f"❌ Synthesis failed: {e}")
            return {
                "query": query,
                "synthesis": "",
                "sources_used": [],
                "cost_usd": 0,
                "error": str(e)
            }
    
    def save_synthesis(self, result: Dict[str, Any], output_path: str):
        """Save synthesis result to a file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"💾 Synthesis saved to: {output_path}")


def main():
    """Test the synthesizer."""
    print("=" * 60)
    print("🧪 Testing Knowledge Synthesizer")
    print("=" * 60)
    
    synthesizer = KnowledgeSynthesizer()
    
    # Mock chunks for testing
    test_chunks = [
        {
            "content": "Machine learning models require large amounts of data for training. Typical datasets range from thousands to millions of examples depending on the complexity of the task.",
            "metadata": {
                "source": "ML Handbook.pdf",
                "page": 23,
                "type": "textbook",
                "year": 2023
            }
        },
        {
            "content": "Neural networks with more layers (deep learning) can learn more complex patterns but require more computational resources and training time.",
            "metadata": {
                "source": "Deep Learning Guide.pdf",
                "page": 45,
                "type": "reference",
                "year": 2024
            }
        },
        {
            "content": "Transfer learning allows pre-trained models to be adapted to new tasks with smaller datasets, reducing training time by up to 90% in some cases.",
            "metadata": {
                "source": "AI Best Practices.pdf",
                "page": 12,
                "type": "guideline",
                "year": 2024
            }
        }
    ]
    
    test_query = "What are the data requirements for training machine learning models?"
    
    print(f"\n📝 Test Query: {test_query}\n")
    
    result = synthesizer.synthesize(test_query, test_chunks, verbose=True)
    
    print("\n📄 SYNTHESIS RESULT:")
    print("=" * 60)
    print(result["synthesis"])
    print("=" * 60)
    print(f"\n💰 Cost: ${result['cost_usd']}")
    print(f"📚 Sources: {len(result['sources_used'])}")
    
    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()
