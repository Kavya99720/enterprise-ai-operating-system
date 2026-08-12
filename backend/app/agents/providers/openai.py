from openai import OpenAI

from app.agents.providers.base import LLMProvider
from app.core.config import settings


class OpenAIProvider(LLMProvider):
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        response = self.client.responses.create(
            model=settings.OPENAI_MODEL,
            input=prompt,
        )

        return response.output_text
