class SimpleReranker:
    """
    Lightweight placeholder reranker.

    Later this can be replaced with a CrossEncoder reranker.
    """

    def rerank(self, query: str, results: list[dict], top_k: int = 5) -> list[dict]:
        query_terms = set(query.lower().split())
        reranked = []

        for result in results:
            text_terms = set(result["text"].lower().split())
            overlap = len(query_terms.intersection(text_terms))

            reranked.append(
                {
                    **result,
                    "rerank_score": overlap,
                }
            )

        reranked.sort(
            key=lambda item: (item["rerank_score"], item["score"]),
            reverse=True,
        )

        return reranked[:top_k]