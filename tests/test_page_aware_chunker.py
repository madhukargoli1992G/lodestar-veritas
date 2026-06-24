from lodestar_veritas.chunking.page_aware_chunker import PageAwareChunker
from lodestar_veritas.agents.chunk_strategy_planner import ChunkStrategy


def test_page_aware_chunker_preserves_pdf_page_number():
    chunker = PageAwareChunker()

    parsed_content = {
        "content": "Revenue increased.",
        "pages": [
            {
                "page_number": 3,
                "text": "Revenue increased by 25% in 2024.",
            }
        ],
        "metadata": {
            "source": "sample.pdf",
            "parser": "PDFParser",
        },
    }

    strategy = ChunkStrategy(
        strategy_name="toc_aware_hierarchical_chunking",
        chunk_size=500,
        chunk_overlap=50,
        use_metadata=True,
        use_hierarchical_chunking=True,
        use_toc_aware_chunking=True,
        notes="test strategy",
    )

    chunks = chunker.chunk(parsed_content, strategy)

    assert len(chunks) == 1
    assert chunks[0].metadata["page_number"] == 3
    assert chunks[0].metadata["content_unit"] == "page"


def test_page_aware_chunker_preserves_csv_row_number():
    chunker = PageAwareChunker()

    parsed_content = {
        "content": "",
        "rows": [
            {"Metric": "Revenue", "Value": "25%"},
        ],
        "columns": ["Metric", "Value"],
        "metadata": {
            "source": "sample.csv",
            "parser": "CSVParser",
        },
    }

    strategy = ChunkStrategy(
        strategy_name="row_based_chunking",
        chunk_size=500,
        chunk_overlap=50,
        use_metadata=True,
        use_hierarchical_chunking=False,
        use_toc_aware_chunking=False,
        notes="test strategy",
    )

    chunks = chunker.chunk(parsed_content, strategy)

    assert len(chunks) == 1
    assert chunks[0].metadata["row_number"] == 1
    assert chunks[0].metadata["content_unit"] == "row"