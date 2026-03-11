"""Pydantic request/response models."""

from pydantic import BaseModel, Field


class DocumentIn(BaseModel):
    document_id: str = Field(..., description="Unique document id")
    text: str = Field(..., min_length=1, description="Document text")
    metadata: dict[str, str] | None = Field(default_factory=dict)
    backends: list[str] | None = Field(default=None, description="Optional target vector backends")


class QueryIn(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(3, ge=1, le=20)
    backends: list[str] | None = Field(default=None, description="Optional retrieval backends")
    llm_provider: str | None = Field(default=None, description="Override configured LLM provider")


class SourceChunk(BaseModel):
    document_id: str
    chunk_id: str
    text: str
    score: float
    backend: str


class QueryOut(BaseModel):
    answer: str
    sources: list[SourceChunk]
