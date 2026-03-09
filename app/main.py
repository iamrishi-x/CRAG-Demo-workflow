"""FastAPI app bootstrap."""

import logging

from fastapi import FastAPI

from app.api.routes.rag import router as rag_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.get("app.name", "RAG FastAPI"),
    version=settings.get("app.version", "0.1.0"),
)
app.include_router(rag_router)


@app.get("/health")
def health() -> dict[str, str]:
    logger.info("health check")
    return {"status": "ok"}
