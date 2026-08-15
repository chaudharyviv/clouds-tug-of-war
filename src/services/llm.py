import os
import json
from typing import Type, TypeVar
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

T = TypeVar('T', bound=BaseModel)

class LLMService:
    @staticmethod
    def query(prompt: str, system_prompt: str = "") -> str:
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
                    temperature=0.2
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Error calling OpenAI: {e}")
                
        # Mock fallback for demonstration / offline use
        return f"MOCK LLM RESPONSE FOR PROMPT: {prompt[:100]}..."

    @staticmethod
    def query_structured(prompt: str, response_model: Type[T], system_prompt: str = "") -> T:
        """
        Queries the LLM and guarantees parsing the response into the requested Pydantic model.
        """
        structured_prompt = (
            f"{prompt}\n\n"
            f"You MUST return ONLY a valid JSON object matching this schema:\n"
            f"{json.dumps(response_model.model_json_schema(), indent=2)}\n\n"
            f"Do not include any intro, outro, explanations, or backticks. Return raw JSON text only."
        )
        
        response_text = LLMService.query(structured_prompt, system_prompt)
        
        # Clean response text in case it wrapped in ```json ... ```
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.split("```")[1]
            if cleaned_text.startswith("json"):
                cleaned_text = cleaned_text[4:]
            cleaned_text = cleaned_text.strip()
            
        try:
            return response_model.model_validate_json(cleaned_text)
        except Exception as e:
            # Fallback parsing/handling logic or raising error for agent debugging
            raise ValueError(f"Failed to parse LLM response into schema {response_model.__name__}. Raw text: {response_text}. Error: {e}")
