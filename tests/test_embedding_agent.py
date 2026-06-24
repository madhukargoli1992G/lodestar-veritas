from lodestar_veritas.agents.embedding_agent import EmbeddingAgent
from lodestar_veritas.chunking.chunk_models import DocumentChunk


def test_embedding_agent_embeds_chunks():
    chunks = [
        DocumentChunk(
            chunk_id="chunk_1",
            text="Revenue increased due to stronger subscription growth.",
            metadata={"source": "sample.txt"},
        )
    ]

    agent = EmbeddingAgent(dimensions=384)
    embedded_chunks = agent.embed_chunks(chunks)

    assert len(embedded_chunks) == 1
    assert embedded_chunks[0]["chunk_id"] == "chunk_1"
    assert embedded_chunks[0]["text"] == chunks[0].text
    assert embedded_chunks[0]["metadata"]["source"] == "sample.txt"
    assert len(embedded_chunks[0]["embedding"]) == 384