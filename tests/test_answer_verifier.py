from lodestar_veritas.verification.answer_verifier import AnswerVerifier


def test_answer_verifier_passes_valid_answer():
    verifier = AnswerVerifier(minimum_confidence=0.60)

    result = verifier.verify_answer(
        answer="Revenue increased by 25% in 2024.",
        context_used="[1] Revenue increased by 25% in 2024.",
        citations=[{"source": "sample.txt", "chunk": 1}],
        confidence=0.95,
    )

    assert result["verified"] is True
    assert result["status"] == "passed"
    assert result["issues"] == []


def test_answer_verifier_fails_without_context():
    verifier = AnswerVerifier(minimum_confidence=0.60)

    result = verifier.verify_answer(
        answer="Revenue increased by 25% in 2024.",
        context_used="",
        citations=[{"source": "sample.txt", "chunk": 1}],
        confidence=0.95,
    )

    assert result["verified"] is False
    assert "missing_context" in result["issues"]


def test_answer_verifier_fails_low_confidence():
    verifier = AnswerVerifier(minimum_confidence=0.80)

    result = verifier.verify_answer(
        answer="Revenue increased by 25% in 2024.",
        context_used="[1] Revenue increased by 25% in 2024.",
        citations=[{"source": "sample.txt", "chunk": 1}],
        confidence=0.40,
    )

    assert result["verified"] is False
    assert "low_confidence" in result["issues"]