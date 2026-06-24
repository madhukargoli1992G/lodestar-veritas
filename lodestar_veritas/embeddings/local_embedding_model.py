import hashlib


class LocalEmbeddingModel:
    """
    Local placeholder embedding model.

    Right now this creates deterministic numeric vectors without downloading models.
    Later we will replace this with SentenceTransformer / Ollama embeddings.

    Why placeholder first?
    Because we want the pipeline structure to work before adding heavy ML dependencies.
    """

    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions

    def embed_text(self, text: str) -> list[float]:
        if not text:
            return [0.0] * self.dimensions

        vector = []

        for i in range(self.dimensions):
            seed = f"{text}-{i}".encode("utf-8")
            digest = hashlib.sha256(seed).hexdigest()
            value = int(digest[:8], 16) / 0xFFFFFFFF
            vector.append(value)

        return vector

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]