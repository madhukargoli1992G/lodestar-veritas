from lodestar_veritas.agents.context_evaluator_agent import ContextEvaluatorAgent


def test_context_evaluator_fails_when_no_chunks():
    agent = ContextEvaluatorAgent()

    result = agent.evaluate([])

    assert result["context_sufficient"] is False
    assert result["reason"] == "no_chunks_retrieved"
    assert result["retrieved_count"] == 0


def test_context_evaluator_passes_with_good_chunks():
    agent = ContextEvaluatorAgent(minimum_chunks=1, minimum_score=0.50)

    chunks = [
        {
            "text": "Revenue increased by 25% in 2024.",
            "score": 0.95,
        }
    ]

    result = agent.evaluate(chunks)

    assert result["context_sufficient"] is True
    assert result["reason"] == "sufficient_context"


def test_context_evaluator_fails_with_low_score():
    agent = ContextEvaluatorAgent(minimum_chunks=1, minimum_score=0.80)

    chunks = [
        {
            "text": "Weakly related context.",
            "score": 0.30,
        }
    ]

    result = agent.evaluate(chunks)

    assert result["context_sufficient"] is False
    assert result["reason"] == "insufficient_context"