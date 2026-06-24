from pathlib import Path

from lodestar_veritas.agents.ingestion_agent import IngestionAgent


def test_ingestion_agent_embeds_text_chunks(tmp_path: Path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("Financial risk disclosure and revenue analysis. " * 200, encoding="utf-8")

    agent = IngestionAgent()
    result = agent.ingest(str(sample_file))

    assert result["chunk_count"] > 0
    assert result["embedded_chunk_count"] == result["chunk_count"]

    first_embedded_chunk = result["embedded_chunks"][0]

    assert "chunk_id" in first_embedded_chunk
    assert "text" in first_embedded_chunk
    assert "metadata" in first_embedded_chunk
    assert "embedding" in first_embedded_chunk
    assert len(first_embedded_chunk["embedding"]) == 384