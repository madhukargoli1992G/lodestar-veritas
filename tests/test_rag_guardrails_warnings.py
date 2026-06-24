from lodestar_veritas.guardrails.rag_guardrails import RAGGuardrails


def test_guardrails_warn_when_verification_fails():
    guardrails = RAGGuardrails()

    rag_result = {
        "answer": "Revenue increased by 25% in 2024.",
        "citations": [{"source": "sample.txt", "chunk": 1}],
        "verification": {
            "verified": False,
            "hallucination_check": {
                "hallucination_risk": False,
            },
        },
    }

    result = guardrails.apply(rag_result)

    assert result["safe_to_return"] is True
    assert result["blocked"] is False
    assert "verification_failed" in result["warnings"]


def test_guardrails_warn_when_hallucination_risk_exists():
    guardrails = RAGGuardrails()

    rag_result = {
        "answer": "Revenue increased by 25% in 2024.",
        "citations": [{"source": "sample.txt", "chunk": 1}],
        "verification": {
            "verified": False,
            "hallucination_check": {
                "hallucination_risk": True,
            },
        },
    }

    result = guardrails.apply(rag_result)

    assert result["safe_to_return"] is True
    assert "hallucination_risk" in result["warnings"]
    assert "verification_failed" in result["warnings"]