from lodestar_veritas.chunking.chunk_models import DocumentChunk
from lodestar_veritas.chunking.recursive_chunker import RecursiveChunker


class PageAwareChunker:
    """
    Creates chunks while preserving page/slide/paragraph/table metadata when available.
    """

    def __init__(self):
        self.recursive_chunker = RecursiveChunker()

    def chunk(self, parsed_content: dict, strategy) -> list[DocumentChunk]:
        metadata = parsed_content.get("metadata", {})
        parser = metadata.get("parser", "")

        if parser == "PDFParser" and parsed_content.get("pages"):
            return self._chunk_pages(parsed_content, strategy)

        if parser == "PPTParser" and parsed_content.get("slides"):
            return self._chunk_slides(parsed_content, strategy)

        if parser == "DOCXParser":
            return self._chunk_docx(parsed_content, strategy)

        if parser == "CSVParser" and parsed_content.get("rows"):
            return self._chunk_rows(parsed_content, strategy)

        return self.recursive_chunker.chunk(
            text=parsed_content.get("content", ""),
            chunk_size=strategy.chunk_size,
            chunk_overlap=strategy.chunk_overlap,
            metadata={
            **metadata,
            "chunk_strategy": strategy.strategy_name,
    },
)

    def _chunk_pages(self, parsed_content: dict, strategy) -> list[DocumentChunk]:
        all_chunks = []
        base_metadata = parsed_content.get("metadata", {})

        for page in parsed_content["pages"]:
            page_number = page["page_number"]
            page_text = page["text"]

            page_chunks = self.recursive_chunker.chunk(
                text=page_text,
                chunk_size=strategy.chunk_size,
                chunk_overlap=strategy.chunk_overlap,
                metadata={
                    **base_metadata,
                    "page_number": page_number,
                    "content_unit": "page",
                    "chunk_strategy": strategy.strategy_name,
                },
            )

            all_chunks.extend(page_chunks)

        return self._renumber_chunks(all_chunks)

    def _chunk_slides(self, parsed_content: dict, strategy) -> list[DocumentChunk]:
        all_chunks = []
        base_metadata = parsed_content.get("metadata", {})

        for slide in parsed_content["slides"]:
            slide_number = slide["slide_number"]
            slide_text = slide["text"]

            if not slide_text:
                continue

            slide_chunks = self.recursive_chunker.chunk(
                text=slide_text,
                chunk_size=strategy.chunk_size,
                chunk_overlap=strategy.chunk_overlap,
                metadata={
                    **base_metadata,
                    "slide_number": slide_number,
                    "content_unit": "slide",
                    "chunk_strategy": strategy.strategy_name
                },
            )

            all_chunks.extend(slide_chunks)

        return self._renumber_chunks(all_chunks)

    def _chunk_docx(self, parsed_content: dict, strategy) -> list[DocumentChunk]:
        all_chunks = []
        base_metadata = parsed_content.get("metadata", {})

        for paragraph in parsed_content.get("paragraphs", []):
            paragraph_text = paragraph.get("text", "")
            if not paragraph_text:
                continue

            paragraph_chunks = self.recursive_chunker.chunk(
                text=paragraph_text,
                chunk_size=strategy.chunk_size,
                chunk_overlap=strategy.chunk_overlap,
                metadata={
                    **base_metadata,
                    "paragraph_number": paragraph.get("paragraph_number"),
                    "paragraph_style": paragraph.get("style"),
                    "content_unit": "paragraph",
                    "chunk_strategy": strategy.strategy_name
                },
            )

            all_chunks.extend(paragraph_chunks)

        for table in parsed_content.get("tables", []):
            table_number = table.get("table_number")
            rows = table.get("rows", [])

            table_text = "\n".join(" | ".join(row) for row in rows)

            table_chunks = self.recursive_chunker.chunk(
                text=table_text,
                chunk_size=strategy.chunk_size,
                chunk_overlap=strategy.chunk_overlap,
                metadata={
                    **base_metadata,
                    "table_number": table_number,
                    "content_unit": "table",
                },
            )

            all_chunks.extend(table_chunks)

        return self._renumber_chunks(all_chunks)

    def _chunk_rows(self, parsed_content: dict, strategy) -> list[DocumentChunk]:
        all_chunks = []
        base_metadata = parsed_content.get("metadata", {})
        columns = parsed_content.get("columns", [])

        for row_index, row in enumerate(parsed_content.get("rows", []), start=1):
            row_text = " | ".join(f"{column}: {row[column]}" for column in columns)

            row_chunks = self.recursive_chunker.chunk(
                text=row_text,
                chunk_size=strategy.chunk_size,
                chunk_overlap=strategy.chunk_overlap,
                metadata={
                    **base_metadata,
                    "row_number": row_index,
                    "columns": columns,
                    "content_unit": "row",
                    "chunk_strategy": strategy.strategy_name
                },
            )

            all_chunks.extend(row_chunks)

        return self._renumber_chunks(all_chunks)

    def _renumber_chunks(self, chunks: list[DocumentChunk]) -> list[DocumentChunk]:
        renumbered = []

        for index, chunk in enumerate(chunks, start=1):
            metadata = dict(chunk.metadata)
            metadata["chunk_number"] = index

            renumbered.append(
                DocumentChunk(
                    chunk_id=f"chunk_{index}",
                    text=chunk.text,
                    metadata=metadata,
                )
            )

        return renumbered