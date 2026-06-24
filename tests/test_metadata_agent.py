from lodestar_veritas.agents.metadata_agent import MetadataAgent
from lodestar_veritas.chunking.chunk_models import DocumentChunk


def test_metadata_agent_enriches_chunk_metadata():
    chunk = DocumentChunk(
        chunk_id="chunk_1",
        text="Revenue increased by 25% in 2024 with USD growth.",
        metadata={"source": "sample.txt"},
    )

    agent = MetadataAgent()
    enriched_chunks = agent.enrich_chunks([chunk])

    enriched = enriched_chunks[0]

    assert enriched.chunk_id == "chunk_1"
    assert enriched.metadata["source"] == "sample.txt"
    assert enriched.metadata["contains_numbers"] is True
    assert enriched.metadata["contains_dates"] is True
    assert enriched.metadata["contains_currency"] is True
    assert enriched.metadata["contains_percentage"] is True
    assert enriched.metadata["word_count"] > 0