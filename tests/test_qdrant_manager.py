from lodestar_veritas.vectorstore.qdrant_manager import QdrantManager


def test_qdrant_manager_adds_and_searches_chunks(tmp_path):
    store = QdrantManager(
        collection_name="test_lodestar_chunks",
        vector_size=3,
        path=str(tmp_path / "qdrant"),
    )

    store.clear()

    chunks = [
        {
            "chunk_id": "chunk_1",
            "text": "Revenue increased in 2024.",
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

    store.add(chunks)

    results = store.search(
        query_embedding=[1.0, 0.0, 0.0],
        top_k=1,
    )

    assert len(results) == 1
    assert results[0]["chunk_id"] == "chunk_1"
    assert results[0]["metadata"]["source"] == "sample.txt"