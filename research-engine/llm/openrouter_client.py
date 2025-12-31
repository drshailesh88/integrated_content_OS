#!/usr/bin/env python3
"""
OpenRouter Client for Free LLMs

Uses free models for demand analysis to preserve Opus context for script writing.

Free models (preference order):
1. google/gemma-3-27b-it:free - Best quality
2. mistralai/mistral-7b-instruct:free - Fast fallback
3. meta-llama/llama-3-8b-instruct:free - Another option

Usage:
    from llm.openrouter_client import OpenRouterClient

    client = OpenRouterClient()
    response = client.complete("Analyze these comments...")
"""

import os
import json
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

try:
    import requests
except ImportError:
    requests = None

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Free models in preference order
FREE_MODELS = [
    "google/gemma-3-27b-it:free",
    "mistralai/mistral-7b-instruct:free",
    "meta-llama/llama-3-8b-instruct:free",
]

# Paid fallback (cheap)
FALLBACK_MODEL = "anthropic/claude-3-haiku"


class OpenRouterClient:
    """Client for OpenRouter API with free model support."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.api_key = OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

        if not self.api_key:
            print("⚠️ OPENROUTER_API_KEY not set - LLM features disabled")
        elif verbose:
            print("✅ OpenRouter client initialized")

    def complete(
        self,
        prompt: str,
        system_prompt: str = None,
        model: str = None,
        temperature: float = 0.3,
        max_tokens: int = 2000,
        json_mode: bool = False
    ) -> Optional[str]:
        """
        Complete a prompt using free LLMs.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            model: Specific model (default: try free models in order)
            temperature: Sampling temperature
            max_tokens: Max response tokens
            json_mode: Request JSON response format

        Returns:
            Response text or None if all models fail
        """
        if not self.api_key or not requests:
            return None

        models_to_try = [model] if model else FREE_MODELS + [FALLBACK_MODEL]

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        for current_model in models_to_try:
            try:
                if self.verbose:
                    print(f"   Trying {current_model}...")

                payload = {
                    "model": current_model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                if json_mode:
                    payload["response_format"] = {"type": "json_object"}

                response = requests.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://github.com/drshailesh88",
                        "X-Title": "Dr Shailesh Content System"
                    },
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

                    if self.verbose:
                        model_used = data.get("model", current_model)
                        print(f"   ✅ Success with {model_used}")

                    return content

                elif response.status_code == 429:
                    if self.verbose:
                        print(f"   ⚠️ Rate limited on {current_model}, trying next...")
                    continue

                else:
                    if self.verbose:
                        print(f"   ⚠️ {current_model} failed: {response.status_code}")
                    continue

            except Exception as e:
                if self.verbose:
                    print(f"   ⚠️ {current_model} error: {e}")
                continue

        if self.verbose:
            print("   ❌ All models failed")
        return None

    def complete_json(
        self,
        prompt: str,
        system_prompt: str = None,
        model: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Complete a prompt and parse JSON response.

        Returns parsed JSON dict or None if failed.
        """
        response = self.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            model=model,
            json_mode=True
        )

        if not response:
            return None

        try:
            # Try to extract JSON from response
            # Sometimes models wrap JSON in markdown code blocks
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]

            return json.loads(response.strip())
        except json.JSONDecodeError:
            if self.verbose:
                print(f"   ⚠️ Failed to parse JSON: {response[:100]}...")
            return None


def main():
    """Test the OpenRouter client."""
    print("=" * 50)
    print("Testing OpenRouter Client")
    print("=" * 50)

    client = OpenRouterClient(verbose=True)

    # Test basic completion
    print("\n1. Testing basic completion...")
    response = client.complete(
        "What are 3 common symptoms of heart disease? Be brief.",
        system_prompt="You are a medical assistant. Be concise."
    )

    if response:
        print(f"\nResponse:\n{response}")
    else:
        print("❌ No response received")

    # Test JSON completion
    print("\n2. Testing JSON completion...")
    json_response = client.complete_json(
        """Extract the main topics from this comment:
        "I want to know about cholesterol levels and when to worry about them.
        Also what diet should I follow for heart health?"

        Return JSON: {"topics": ["topic1", "topic2"], "intent": "question/concern/request"}""",
        system_prompt="You are a content analyzer. Return valid JSON only."
    )

    if json_response:
        print(f"\nJSON Response:\n{json.dumps(json_response, indent=2)}")
    else:
        print("❌ No JSON response received")

    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()
