from groq import Groq

from app.agents.providers.base import LLMProvider
from app.agents.providers.exceptions import ProviderConfigurationError
from app.core.config import settings


class GroqProvider(LLMProvider):
    def __init__(self) -> None:
        if not settings.GROQ_API_KEY:
            raise ProviderConfigurationError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate(
        self,
        prompt: str,
    ) -> str:
        response = self.client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""