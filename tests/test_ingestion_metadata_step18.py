from pathlib import Path

from lodestar_veritas.agents.ingestion_agent import IngestionAgent


def test_ingestion_agent_enriches_metadata_before_embedding(tmp_path: Path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text(
        "Revenue increased by 25% in 2024 with USD growth. " * 150,
        encoding="utf-8",
    )

    agent = IngestionAgent()
    result = agent.ingest(str(sample_file))

    assert result["chunk_count"] > 0
    assert result["embedded_chunk_count"] == result["chunk_count"]

    first_chunk = result["chunks"][0]
    first_embedded_chunk = result["embedded_chunks"][0]

    assert first_chunk.metadata["contains_numbers"] is True
    assert first_chunk.metadata["contains_dates"] is True
    assert first_chunk.metadata["contains_currency"] is True
    assert first_chunk.metadata["contains_percentage"] is True

    assert first_embedded_chunk["metadata"]["contains_numbers"] is True
    assert first_embedded_chunk["metadata"]["contains_dates"] is True
    assert first_embedded_chunk["metadata"]["contains_currency"] is True
    assert first_embedded_chunk["metadata"]["contains_percentage"] is True