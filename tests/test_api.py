from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_document_and_query() -> None:
    add = client.post(
        "/rag/documents",
        json={"document_id": "doc-1", "text": "Paris is the capital of France.", "metadata": {}},
    )
    assert add.status_code == 200
    assert add.json()["chunks_indexed"] >= 1

    query = client.post("/rag/query", json={"query": "What is the capital of France?", "top_k": 1})
    assert query.status_code == 200
    payload = query.json()
    assert "answer" in payload
    assert len(payload["sources"]) == 1
