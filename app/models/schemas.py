"""Pydantic request/response models."""

from pydantic import BaseModel, Field


class DocumentIn(BaseModel):
    document_id: str = Field(..., description="Unique document id")
    text: str = Field(..., min_length=1, description="Document text")
    metadata: dict[str, str] | None = Field(default_factory=dict)


class QueryIn(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(3, ge=1, le=20)


class SourceChunk(BaseModel):
    document_id: str
    chunk_id: str
    text: str
    score: float


class QueryOut(BaseModel):
    answer: str
    sources: list[SourceChunk]
