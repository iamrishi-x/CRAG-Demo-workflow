"""Generation agent for response synthesis."""

from app.agents.base import Agent


class GenerationAgent(Agent):
    name = "generation-agent"

    def run(self, query: str, contexts: list[str]) -> str:
        if not contexts:
            return "I could not find relevant context for your question."
        context = "\n".join(f"- {chunk}" for chunk in contexts[:3])
        return f"Answer based on retrieved context for '{query}':\n{context}"
