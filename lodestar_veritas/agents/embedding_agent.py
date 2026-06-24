from lodestar_veritas.embeddings.local_embedding_model import LocalEmbeddingModel


class EmbeddingAgent:
    """
    Converts document chunks into embeddings.
    """

    def __init__(self, dimensions: int = 384):
        self.embedding_model = LocalEmbeddingModel(dimensions=dimensions)

    def embed_chunks(self, chunks: list) -> list[dict]:
        embedded_chunks = []

        for chunk in chunks:
            vector = self.embedding_model.embed_text(chunk.text)

            embedded_chunks.append(
                {
                    "chunk_id": chunk.chunk_id,
                    "text": chunk.text,
                    "metadata": chunk.metadata,
                    "embedding": vector,
                }
            )

        return embedded_chunks