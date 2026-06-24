from lodestar_veritas.retrieval.hybrid_search import HybridSearch
from lodestar_veritas.retrieval.query_router import QueryRouter


class RetrievalAgent:
    """
    Retrieval agent with query routing.

    Current strategies:
    - hybrid: dense + BM25 + RRF + rerank

    Later:
    - dense only
    - BM25 only
    - metadata filter
    - multi-query retrieval
    """

    def __init__(self):
        self.query_router = QueryRouter()
        self.hybrid_search = HybridSearch()

    def add_documents(self, embedded_chunks: list[dict]) -> None:
        self.hybrid_search.add_documents(embedded_chunks)

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        route = self.query_router.route(query)

        if route == "hybrid":
            return self.hybrid_search.search(query=query, top_k=top_k)

        return self.hybrid_search.search(query=query, top_k=top_k)