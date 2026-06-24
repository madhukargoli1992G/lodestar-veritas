from lodestar_veritas.verification.hallucination_checker import HallucinationChecker


def test_hallucination_checker_passes_supported_answer():
    checker = HallucinationChecker(minimum_confidence=0.60)

    result = checker.check(
        answer="Revenue increased by 25% in 2024.",
        context_used="[1] Revenue increased by 25% in 2024.",
        citations=[{"source": "sample.txt", "chunk": 1}],
        confidence=0.95,
    )

    assert result["hallucination_risk"] is False
    assert result["risks"] == []


def test_hallucination_checker_flags_answer_without_context():
    checker = HallucinationChecker(minimum_confidence=0.60)

    result = checker.check(
        answer="Revenue increased by 25% in 2024.",
        context_used="",
        citations=[{"source": "sample.txt", "chunk": 1}],
        confidence=0.95,
    )

    assert result["hallucination_risk"] is True
    assert "answer_without_context" in result["risks"]


def test_hallucination_checker_flags_answer_without_citations():
    checker = HallucinationChecker(minimum_confidence=0.60)

    result = checker.check(
        answer="Revenue increased by 25% in 2024.",
        context_used="[1] Revenue increased by 25% in 2024.",
        citations=[],
        confidence=0.95,
    )

    assert result["hallucination_risk"] is True
    assert "answer_without_citations" in result["risks"]