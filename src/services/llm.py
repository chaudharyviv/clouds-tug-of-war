import os
import json
from typing import Type, TypeVar
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

T = TypeVar('T', bound=BaseModel)

class LLMService:
    @staticmethod
    def query(prompt: str, system_prompt: str = "", temperature: float = 0.2) -> str:
        """
        Sends a query to the selected LLM provider.
        Supports OpenAI, with a mock fallback for testing.
        """
        # Read API Keys from environment
        openai_key = os.getenv("OPENAI_API_KEY")

        if openai_key and not openai_key.startswith("sk-..."):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=temperature,
                    max_tokens=4000
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Error calling OpenAI: {e}")

        # Mock fallback for demonstration / offline use
        return f"MOCK LLM RESPONSE FOR PROMPT: {prompt[:100]}..."

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
