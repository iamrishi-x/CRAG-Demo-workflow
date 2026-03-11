"""Agent orchestrator for modular RAG flow."""

from app.agents.generation_agent import GenerationAgent
from app.agents.retrieval_agent import RetrievalAgent


class RagOrchestrator:
    def __init__(self, retrieval_agent: RetrievalAgent, generation_agent: GenerationAgent):
        self.retrieval_agent = retrieval_agent
        self.generation_agent = generation_agent

    def answer(self, query: str, top_k: int = 3, backends: list[str] | None = None, llm_provider: str | None = None):
        hits = self.retrieval_agent.run(query=query, top_k=top_k, backends=backends)
        contexts = [record.text for record, _ in hits]
        answer = self.generation_agent.run(query=query, contexts=contexts, provider_name=llm_provider)
        return answer, hits
