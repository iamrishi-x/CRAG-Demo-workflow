from app.rag.pipeline import RagPipeline


def test_pipeline_ingest_and_query_multi_backend() -> None:
    pipeline = RagPipeline()
    pipeline.clear()

    n = pipeline.ingest("doc-1", "FastAPI is a modern Python web framework for APIs.")
    assert n >= 1

    answer, hits = pipeline.query("What is FastAPI?", top_k=2)
    assert "FastAPI" in answer
    assert len(hits) >= 1
    assert all(hit[0].backend for hit in hits)


def test_pipeline_llm_provider_override() -> None:
    pipeline = RagPipeline()
    pipeline.clear()
    pipeline.ingest("doc-2", "Paris is the capital of France.")

    answer, _ = pipeline.query("Capital of France?", top_k=1, llm_provider="extractive")
    assert "Paris" in answer
