class ContextEvaluatorAgent:
    """
    Evaluates whether retrieved context is sufficient for answer generation.

    This helps the graph decide whether to:
    1. Continue to answer generation
    2. Rewrite the query and retrieve again
    """

    def __init__(self, minimum_chunks: int = 1, minimum_score: float = 0.50):
        self.minimum_chunks = minimum_chunks
        self.minimum_score = minimum_score

    def evaluate(self, retrieved_chunks: list[dict]) -> dict:
        if not retrieved_chunks:
            return {
                "context_sufficient": False,
                "reason": "no_chunks_retrieved",
                "retrieved_count": 0,
                "average_score": 0.0,
            }

        scores = []

        for chunk in retrieved_chunks:
            score = chunk.get("score")

            if isinstance(score, (int, float)):
                scores.append(float(score))

        average_score = sum(scores) / len(scores) if scores else 0.75

        context_sufficient = (
            len(retrieved_chunks) >= self.minimum_chunks
            and average_score >= self.minimum_score
        )

        return {
            "context_sufficient": context_sufficient,
            "reason": "sufficient_context"
            if context_sufficient
            else "insufficient_context",
            "retrieved_count": len(retrieved_chunks),
            "average_score": round(average_score, 2),
        }