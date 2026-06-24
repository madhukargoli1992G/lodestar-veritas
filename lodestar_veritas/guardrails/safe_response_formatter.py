class SafeResponseFormatter:
    """
    Formats the final RAG response after guardrails.

    If the answer is blocked, it returns a safe fallback message.
    If the answer is safe, it returns the original answer with metadata.
    """

    def format(self, rag_result: dict) -> dict:
        guardrails = rag_result.get("guardrails", {})
        safe_to_return = guardrails.get("safe_to_return", False)

        if not safe_to_return:
            return {
                "answer": "I could not generate a safe, grounded answer from the provided documents.",
                "safe_to_return": False,
                "warnings": guardrails.get("warnings", []),
                "citations": [],
                "sources": [],
            }

        return {
            "answer": rag_result.get("answer", ""),
            "safe_to_return": True,
            "warnings": guardrails.get("warnings", []),
            "citations": rag_result.get("citations", []),
            "sources": rag_result.get("sources", []),
            "confidence": rag_result.get("confidence", 0.0),
            "verified": rag_result.get("verified", False),
            "is_grounded": rag_result.get("is_grounded", False),
        }