from app.agents.providers.exceptions import ProviderConfigurationError
from app.agents.providers.registry import PROVIDER_REGISTRY
from app.core.config import settings


def get_llm_provider():
    provider_name = settings.LLM_PROVIDER.lower()

    provider_factory = PROVIDER_REGISTRY.get(provider_name)

    if provider_factory is None:
        raise ProviderConfigurationError(
            f"Unsupported LLM provider: {settings.LLM_PROVIDER}"
        )

    return provider_factory()
