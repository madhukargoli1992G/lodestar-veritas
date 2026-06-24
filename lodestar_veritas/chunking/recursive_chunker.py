from lodestar_veritas.chunking.chunk_models import DocumentChunk


class RecursiveChunker:
    """
    Simple recursive-style chunker.

    For now, it chunks text by character length with overlap.
    Later we can improve it to split by headings, paragraphs, tables, and sections.
    """

    def chunk(
        self,
        text: str,
        chunk_size: int = 700,
        chunk_overlap: int = 100,
        metadata: dict | None = None,
    ) -> list[DocumentChunk]:

        if not text:
            return []

        metadata = metadata or {}

        chunks = []
        start = 0
        chunk_number = 1

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append(
                DocumentChunk(
                    chunk_id=f"chunk_{chunk_number}",
                    text=chunk_text,
                    metadata={
                        **metadata,
                        "chunk_number": chunk_number,
                        "chunk_size": chunk_size,
                        "chunk_overlap": chunk_overlap,
                    },
                )
            )

            chunk_number += 1
            start = end - chunk_overlap

            if start < 0:
                start = 0

            if start >= len(text):
                break

        return chunks