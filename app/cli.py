"""CLI entrypoint for local and batch RAG operations."""

import json
from pathlib import Path

import typer
from rich import print

from app.rag.pipeline import RagPipeline

app = typer.Typer(help="RAG CLI")


@app.command("ingest")
def ingest(document_id: str, file: Path, backends: str = "") -> None:
    text = file.read_text(encoding="utf-8")
    pipeline = RagPipeline()
    selected = [item.strip() for item in backends.split(",") if item.strip()] or None
    chunks = pipeline.ingest(document_id=document_id, text=text, backends=selected)
    print({"document_id": document_id, "chunks_indexed": chunks, "backends": selected or "all"})


@app.command("query")
def query(text: str, top_k: int = 3, backends: str = "", llm_provider: str = "") -> None:
    pipeline = RagPipeline()
    selected = [item.strip() for item in backends.split(",") if item.strip()] or None
    provider = llm_provider or None
    answer, hits = pipeline.query(text=text, top_k=top_k, backends=selected, llm_provider=provider)
    response = {
        "answer": answer,
        "sources": [
            {
                "document_id": rec.document_id,
                "chunk_id": rec.chunk_id,
                "score": score,
                "backend": rec.backend,
            }
            for rec, score in hits
        ],
    }
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    app()
