"""Config-driven RAG pipeline with multi-store and multi-LLM support."""

from __future__ import annotations

from app.agents.generation_agent import GenerationAgent
from app.agents.orchestrator import RagOrchestrator
from app.agents.retrieval_agent import RetrievalAgent
from app.core.config import settings
from app.rag.chunker import chunk_text
from app.rag.store import InMemoryVectorStore, SQLiteVectorStore, VectorStore


class RagPipeline:
    def __init__(self):
        rag = settings.get("rag", {})
        self.chunk_size = int(rag.get("chunk_size", 500))
        self.chunk_overlap = int(rag.get("chunk_overlap", 50))
        self.dimensions = int(rag.get("vector_dimensions", 512))
        self.stores = self._build_stores()
        llm_cfg = settings.get("llm", {})
        self.retrieval = RetrievalAgent(self.stores)
        self.generation = GenerationAgent(
            providers_config=llm_cfg.get("providers", {}),
            default_provider=llm_cfg.get("default_provider", "echo"),
        )
        self.orchestrator = RagOrchestrator(self.retrieval, self.generation)

    def _build_stores(self) -> dict[str, VectorStore]:
        backends = settings.get("vector_backends") or [{"name": "memory", "type": "in_memory", "enabled": True}]
        stores: dict[str, VectorStore] = {}
        for backend in backends:
            if not backend.get("enabled", True):
                continue
            name = backend["name"]
            btype = backend.get("type", "in_memory")
            if btype == "in_memory":
                stores[name] = InMemoryVectorStore(name=name, dimensions=self.dimensions)
            elif btype == "sqlite":
                stores[name] = SQLiteVectorStore(
                    name=name,
                    db_path=backend.get("path", "data/vector.db"),
                    dimensions=self.dimensions,
                )
        if not stores:
            stores["memory"] = InMemoryVectorStore(name="memory", dimensions=self.dimensions)
        return stores

    def ingest(self, document_id: str, text: str, backends: list[str] | None = None) -> int:
        chunks = chunk_text(text=text, chunk_size=self.chunk_size, overlap=self.chunk_overlap)
        selected = backends or list(self.stores.keys())
        for idx, chunk in enumerate(chunks):
            for backend in selected:
                store = self.stores.get(backend)
                if store is None:
                    continue
                store.add_chunk(document_id=document_id, chunk_id=f"{document_id}-{backend}-{idx}", text=chunk)
        return len(chunks)

    def query(
        self,
        text: str,
        top_k: int = 3,
        backends: list[str] | None = None,
        llm_provider: str | None = None,
    ):
        return self.orchestrator.answer(
            query=text,
            top_k=top_k,
            backends=backends,
            llm_provider=llm_provider,
        )

    def clear(self) -> None:
        for store in self.stores.values():
            store.clear()
