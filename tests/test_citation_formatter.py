from lodestar_veritas.retrieval.citation_formatter import CitationFormatter


def test_citation_formatter_formats_pdf_page_citation():
    formatter = CitationFormatter()

    chunks = [
        {
            "chunk_id": "chunk_1",
            "text": "Revenue increased by 25%.",
            "metadata": {
                "file_name": "annual_report.pdf",
                "page_number": 12,
                "chunk_number": 3,
            },
            "score": 0.91,
            "rerank_score": 4,
        }
    ]

    citations = formatter.format(chunks)

    assert len(citations) == 1
    assert citations[0]["source"] == "annual_report.pdf"
    assert citations[0]["page"] == 12
    assert citations[0]["chunk"] == 3