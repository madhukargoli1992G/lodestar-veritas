from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class QdrantManager:
    """
    Local Qdrant vector store manager.

    Uses embedded local storage by default.
    No Docker needed.
    """

    def __init__(
        self,
        collection_name: str = "lodestar_veritas_chunks",
        vector_size: int = 384,
        path: str = ".qdrant",
    ):
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.client = QdrantClient(path=path)

        self._ensure_collection()

    def _ensure_collection(self) -> None:
        existing_collections = [
            collection.name
            for collection in self.client.get_collections().collections
        ]

        if self.collection_name not in existing_collections:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def add(self, embedded_chunks: list[dict]) -> None:
        points = []

        for index, chunk in enumerate(embedded_chunks):
            points.append(
                PointStruct(
                    id=index + 1,
                    vector=chunk["embedding"],
                    payload={
                        "chunk_id": chunk["chunk_id"],
                        "text": chunk["text"],
                        "metadata": chunk.get("metadata", {}),
                    },
                )
            )

        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
        )

        results = []

        for result in search_results:
            payload = result.payload or {}

            results.append(
                {
                    "chunk_id": payload.get("chunk_id"),
                    "text": payload.get("text"),
                    "metadata": payload.get("metadata", {}),
                    "score": result.score,
                }
            )

        return results

    def clear(self) -> None:
        self.client.delete_collection(self.collection_name)
        self._ensure_collection()