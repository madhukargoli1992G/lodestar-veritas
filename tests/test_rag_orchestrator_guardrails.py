from lodestar_veritas.agents.rag_orchestrator_agent import RAGOrchestratorAgent


def test_rag_orchestrator_returns_guardrails():
    agent = RAGOrchestratorAgent()

    sample_chunks = [
        {
            "chunk_id": "chunk_1",
            "text": "Revenue increased by 25% in 2024.",
            "metadata": {
                "source": "sample.txt",
                "file_name": "sample.txt",
                "chunk_number": 1,
            },
            "embedding": [0.1, 0.2, 0.3],
            "score": 0.95,
        }
    ]

    agent.retrieval_agent.add_documents(sample_chunks)

    result = agent.ask(
        query="What increased in 2024?",
        top_k=1,
    )

    assert "guardrails" in result
    assert "safe_to_return" in result
    assert result["guardrails"]["safe_to_return"] is True
    assert result["safe_to_return"] is True