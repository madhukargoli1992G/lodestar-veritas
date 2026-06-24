class BasicGuardrails:
    """
    Basic query safety and scope guardrails.
    """

    def validate_query(self, query: str) -> dict:
        if not query or not query.strip():
            return {
                "allowed": False,
                "reason": "Query is empty.",
            }

        blocked_terms = [
            "ignore previous instructions",
            "system prompt",
            "developer message",
        ]

        query_lower = query.lower()

        for term in blocked_terms:
            if term in query_lower:
                return {
                    "allowed": False,
                    "reason": "Query appears to request hidden system instructions.",
                }

        return {
            "allowed": True,
            "reason": "Query passed guardrails.",
        }