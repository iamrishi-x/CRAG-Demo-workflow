"""Retrieval agent that wraps vector store search."""

from app.agents.base import Agent
from app.rag.store import ChunkRecord, VectorStore


class RetrievalAgent(Agent):
    name = "retrieval-agent"

    def __init__(self, stores: dict[str, VectorStore]):
        self.stores = stores

    def run(self, query: str, top_k: int = 3, backends: list[str] | None = None) -> list[tuple[ChunkRecord, float]]:
        selected = backends or list(self.stores.keys())
        scored: list[tuple[ChunkRecord, float]] = []
        for backend in selected:
            store = self.stores.get(backend)
            if store is None:
                continue
            scored.extend(store.search(query=query, top_k=top_k))
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]
