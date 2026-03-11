"""RAG API routes."""

from fastapi import APIRouter

from app.models.schemas import DocumentIn, QueryIn, QueryOut, SourceChunk
from app.rag.pipeline import RagPipeline

router = APIRouter(prefix="/rag", tags=["rag"])
pipeline = RagPipeline()


@router.post("/documents")
def add_document(payload: DocumentIn) -> dict[str, str | int]:
    total = pipeline.ingest(document_id=payload.document_id, text=payload.text)
    return {"status": "ok", "chunks_indexed": total}


@router.post("/query", response_model=QueryOut)
def query(payload: QueryIn) -> QueryOut:
    answer, hits = pipeline.query(payload.query, top_k=payload.top_k)
    sources = [
        SourceChunk(
            document_id=record.document_id,
            chunk_id=record.chunk_id,
            text=record.text,
            score=score,
        )
        for record, score in hits
    ]
    return QueryOut(answer=answer, sources=sources)
