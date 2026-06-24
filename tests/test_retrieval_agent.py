from lodestar_veritas.agents.ingestion_agent import IngestionAgent
from lodestar_veritas.agents.retrieval_agent import RetrievalAgent


def test_retrieval_agent_retrieves_chunks(tmp_path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text(
        "Revenue increased by 25% in 2024. "
        "Risk factors include inflation and market volatility. "
        * 100,
        encoding="utf-8",
    )

    ingestion_agent = IngestionAgent()
    ingestion_result = ingestion_agent.ingest(str(sample_file))

    retrieval_agent = RetrievalAgent()
    retrieval_agent.add_documents(ingestion_result["embedded_chunks"])

    results = retrieval_agent.retrieve(
        query="What increased in 2024?",
        top_k=2,
    )

    assert len(results) > 0
    assert len(results) <= 2
    assert "text" in results[0]
    assert "score" in results[0]
    assert "metadata" in results[0]