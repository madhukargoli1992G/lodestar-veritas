"""
Basic tests for document detection and the Document Intelligence Agent.
"""

from lodestar_veritas.agents.document_intelligence_agent import (
    document_intelligence_agent,
)
from lodestar_veritas.document_detector import detect_file_type


def test_detect_pdf_type():
    assert detect_file_type("sample.pdf") == "pdf"


def test_detect_docx_type():
    assert detect_file_type("sample.docx") == "docx"


def test_detect_csv_type():
    assert detect_file_type("sample.csv") == "csv"


def test_detect_pptx_type():
    assert detect_file_type("sample.pptx") == "pptx"


def test_detect_image_type():
    assert detect_file_type("sample.png") == "image"


def test_document_intelligence_agent(tmp_path):
    sample_file = tmp_path / "sample.pdf"
    sample_file.write_text("Dummy PDF placeholder")

    state = {
        "file_path": str(sample_file)
    }

    result = document_intelligence_agent(state)

    assert result["file_type"] == "pdf"
    assert result["file_name"] == "sample.pdf"
    assert result["document_complexity"] in ["simple", "moderate", "complex"]