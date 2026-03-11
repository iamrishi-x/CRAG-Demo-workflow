"""Vector store providers (in-memory + sqlite) for local multi-db retrieval."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from app.rag.embeddings import cosine_similarity, embed_text


@dataclass
class ChunkRecord:
    document_id: str
    chunk_id: str
    text: str
    vector: list[float]
    backend: str


class VectorStore:
    """Minimal interface for vector stores."""

    name: str

    def add_chunk(self, document_id: str, chunk_id: str, text: str) -> None: ...

    def search(self, query: str, top_k: int = 3) -> list[tuple[ChunkRecord, float]]: ...

    def clear(self) -> None: ...


class InMemoryVectorStore(VectorStore):
    def __init__(self, name: str, dimensions: int = 512):
        self.name = name
        self.dimensions = dimensions
        self._records: list[ChunkRecord] = []

    def add_chunk(self, document_id: str, chunk_id: str, text: str) -> None:
        self._records.append(
            ChunkRecord(
                document_id=document_id,
                chunk_id=chunk_id,
                text=text,
                vector=embed_text(text, dimensions=self.dimensions),
                backend=self.name,
            )
        )

    def search(self, query: str, top_k: int = 3) -> list[tuple[ChunkRecord, float]]:
        qv = embed_text(query, dimensions=self.dimensions)
        scored = [(record, cosine_similarity(qv, record.vector)) for record in self._records]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def clear(self) -> None:
        self._records.clear()


class SQLiteVectorStore(VectorStore):
    """SQLite-backed local vector store using JSON-serialized vectors."""

    def __init__(self, name: str, db_path: str, dimensions: int = 512):
        self.name = name
        self.db_path = db_path
        self.dimensions = dimensions
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    document_id TEXT NOT NULL,
                    chunk_id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    vector TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add_chunk(self, document_id: str, chunk_id: str, text: str) -> None:
        vector = embed_text(text, dimensions=self.dimensions)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO chunks (document_id, chunk_id, text, vector)
                VALUES (?, ?, ?, ?)
                """,
                (document_id, chunk_id, text, json.dumps(vector)),
            )
            conn.commit()

    def search(self, query: str, top_k: int = 3) -> list[tuple[ChunkRecord, float]]:
        qv = embed_text(query, dimensions=self.dimensions)
        rows: list[tuple[str, str, str, str]]
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT document_id, chunk_id, text, vector FROM chunks").fetchall()

        scored: list[tuple[ChunkRecord, float]] = []
        for document_id, chunk_id, text, vector_json in rows:
            vector = [float(v) for v in json.loads(vector_json)]
            record = ChunkRecord(
                document_id=document_id,
                chunk_id=chunk_id,
                text=text,
                vector=vector,
                backend=self.name,
            )
            scored.append((record, cosine_similarity(qv, vector)))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def clear(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM chunks")
            conn.commit()
