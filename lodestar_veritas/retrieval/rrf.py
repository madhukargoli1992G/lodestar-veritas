class ReciprocalRankFusion:
    """
    Combines ranked results from multiple retrievers.

    Formula:
        score = 1 / (k + rank)
    """

    def __init__(self, k: int = 60):
        self.k = k

    def fuse(self, ranked_lists: list[list[dict]], top_k: int = 5) -> list[dict]:
        fused_scores = {}
        fused_items = {}

        for ranked_list in ranked_lists:
            for rank, item in enumerate(ranked_list, start=1):
                chunk_id = item["chunk_id"]

                if chunk_id not in fused_scores:
                    fused_scores[chunk_id] = 0.0
                    fused_items[chunk_id] = item

                fused_scores[chunk_id] += 1 / (self.k + rank)

        fused_results = []

        for chunk_id, item in fused_items.items():
            fused_results.append(
                {
                    **item,
                    "score": fused_scores[chunk_id],
                    "retrieval_method": "hybrid_rrf",
                }
            )

        fused_results.sort(key=lambda item: item["score"], reverse=True)
        return fused_results[:top_k]