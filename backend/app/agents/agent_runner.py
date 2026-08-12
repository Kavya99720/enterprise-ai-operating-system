from app.agents.providers.base import LLMProvider
from app.agents.providers.factory import get_llm_provider
from app.models.agent import Agent
from app.models.task import Task


def get_provider() -> LLMProvider:
    return get_llm_provider()


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
