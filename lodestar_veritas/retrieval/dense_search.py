from lodestar_veritas.embeddings.local_embedding_model import LocalEmbeddingModel
from lodestar_veritas.vectorstore.in_memory_vector_store import InMemoryVectorStore


class DenseSearch:
    def __init__(self):
        self.embedding_model = LocalEmbeddingModel(dimensions=384)
        self.vector_store = InMemoryVectorStore()

    def add_documents(self, embedded_chunks: list[dict]) -> None:
        self.vector_store.add(embedded_chunks)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        query_embedding = self.embedding_model.embed_text(query)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return [
            {
                **result,
                "retrieval_method": "dense",
            }
            for result in results
        ]