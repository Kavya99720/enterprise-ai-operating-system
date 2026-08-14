from app.agents.agent_runner import run_agent
from app.models.agent import Agent
from app.models.task import Task


class RecordingProvider:
    def __init__(self):
        self.received_prompt = None

    def generate(self, prompt: str) -> str:
        self.received_prompt = prompt
        return "Test provider response"


def test_run_agent_builds_prompt_and_returns_response(monkeypatch):
    provider = RecordingProvider()

    monkeypatch.setattr(
        "app.agents.agent_runner.get_provider",
        lambda: provider,
    )

    agent = Agent(
        id=1,
        name="Data Analyst",
        role="Data Scientist",
        capabilities="Python, SQL, Machine Learning",
    )

    task = Task(
        id=1,
        title="Analyze sales data",
        description="Identify the top-performing products.",
    )

    result = run_agent(agent, task)

    assert result == "Test provider response"
    assert provider.received_prompt is not None
    assert "Data Analyst" in provider.received_prompt
    assert "Data Scientist" in provider.received_prompt
    assert "Python, SQL, Machine Learning" in provider.received_prompt
    assert "Analyze sales data" in provider.received_prompt
    assert "Identify the top-performing products." in provider.received_prompt


def test_run_agent_handles_missing_capabilities(monkeypatch):
    provider = RecordingProvider()

    monkeypatch.setattr(
        "app.agents.agent_runner.get_provider",
        lambda: provider,
    )

    agent = Agent(
        id=2,
        name="Research Agent",
        role="Researcher",
        capabilities=None,
    )

    task = Task(
        id=2,
        title="Research AI trends",
        description=None,
    )

    result = run_agent(agent, task)

    assert result == "Test provider response"
    assert provider.received_prompt is not None
    assert "capabilities are: not specified" in provider.received_prompt
    assert "Research AI trends" in provider.received_prompt
    assert "No description provided." in provider.received_prompt
