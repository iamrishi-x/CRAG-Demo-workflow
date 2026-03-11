"""Config-driven RAG pipeline entrypoint."""

from app.agents.generation_agent import GenerationAgent
from app.agents.orchestrator import RagOrchestrator
from app.agents.retrieval_agent import RetrievalAgent
from app.core.config import settings
from app.rag.chunker import chunk_text
from app.rag.store import InMemoryVectorStore


class RagPipeline:
    def __init__(self):
        dims = int(settings.get("rag.vector_dimensions", 512))
        self.store = InMemoryVectorStore(dimensions=dims)
        self.retrieval = RetrievalAgent(self.store)
        self.generation = GenerationAgent()
        self.orchestrator = RagOrchestrator(self.retrieval, self.generation)
        self.chunk_size = int(settings.get("rag.chunk_size", 500))
        self.chunk_overlap = int(settings.get("rag.chunk_overlap", 50))

    def ingest(self, document_id: str, text: str) -> int:
        chunks = chunk_text(text=text, chunk_size=self.chunk_size, overlap=self.chunk_overlap)
        for idx, chunk in enumerate(chunks):
            self.store.add_chunk(document_id=document_id, chunk_id=f"{document_id}-{idx}", text=chunk)
        return len(chunks)

    def query(self, text: str, top_k: int = 3):
        return self.orchestrator.answer(query=text, top_k=top_k)
