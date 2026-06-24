from pathlib import Path

from lodestar_veritas.agents.ingestion_agent import IngestionAgent


def test_ingestion_agent_creates_chunks_for_text_file(tmp_path: Path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("This is a sample text file. " * 200, encoding="utf-8")

    agent = IngestionAgent()
    result = agent.ingest(str(sample_file))

    assert result["analysis"].document_type == "plain_text"
    assert result["parsed_content"]["metadata"]["parser"] == "TextParser"
    assert result["chunk_count"] > 0
    assert len(result["chunks"]) == result["chunk_count"]
    assert result["chunks"][0].metadata["source"] == str(sample_file)