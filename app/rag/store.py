"""In-memory vector store for demo purposes."""

from dataclasses import dataclass

from app.rag.embeddings import cosine_similarity, embed_text


@dataclass
class ChunkRecord:
    document_id: str
    chunk_id: str
    text: str
    vector: list[float]


class InMemoryVectorStore:
    def __init__(self, dimensions: int = 512):
        self.dimensions = dimensions
        self._records: list[ChunkRecord] = []

    def add_chunk(self, document_id: str, chunk_id: str, text: str) -> None:
        self._records.append(
            ChunkRecord(
                document_id=document_id,
                chunk_id=chunk_id,
                text=text,
                vector=embed_text(text, dimensions=self.dimensions),
            )
        )

    def search(self, query: str, top_k: int = 3) -> list[tuple[ChunkRecord, float]]:
        qv = embed_text(query, dimensions=self.dimensions)
        scored = [(record, cosine_similarity(qv, record.vector)) for record in self._records]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def clear(self) -> None:
        self._records.clear()
