class QueryRewriteAgent:
    """
    Rewrites user queries for better retrieval.

    This is intentionally lightweight for local/offline use.
    Later, this can be upgraded to use Ollama or another LLM.
    """

    def rewrite(self, query: str, retry_count: int = 0) -> str:
        cleaned_query = query.strip()

        if not cleaned_query:
            return ""

        if retry_count <= 0:
            return cleaned_query

        return (
            f"{cleaned_query} "
            f"Use related financial, regulatory, table, and summary context."
        )