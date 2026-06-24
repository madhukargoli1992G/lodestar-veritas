from lodestar_veritas.retrieval.qdrant_dense_search import QdrantDenseSearch


def test_qdrant_dense_search_returns_results(tmp_path, monkeypatch):
    search = QdrantDenseSearch()

    search.qdrant.client.close()
    from lodestar_veritas.vectorstore.qdrant_manager import QdrantManager

    search.qdrant = QdrantManager(
        collection_name="test_qdrant_dense_search",
        vector_size=384,
        path=str(tmp_path / "qdrant"),
    )
    search.qdrant.clear()

    embedded_chunks = [
        {
            "chunk_id": "chunk_1",
            "text": "Revenue increased by 25% in 2024.",
            "metadata": {"source": "sample.txt"},
            "embedding": [1.0] + [0.0] * 383,
        }
    ]

    search.add_documents(embedded_chunks)

    results = search.search(
        query="What happened to revenue?",
        top_k=1,
    )

    assert len(results) == 1
    assert "text" in results[0]
    assert results[0]["retrieval_method"] == "qdrant_dense"