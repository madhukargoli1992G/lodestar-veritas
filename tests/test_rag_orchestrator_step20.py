from lodestar_veritas.agents.rag_orchestrator_agent import RAGOrchestratorAgent


def test_rag_orchestrator_ingests_retrieves_and_answers(tmp_path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text(
        "Revenue increased by 25% in 2024 due to subscription growth. "
        "Risk factors include inflation and market volatility. "
        * 100,
        encoding="utf-8",
    )

    agent = RAGOrchestratorAgent()

    ingestion_result = agent.ingest_file(str(sample_file))

    assert ingestion_result["chunk_count"] > 0
    assert ingestion_result["embedded_chunk_count"] == ingestion_result["chunk_count"]

    answer_result = agent.ask(
        query="What increased in 2024?",
        top_k=2,
    )

    assert answer_result["query"] == "What increased in 2024?"
    assert answer_result["retrieved_count"] > 0
    assert answer_result["retrieved_count"] <= 2
    assert "answer" in answer_result
    assert "sources" in answer_result
    assert len(answer_result["sources"]) > 0