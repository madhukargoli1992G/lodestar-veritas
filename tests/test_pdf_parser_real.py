from pathlib import Path

import fitz

from lodestar_veritas.parsers.pdf_parser import PDFParser


def test_pdf_parser_extracts_text(tmp_path: Path):
    pdf_path = tmp_path / "sample.pdf"

    document = fitz.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "Revenue increased by 25% in 2024 due to subscription growth.",
    )
    document.save(pdf_path)
    document.close()

    parser = PDFParser()
    result = parser.parse(str(pdf_path))

    assert result["metadata"]["parser"] == "PDFParser"
    assert result["metadata"]["page_count"] == 1
    assert "Revenue increased" in result["content"]
    assert result["pages"][0]["page_number"] == 1