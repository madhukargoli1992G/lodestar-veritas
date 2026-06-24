from lodestar_veritas.agents.verification_agent import VerificationAgent


def test_verification_agent_passes_grounded_answer():
    agent = VerificationAgent(minimum_confidence=0.60)

    generated_result = {
        "answer": "Revenue increased by 25% in 2024.",
        "context_used": "[1] Revenue increased by 25% in 2024.",
        "citations": [{"source": "sample.txt", "chunk": 1}],
        "confidence": 0.95,
        "grounded": True,
    }

    result = agent.verify(generated_result)

    assert result["verified"] is True
    assert result["status"] == "passed"
    assert result["issues"] == []


def test_verification_agent_fails_without_citations():
    agent = VerificationAgent(minimum_confidence=0.60)

    generated_result = {
        "answer": "Revenue increased by 25% in 2024.",
        "context_used": "[1] Revenue increased by 25% in 2024.",
        "citations": [],
        "confidence": 0.95,
        "grounded": True,
    }

    result = agent.verify(generated_result)

    assert result["verified"] is False
    assert result["status"] == "failed"
    assert "missing_citations" in result["issues"]


def test_verification_agent_fails_low_confidence():
    agent = VerificationAgent(minimum_confidence=0.80)

    generated_result = {
        "answer": "Revenue increased by 25% in 2024.",
        "context_used": "[1] Revenue increased by 25% in 2024.",
        "citations": [{"source": "sample.txt", "chunk": 1}],
        "confidence": 0.40,
        "grounded": True,
    }

    result = agent.verify(generated_result)

    assert result["verified"] is False
    assert "low_confidence" in result["issues"]