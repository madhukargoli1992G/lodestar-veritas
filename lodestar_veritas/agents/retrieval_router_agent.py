class RetrievalRouterAgent:
    """
    Routes a query to the best retrieval strategy.

    This is lightweight and explainable:
    - keyword: exact terms, IDs, names, dates
    - semantic: broad meaning-based questions
    - hybrid: default for most enterprise RAG queries
    - metadata: source/page/file-specific questions
    """

    def route(self, query: str) -> dict:
        cleaned_query = query.strip().lower()

        if not cleaned_query:
            return {
                "strategy": "hybrid",
                "reason": "empty_query_default_hybrid",
            }

        metadata_terms = ["page", "file", "source", "document", "section"]
        keyword_terms = ["id", "exact", "quote", "date", "number", "amount"]
        semantic_terms = ["summarize", "explain", "compare", "why", "how"]

        if any(term in cleaned_query for term in metadata_terms):
            return {
                "strategy": "metadata",
                "reason": "metadata_terms_detected",
            }

        if any(term in cleaned_query for term in keyword_terms):
            return {
                "strategy": "keyword",
                "reason": "keyword_terms_detected",
            }

        if any(term in cleaned_query for term in semantic_terms):
            return {
                "strategy": "semantic",
                "reason": "semantic_terms_detected",
            }

        return {
            "strategy": "hybrid",
            "reason": "default_enterprise_rag_strategy",
        }