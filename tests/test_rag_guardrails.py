from lodestar_veritas.guardrails.rag_guardrails import RAGGuardrails


def test_guardrails_pass_valid_rag_result():
    guardrails = RAGGuardrails()

    rag_result = {
        "answer": "Revenue increased by 25% in 2024.",
        "citations": [{"source": "sample.txt", "chunk": 1}],
        "verification": {
            "verified": True,
            "hallucination_check": {
                "hallucination_risk": False,
            },
        },
    }

    result = guardrails.apply(rag_result)

    assert result["safe_to_return"] is True
    assert result["blocked"] is False
    assert result["warnings"] == []


def test_guardrails_warn_missing_citations():
    guardrails = RAGGuardrails()

    rag_result = {
        "answer": "Revenue increased by 25% in 2024.",
        "citations": [],
        "verification": {
            "verified": True,
            "hallucination_check": {
                "hallucination_risk": False,
            },
        },
    }

    result = guardrails.apply(rag_result)

    assert result["safe_to_return"] is True
    assert "missing_citations" in result["warnings"]


def test_guardrails_block_empty_answer():
    guardrails = RAGGuardrails()

    rag_result = {
        "answer": "",
        "citations": [],
        "verification": {
            "verified": False,
            "hallucination_check": {
                "hallucination_risk": True,
            },
        },
    }

    result = guardrails.apply(rag_result)

    assert result["safe_to_return"] is False
    assert result["blocked"] is True
    assert "empty_answer" in result["warnings"]