from app.rag.pipeline import RagPipeline


def test_pipeline_ingest_and_query() -> None:
    pipeline = RagPipeline()
    pipeline.store.clear()

    n = pipeline.ingest("doc-1", "FastAPI is a modern Python web framework for APIs.")
    assert n >= 1

    answer, hits = pipeline.query("What is FastAPI?", top_k=1)
    assert "FastAPI" in answer
    assert len(hits) == 1
