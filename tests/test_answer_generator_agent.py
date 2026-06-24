from lodestar_veritas.agents.answer_generator_agent import AnswerGeneratorAgent


def test_answer_generator_uses_retrieved_chunks():
    agent = AnswerGeneratorAgent(use_llm=False)

    retrieved_chunks = [
        {
            "chunk_id": "chunk_1",
            "text": "Revenue increased by 25% in 2024.",
            "metadata": {
                "source": "sample.txt",
                "file_name": "sample.txt",
                "parser": "TextParser",
                "chunk_number": 1,
            },
            "score": 0.95,
            "rerank_score": 3,
        }
    ]

    result = agent.generate(
        query="What increased in 2024?",
        retrieved_chunks=retrieved_chunks,
    )

    assert "Revenue increased" in result["answer"]
    assert result["citations"][0]["source"] == "sample.txt"
    assert result["citations"][0]["chunk"] == 1
    assert result["sources"][0]["chunk_id"] == "chunk_1"
    assert "[1]" in result["context_used"]