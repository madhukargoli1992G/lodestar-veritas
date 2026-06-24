import math


class InMemoryVectorStore:
    """
    Simple in-memory vector store.

    Stores embedded chunks and retrieves similar chunks using cosine similarity.
    Later we can replace this with Qdrant, Redis, or FAISS.
    """

    def __init__(self):
        self.items = []

    def add(self, embedded_chunks: list[dict]) -> None:
        self.items.extend(embedded_chunks)

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        scored_items = []

        for item in self.items:
            score = self._cosine_similarity(query_embedding, item["embedding"])
            scored_items.append(
                {
                    **item,
                    "score": score,
                }
            )

        scored_items.sort(key=lambda item: item["score"], reverse=True)

        return scored_items[:top_k]

    def count(self) -> int:
        return len(self.items)

    def _cosine_similarity(
        self,
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        norm_a = math.sqrt(sum(a * a for a in vector_a))
        norm_b = math.sqrt(sum(b * b for b in vector_b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)