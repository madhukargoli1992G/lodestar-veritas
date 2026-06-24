class HallucinationChecker:
    """
    Simple hallucination-risk checker.

    This does not prove hallucination perfectly.
    It flags risk when the answer is present but support is weak.

    Checks:
    1. Answer exists but context is missing
    2. Answer exists but citations are missing
    3. Answer confidence is below threshold
    """

    def __init__(self, minimum_confidence: float = 0.60):
        self.minimum_confidence = minimum_confidence

    def check(
        self,
        answer: str,
        context_used: str,
        citations: list[dict],
        confidence: float,
    ) -> dict:
        risks = []

        has_answer = bool(answer and answer.strip())
        has_context = bool(context_used and context_used.strip())
        has_citations = bool(citations)

        if has_answer and not has_context:
            risks.append("answer_without_context")

        if has_answer and not has_citations:
            risks.append("answer_without_citations")

        if confidence < self.minimum_confidence:
            risks.append("low_confidence_answer")

        hallucination_risk = len(risks) > 0

        return {
            "hallucination_risk": hallucination_risk,
            "risks": risks,
            "confidence": confidence,
            "minimum_confidence": self.minimum_confidence,
        }