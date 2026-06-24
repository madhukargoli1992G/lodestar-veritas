from lodestar_veritas.embeddings.local_embedding_model import LocalEmbeddingModel


def test_local_embedding_model_returns_vector():
    model = LocalEmbeddingModel(dimensions=384)

    vector = model.embed_text("financial risk disclosure")

    assert isinstance(vector, list)
    assert len(vector) == 384
    assert all(isinstance(value, float) for value in vector)


def test_local_embedding_model_is_deterministic():
    model = LocalEmbeddingModel(dimensions=384)

    vector_1 = model.embed_text("same text")
    vector_2 = model.embed_text("same text")

    assert vector_1 == vector_2