from collections.abc import Callable

from app.agents.providers.base import LLMProvider
from app.agents.providers.mock import MockLLMProvider
from app.agents.providers.openai import OpenAIProvider
from app.agents.providers.groq import GroqProvider

PROVIDER_REGISTRY: dict[str, Callable[[], LLMProvider]] = {
    "mock": MockLLMProvider,
    "openai": OpenAIProvider,
    "groq": GroqProvider,

}
