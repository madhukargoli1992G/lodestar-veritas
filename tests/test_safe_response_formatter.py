from lodestar_veritas.guardrails.safe_response_formatter import SafeResponseFormatter


def test_safe_response_formatter_returns_safe_answer():
    formatter = SafeResponseFormatter()

    rag_result = {
        "answer": "Revenue increased by 25% in 2024.",
        "citations": [{"source": "sample.txt", "chunk": 1}],
        "sources": [{"source": "sample.txt"}],
        "confidence": 0.95,
        "verified": True,
        "is_grounded": True,
        "guardrails": {
            "safe_to_return": True,
            "warnings": [],
        },
    }

    result = formatter.format(rag_result)

    assert result["answer"] == "Revenue increased by 25% in 2024."
    assert result["safe_to_return"] is True
    assert result["warnings"] == []
    assert result["verified"] is True


def test_safe_response_formatter_blocks_unsafe_answer():
    formatter = SafeResponseFormatter()

    rag_result = {
        "answer": "",
        "citations": [],
        "sources": [],
        "guardrails": {
            "safe_to_return": False,
            "warnings": ["empty_answer"],
        },
    }

    result = formatter.format(rag_result)

    assert result["safe_to_return"] is False
    assert "safe, grounded answer" in result["answer"]
    assert result["citations"] == []