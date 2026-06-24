class AnswerVerifier:
    """
    Lightweight answer verification utility.

    This sits below the VerificationAgent and focuses on simple,
    explainable checks:

    1. Answer exists
    2. Context exists
    3. Answer has citation support
    4. Confidence passes threshold
    """

    def __init__(self, minimum_confidence: float = 0.60):
        self.minimum_confidence = minimum_confidence

    def verify_answer(
        self,
        answer: str,
        context_used: str,
        citations: list[dict],
        confidence: float,
    ) -> dict:
        issues = []

        if not answer or not answer.strip():
            issues.append("empty_answer")

        if not context_used or not context_used.strip():
            issues.append("missing_context")

        if not citations:
            issues.append("missing_citations")

        if confidence < self.minimum_confidence:
            issues.append("low_confidence")

        verified = len(issues) == 0

        return {
            "verified": verified,
            "issues": issues,
            "confidence": confidence,
            "minimum_confidence": self.minimum_confidence,
            "status": "passed" if verified else "failed",
        }