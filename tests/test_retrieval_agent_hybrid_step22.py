from pathlib import Path

from lodestar_veritas.agents.ingestion_agent import IngestionAgent
from lodestar_veritas.agents.retrieval_agent import RetrievalAgent


def test_retrieval_agent_uses_hybrid_search(tmp_path: Path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text(
        "Revenue increased by 25% in 2024 because of subscription growth. "
        "Risk factors include inflation, currency pressure, and market volatility. "
        "Operating margin improved due to cost optimization. "
        * 100,
        encoding="utf-8",
    )

    ingestion_agent = IngestionAgent()
    ingestion_result = ingestion_agent.ingest(str(sample_file))

    retrieval_agent = RetrievalAgent()
    retrieval_agent.add_documents(ingestion_result["embedded_chunks"])

    results = retrieval_agent.retrieve(
        query="What happened to revenue in 2024?",
        top_k=3,
    )

    assert len(results) > 0
    assert len(results) <= 3
    assert results[0]["retrieval_method"] == "hybrid_rrf"
    assert "rerank_score" in results[0]