from fastapi.testclient import TestClient

from app.api.routes.rag import pipeline
from app.main import app


client = TestClient(app)


def setup_function() -> None:
    pipeline.clear()


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_document_and_query_with_provider_and_backend() -> None:
    add = client.post(
        "/rag/documents",
        json={
            "document_id": "doc-1",
            "text": "Paris is the capital of France.",
            "metadata": {},
            "backends": ["memory"],
        },
    )
    assert add.status_code == 200
    assert add.json()["chunks_indexed"] >= 1

    query = client.post(
        "/rag/query",
        json={
            "query": "What is the capital of France?",
            "top_k": 1,
            "backends": ["memory"],
            "llm_provider": "extractive",
        },
    )
    assert query.status_code == 200
    payload = query.json()
    assert "Paris" in payload["answer"]
    assert len(payload["sources"]) == 1
    assert payload["sources"][0]["backend"] == "memory"
