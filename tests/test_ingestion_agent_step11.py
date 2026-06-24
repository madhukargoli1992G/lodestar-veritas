from lodestar_veritas.agents.ingestion_agent import IngestionAgent


def test_ingestion_agent_for_pdf_placeholder():
    agent = IngestionAgent()

    result = agent.ingest("sample_report.unknown")

    assert "analysis" in result
    assert "chunk_strategy" in result
    assert "parsed_content" in result
    assert "chunks" in result
    assert "chunk_count" in result

    assert result["analysis"].document_type == "unknown"
    assert result["chunk_count"] == 0