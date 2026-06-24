from typing import List


class CitationFormatter:
    """
    Converts retrieved chunk metadata into human-readable citations.
    """

    def format(self, retrieved_chunks: List[dict]) -> list[dict]:

        citations = []

        seen = set()

        for index, chunk in enumerate(retrieved_chunks, start=1):

            metadata = chunk.get("metadata", {})

            source = metadata.get("file_name") \
                or metadata.get("source", "Unknown")

            page = metadata.get("page_number")

            slide = metadata.get("slide_number")

            paragraph = metadata.get("paragraph_number")

            table = metadata.get("table_number")

            row = metadata.get("row_number")

            chunk_number = metadata.get("chunk_number")

            score = round(chunk.get("rerank_score", chunk.get("score", 0)), 3)

            key = (
                source,
                page,
                slide,
                paragraph,
                table,
                row,
                chunk_number,
            )

            if key in seen:
                continue

            seen.add(key)

            citations.append(
                {
                    "id": index,
                    "source": source,
                    "page": page,
                    "slide": slide,
                    "paragraph": paragraph,
                    "table": table,
                    "row": row,
                    "chunk": chunk_number,
                    "score": score,
                }
            )

        return citations