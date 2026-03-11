"""Retrieval agent that wraps vector store search."""

from app.agents.base import Agent
from app.rag.store import InMemoryVectorStore


class RetrievalAgent(Agent):
    name = "retrieval-agent"

    def __init__(self, store: InMemoryVectorStore):
        self.store = store

    def run(self, query: str, top_k: int = 3):
        return self.store.search(query=query, top_k=top_k)
