from lodestar_veritas.chunking.recursive_chunker import RecursiveChunker


def test_recursive_chunker_creates_chunks():
    chunker = RecursiveChunker()

    text = "A" * 1500

    chunks = chunker.chunk(
        text=text,
        chunk_size=500,
        chunk_overlap=100,
        metadata={"source": "test.txt"},
    )

    assert len(chunks) > 1
    assert chunks[0].text == "A" * 500
    assert chunks[0].metadata["source"] == "test.txt"
    assert chunks[0].metadata["chunk_number"] == 1