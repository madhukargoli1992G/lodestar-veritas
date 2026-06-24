from pathlib import Path

import fitz

from lodestar_veritas.agents.ingestion_agent import IngestionAgent


def test_ingestion_agent_creates_chunks_for_real_pdf(tmp_path: Path):
    pdf_path = tmp_path / "sample.pdf"

    document = fitz.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "Revenue increased by 25% in 2024 due to subscription growth. " * 80,
    )
    document.save(pdf_path)
    document.close()

    agent = IngestionAgent()
    result = agent.ingest(str(pdf_path))

    assert result["analysis"].document_type == "pdf_document"
    assert result["parsed_content"]["metadata"]["parser"] == "PDFParser"
    assert result["chunk_count"] > 0
    assert result["embedded_chunk_count"] == result["chunk_count"]