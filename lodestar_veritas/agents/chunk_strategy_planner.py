from dataclasses import dataclass
from lodestar_veritas.agents.content_analyzer_agent import ContentAnalysis


@dataclass
class ChunkStrategy:
    strategy_name: str
    chunk_size: int
    chunk_overlap: int
    use_metadata: bool
    use_hierarchical_chunking: bool
    use_toc_aware_chunking: bool
    notes: str


class ChunkStrategyPlanner:
    """
    Chooses the best chunking strategy based on the document content analysis.
    """

    def plan(self, analysis: ContentAnalysis) -> ChunkStrategy:
        document_type = analysis.document_type

        if document_type == "pdf_document":
            return ChunkStrategy(
                strategy_name="toc_aware_hierarchical_chunking",
                chunk_size=900,
                chunk_overlap=150,
                use_metadata=True,
                use_hierarchical_chunking=True,
                use_toc_aware_chunking=True,
                notes="PDF detected. Use TOC-aware metadata when available and hierarchical chunking for sections, subsections, and paragraphs.",
            )

        if document_type == "word_document":
            return ChunkStrategy(
                strategy_name="section_based_chunking",
                chunk_size=800,
                chunk_overlap=120,
                use_metadata=True,
                use_hierarchical_chunking=True,
                use_toc_aware_chunking=False,
                notes="DOCX detected. Use heading-aware or section-based chunking.",
            )

        if document_type == "presentation":
            return ChunkStrategy(
                strategy_name="slide_level_chunking",
                chunk_size=600,
                chunk_overlap=80,
                use_metadata=True,
                use_hierarchical_chunking=False,
                use_toc_aware_chunking=False,
                notes="Presentation detected. Chunk by slide and preserve slide number/title metadata.",
            )

        if document_type == "tabular_data":
            return ChunkStrategy(
                strategy_name="row_group_chunking",
                chunk_size=500,
                chunk_overlap=50,
                use_metadata=True,
                use_hierarchical_chunking=False,
                use_toc_aware_chunking=False,
                notes="Tabular data detected. Chunk by row groups and preserve column metadata.",
            )

        if document_type == "image":
            return ChunkStrategy(
                strategy_name="image_caption_ocr_chunking",
                chunk_size=400,
                chunk_overlap=50,
                use_metadata=True,
                use_hierarchical_chunking=False,
                use_toc_aware_chunking=False,
                notes="Image detected. Extract OCR/caption text first, then chunk extracted content.",
            )

        return ChunkStrategy(
            strategy_name="default_recursive_chunking",
            chunk_size=700,
            chunk_overlap=100,
            use_metadata=True,
            use_hierarchical_chunking=False,
            use_toc_aware_chunking=False,
            notes="Unknown or plain text document. Use default recursive chunking.",
        )