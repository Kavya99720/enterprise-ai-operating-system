from app.agents.providers.base import LLMProvider


class MockLLMProvider(LLMProvider):
    def generate(
        self,
        prompt: str,
    ) -> str:
        return f"Mock LLM response for: {prompt}"
