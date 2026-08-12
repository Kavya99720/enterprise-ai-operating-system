from app.agents.providers.base import LLMProvider
from app.agents.providers.mock import MockLLMProvider
from app.core.config import settings
from app.models.agent import Agent
from app.models.task import Task


def get_provider() -> LLMProvider:
    provider_name = settings.LLM_PROVIDER.lower()

    if provider_name == "mock":
        return MockLLMProvider()

    raise ValueError(
        f"Unsupported LLM provider: {settings.LLM_PROVIDER}"
    )


def run_agent(
    agent: Agent,
    task: Task,
) -> str:
    provider = get_provider()

    prompt = (
        f"You are {agent.name}, whose role is {agent.role}. "
        f"Your capabilities are: {agent.capabilities or 'not specified'}. "
        f"Execute the following task:\n\n"
        f"Title: {task.title}\n"
        f"Description: {task.description or 'No description provided.'}"
    )

    return provider.generate(prompt)
