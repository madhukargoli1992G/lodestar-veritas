from lodestar_veritas.retrieval.bm25_search import BM25Search
from lodestar_veritas.retrieval.dense_search import DenseSearch
from lodestar_veritas.retrieval.rrf import ReciprocalRankFusion
from lodestar_veritas.retrieval.reranker import SimpleReranker


class HybridSearch:
    """
    Hybrid retrieval pipeline:

    query
      -> dense search
      -> BM25 search
      -> RRF fusion
      -> reranking
    """

    def __init__(self):
        self.dense_search = DenseSearch()
        self.bm25_search = BM25Search()
        self.rrf = ReciprocalRankFusion()
        self.reranker = SimpleReranker()

    def add_documents(self, embedded_chunks: list[dict]) -> None:
        self.dense_search.add_documents(embedded_chunks)
        self.bm25_search.add_documents(embedded_chunks)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        dense_results = self.dense_search.search(query=query, top_k=top_k)
        bm25_results = self.bm25_search.search(query=query, top_k=top_k)

        fused_results = self.rrf.fuse(
            ranked_lists=[dense_results, bm25_results],
            top_k=top_k,
        )

        reranked_results = self.reranker.rerank(
            query=query,
            results=fused_results,
            top_k=top_k,
        )

        return reranked_results