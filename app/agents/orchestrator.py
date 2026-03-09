"""Agent orchestrator for modular RAG flow."""

from app.agents.generation_agent import GenerationAgent
from app.agents.retrieval_agent import RetrievalAgent


class RagOrchestrator:
    def __init__(self, retrieval_agent: RetrievalAgent, generation_agent: GenerationAgent):
        self.retrieval_agent = retrieval_agent
        self.generation_agent = generation_agent

    def answer(self, query: str, top_k: int = 3):
        hits = self.retrieval_agent.run(query=query, top_k=top_k)
        contexts = [record.text for record, _ in hits]
        answer = self.generation_agent.run(query=query, contexts=contexts)
        return answer, hits
