import os
import json
from typing import Type, TypeVar
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

T = TypeVar('T', bound=BaseModel)

class LLMService:
    _openai_client = None
    _anthropic_client = None
    _primary_model = None
    _fallback_model = None
    _max_tokens = None

    @classmethod
    def _init_config(cls):
        """Initialize LLM configuration from environment variables."""
        if cls._primary_model is None:
            cls._primary_model = os.getenv("PRIMARY_MODEL", "openai/gpt-4o")
            cls._fallback_model = os.getenv("FALLBACK_MODEL", "anthropic/claude-haiku-4-5")
            cls._max_tokens = int(os.getenv("MAX_TOKENS", "4000"))

    @classmethod
    def _get_openai_client(cls):
        """Returns a cached OpenAI client instance."""
        if cls._openai_client is None:
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key and openai_key not in ("sk-...", ""):
                from openai import OpenAI
                cls._openai_client = OpenAI(api_key=openai_key)
        return cls._openai_client

    @classmethod
    def _get_anthropic_client(cls):
        """Returns a cached Anthropic client instance."""
        if cls._anthropic_client is None:
            anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            if anthropic_key and anthropic_key not in ("sk-ant-...", ""):
                from anthropic import Anthropic
                cls._anthropic_client = Anthropic(api_key=anthropic_key)
        return cls._anthropic_client

    @classmethod
    def _get_model_provider(cls, model: str) -> str:
        """Extract provider from model string (e.g., 'openai/gpt-4o' -> 'openai')."""
        return model.split("/")[0] if "/" in model else "openai"

    @classmethod
    def _get_model_name(cls, model: str) -> str:
        """Extract model name from model string (e.g., 'openai/gpt-4o' -> 'gpt-4o')."""
        return model.split("/")[1] if "/" in model else model

    @staticmethod
    def query(prompt: str, system_prompt: str = "", temperature: float = 0.2, use_fallback: bool = False) -> str:
        """
        Sends a query to the selected LLM provider (primary or fallback).
        Supports OpenAI and Anthropic with automatic failover.
        """
        LLMService._init_config()

        model_to_use = LLMService._fallback_model if use_fallback else LLMService._primary_model
        provider = LLMService._get_model_provider(model_to_use)
        model_name = LLMService._get_model_name(model_to_use)

        try:
            if provider == "openai":
                return LLMService._query_openai(prompt, system_prompt, temperature, model_name)
            elif provider == "anthropic":
                return LLMService._query_anthropic(prompt, system_prompt, temperature, model_name)
        except Exception as e:
            print(f"Error calling {provider}: {e}")
            if not use_fallback:
                return LLMService.query(prompt, system_prompt, temperature, use_fallback=True)

        return f"MOCK LLM RESPONSE FOR PROMPT: {prompt[:100]}..."

    @staticmethod
    def _query_openai(prompt: str, system_prompt: str, temperature: float, model: str) -> str:
        """Query OpenAI API."""
        client = LLMService._get_openai_client()
        if not client:
            raise ValueError("OpenAI client not initialized")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=LLMService._max_tokens
        )
        return response.choices[0].message.content

    @staticmethod
    def _query_anthropic(prompt: str, system_prompt: str, temperature: float, model: str) -> str:
        """Query Anthropic API."""
        client = LLMService._get_anthropic_client()
        if not client:
            raise ValueError("Anthropic client not initialized")

        response = client.messages.create(
            model=model,
            max_tokens=LLMService._max_tokens,
            system=system_prompt if system_prompt else None,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.content[0].text

    @staticmethod
    def _clean_json_text(text: str) -> str:
        cleaned_text = text.strip()
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.split("```")[1]
            if cleaned_text.startswith("json"):
                cleaned_text = cleaned_text[4:]
            cleaned_text = cleaned_text.strip()
        return cleaned_text

    @staticmethod
    def query_structured(
        prompt: str,
        response_model: Type[T],
        system_prompt: str = "",
        temperature: float = 0.2,
        max_attempts: int = 2,
    ) -> T:
        """
        Queries the LLM and guarantees parsing the response into the requested Pydantic model.
        Retries once with a stricter repair prompt (and a lower temperature) if the first
        response fails to parse — the most common failure at high creative temperatures is
        the model nesting fields under an extra "properties" key instead of matching the
        schema's flat shape.
        """
        schema_json = json.dumps(response_model.model_json_schema(), indent=2)
        structured_prompt = (
            f"{prompt}\n\n"
            f"You MUST return ONLY a valid JSON object matching this schema:\n"
            f"{schema_json}\n\n"
            f"Return the fields directly at the top level (do not nest them under a "
            f"'properties' key or include the schema itself). Do not include any intro, "
            f"outro, explanations, or backticks. Return raw JSON text only."
        )

        last_error = None
        last_raw = None
        current_prompt = structured_prompt

        for attempt in range(max_attempts):
            attempt_temperature = temperature if attempt == 0 else min(temperature, 0.3)
            response_text = LLMService.query(current_prompt, system_prompt, temperature=attempt_temperature)
            cleaned_text = LLMService._clean_json_text(response_text)

            try:
                return response_model.model_validate_json(cleaned_text)
            except Exception as e:
                last_error = e
                last_raw = response_text
                current_prompt = (
                    f"{structured_prompt}\n\n"
                    f"Your previous response failed to validate against the schema.\n"
                    f"Previous response:\n{response_text}\n\n"
                    f"Validation error:\n{e}\n\n"
                    f"Return ONLY the corrected raw JSON object, with fields at the top level, "
                    f"matching the schema exactly."
                )

        raise ValueError(
            f"Failed to parse LLM response into schema {response_model.__name__} after "
            f"{max_attempts} attempt(s). Raw text: {last_raw}. Error: {last_error}"
        )

