from lodestar_veritas.embeddings.local_embedding_model import LocalEmbeddingModel
from lodestar_veritas.vectorstore.qdrant_manager import QdrantManager


class QdrantDenseSearch:
    """
    Dense semantic search using Qdrant.
    """

    def __init__(self):
        self.embedding_model = LocalEmbeddingModel(dimensions=384)
        self.qdrant = QdrantManager(vector_size=384)

    def add_documents(self, embedded_chunks: list[dict]) -> None:
        self.qdrant.add(embedded_chunks)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        query_embedding = self.embedding_model.embed_text(query)

        results = self.qdrant.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return [
            {
                **result,
                "retrieval_method": "qdrant_dense",
            }
            for result in results
        ]

    def clear(self) -> None:
        self.qdrant.clear()