"""Generation agent for response synthesis with pluggable providers."""

from app.agents.base import Agent
from app.llm.providers import PROVIDERS


class GenerationAgent(Agent):
    name = "generation-agent"

    def __init__(self, providers_config: dict[str, dict], default_provider: str):
        self.providers_config = providers_config
        self.default_provider = default_provider

    def run(self, query: str, contexts: list[str], provider_name: str | None = None) -> str:
        active = provider_name or self.default_provider
        provider = PROVIDERS.get(active)
        if provider is None:
            available = ", ".join(sorted(PROVIDERS))
            return f"Unknown provider '{active}'. Available providers: {available}"
        config = self.providers_config.get(active, {})
        return provider(query=query, contexts=contexts, config=config)
