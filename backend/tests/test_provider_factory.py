import pytest

from app.agents.providers.exceptions import ProviderConfigurationError
from app.agents.providers.factory import get_llm_provider
from app.agents.providers.groq import GroqProvider
from app.core.config import settings


def test_factory_returns_groq_provider():
    original_provider = settings.LLM_PROVIDER
    settings.LLM_PROVIDER = "groq"

    try:
        provider = get_llm_provider()
        assert isinstance(provider, GroqProvider)
    finally:
        settings.LLM_PROVIDER = original_provider


def test_factory_rejects_unsupported_provider():
    original_provider = settings.LLM_PROVIDER
    settings.LLM_PROVIDER = "unsupported-provider"

    try:
        with pytest.raises(ProviderConfigurationError):
            get_llm_provider()
    finally:
        settings.LLM_PROVIDER = original_provider
