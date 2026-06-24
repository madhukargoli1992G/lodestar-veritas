class RAGGuardrails:
    """
    Guardrails for the RAG pipeline.

    These checks prevent unsafe or low-quality responses from being returned
    as if they are fully verified.

    Current checks:
    1. Empty answer
    2. Missing citations
    3. Hallucination risk
    4. Failed verification
    """

    def apply(self, rag_result: dict) -> dict:
        answer = rag_result.get("answer", "")
        citations = rag_result.get("citations", [])
        verification = rag_result.get("verification", {})

        hallucination_check = verification.get("hallucination_check", {})
        hallucination_risk = hallucination_check.get(
            "hallucination_risk",
            False,
        )

        blocked = False
        warnings = []

        if not answer or not answer.strip():
            blocked = True
            warnings.append("empty_answer")

        if not citations:
            warnings.append("missing_citations")

        if hallucination_risk:
            warnings.append("hallucination_risk")

        if verification and not verification.get("verified", False):
            warnings.append("verification_failed")

        safe_to_return = not blocked

        return {
            "safe_to_return": safe_to_return,
            "blocked": blocked,
            "warnings": warnings,
        }