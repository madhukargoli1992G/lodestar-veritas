class QueryRouter:
    """
    Decides which retrieval strategy to use.

    For now:
    - numbers, dates, exact terms -> hybrid
    - normal questions -> hybrid

    Later:
    - exact search -> BM25
    - semantic question -> dense
    - complex question -> hybrid + rerank
    """

    def route(self, query: str) -> str:
        query_lower = query.lower()

        exact_keywords = [
            "revenue",
            "risk",
            "date",
            "year",
            "percentage",
            "amount",
            "usd",
            "$",
            "%",
        ]

        if any(keyword in query_lower for keyword in exact_keywords):
            return "hybrid"

        return "hybrid"