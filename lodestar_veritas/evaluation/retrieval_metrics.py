class RetrievalMetrics:
    """
    Evaluation metrics for retrieval quality.
    """

    def reciprocal_rank(self, retrieved_ids: list[str], relevant_ids: set[str]) -> float:
        for rank, chunk_id in enumerate(retrieved_ids, start=1):
            if chunk_id in relevant_ids:
                return 1 / rank

        return 0.0

    def recall_at_k(
        self,
        retrieved_ids: list[str],
        relevant_ids: set[str],
        k: int,
    ) -> float:
        if not relevant_ids:
            return 0.0

        retrieved_at_k = set(retrieved_ids[:k])
        matches = retrieved_at_k.intersection(relevant_ids)

        return len(matches) / len(relevant_ids)
    