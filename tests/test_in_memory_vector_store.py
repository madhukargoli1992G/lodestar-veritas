from lodestar_veritas.vectorstore.in_memory_vector_store import InMemoryVectorStore


def test_in_memory_vector_store_adds_items():
    store = InMemoryVectorStore()

    embedded_chunks = [
        {
            "chunk_id": "chunk_1",
            "text": "Revenue increased this quarter.",
            "metadata": {"source": "sample.txt"},
            "embedding": [1.0, 0.0, 0.0],
        },
        {
            "chunk_id": "chunk_2",
            "text": "Risk factors include inflation.",
            "metadata": {"source": "sample.txt"},
            "embedding": [0.0, 1.0, 0.0],
        },
    ]

    store.add(embedded_chunks)

    assert store.count() == 2


def test_in_memory_vector_store_search_returns_top_k():
    store = InMemoryVectorStore()

    embedded_chunks = [
        {
            "chunk_id": "chunk_1",
            "text": "Revenue increased this quarter.",
            "metadata": {"source": "sample.txt"},
            "embedding": [1.0, 0.0, 0.0],
        },
        {
            "chunk_id": "chunk_2",
            "text": "Risk factors include inflation.",
            "metadata": {"source": "sample.txt"},
            "embedding": [0.0, 1.0, 0.0],
        },
    ]

    store.add(embedded_chunks)

    results = store.search(query_embedding=[1.0, 0.0, 0.0], top_k=1)

    assert len(results) == 1
    assert results[0]["chunk_id"] == "chunk_1"
    assert results[0]["score"] > 0