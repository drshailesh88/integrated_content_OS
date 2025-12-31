"""
LLM client for content generation.
Supports OpenRouter (Claude 3.5 Sonnet) and direct Anthropic API.
"""

import json
from typing import Optional
import httpx

from ..config import config


class LLMClient:
    """Unified LLM client supporting multiple providers."""

    def __init__(self):
        self.config = config.llm
        self.openai_config = config.openai

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        json_mode: bool = False,
    ) -> str:
        """
        Generate text using the configured LLM.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            max_tokens: Max tokens to generate
            temperature: Sampling temperature
            json_mode: If True, request JSON output

        Returns:
            Generated text response
        """
        max_tokens = max_tokens or self.config.max_tokens
        temperature = temperature or self.config.temperature

        # Try OpenRouter first, fall back to Anthropic
        if self.config.openrouter_api_key:
            return await self._generate_openrouter(
                prompt, system_prompt, max_tokens, temperature, json_mode
            )
        elif self.config.anthropic_api_key:
            return await self._generate_anthropic(
                prompt, system_prompt, max_tokens, temperature, json_mode
            )
        else:
            raise ValueError("No LLM API key configured")

    async def _generate_openrouter(
        self,
        prompt: str,
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
        json_mode: bool,
    ) -> str:
        """Generate using OpenRouter API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.config.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://twitter-content-system.local",
            "X-Title": "Twitter Content System",
        }

        payload = {
            "model": self.config.openrouter_model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
        json_mode: bool,
    ) -> str:
        """Generate using direct Anthropic API."""
        headers = {
            "x-api-key": self.config.anthropic_api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.config.anthropic_model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }

        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]

    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> dict:
        """Generate and parse JSON response."""
        response = await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            json_mode=True,
        )

        # Try to extract JSON from the response
        import re

        # Clean up common issues
        cleaned = response.strip()

        # Remove markdown code blocks if present
        if cleaned.startswith("```"):
            cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
            cleaned = re.sub(r'\s*```$', '', cleaned)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Try to find JSON object in the response
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass

            # Try more aggressive extraction - find outermost braces
            start = response.find('{')
            end = response.rfind('}')
            if start != -1 and end > start:
                try:
                    return json.loads(response[start:end+1])
                except json.JSONDecodeError:
                    pass

            raise ValueError(f"Could not parse JSON from response: {response[:200]}")

    async def generate_gemini(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Generate using Gemini 2.5 Flash (cheap and fast).

        Cost: ~$0.15/1M input, $0.60/1M output tokens
        ~20-50x cheaper than Claude Sonnet

        Note: Gemini 2.5 Flash uses internal "thinking" tokens before producing
        output, so ensure max_tokens is high enough for both thinking + output.
        """
        from ..config import config

        api_key = config.gemini.api_key
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")

        # Ensure enough tokens for thinking + output
        max_tokens = max(max_tokens or 4096, 256)
        temperature = temperature or 0.7

        # Build the prompt with system instruction
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n---\n\n{prompt}"

        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
            }
        }

        model = config.gemini.model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

            # Extract text from response, handling edge cases
            candidates = data.get("candidates", [])
            if not candidates:
                raise ValueError(f"No candidates in Gemini response: {data}")

            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if not parts:
                # May have hit token limit before producing output
                finish_reason = candidates[0].get("finishReason", "UNKNOWN")
                raise ValueError(f"No output parts, finishReason: {finish_reason}")

            return parts[0].get("text", "")

    async def get_embedding(self, text: str) -> list[float]:
        """
        Get embedding for text using OpenAI's embedding model.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        headers = {
            "Authorization": f"Bearer {self.openai_config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.openai_config.embedding_model,
            "input": text,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/embeddings",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["data"][0]["embedding"]


# Singleton instance
llm_client = LLMClient()
