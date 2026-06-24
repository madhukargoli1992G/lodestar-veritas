from pathlib import Path

import fitz


class PDFParser:
    """
    Real PDF parser using PyMuPDF.

    Extracts:
    - page text
    - page numbers
    - document metadata
    """

    def parse(self, file_path: str) -> dict:
        path = Path(file_path)

        pages = []
        full_text_parts = []

        with fitz.open(file_path) as document:
            pdf_metadata = document.metadata or {}

            for page_index, page in enumerate(document, start=1):
                page_text = page.get_text("text").strip()

                if page_text:
                    pages.append(
                        {
                            "page_number": page_index,
                            "text": page_text,
                        }
                    )
                    full_text_parts.append(
                        f"\n\n[Page {page_index}]\n{page_text}"
                    )

        full_text = "\n".join(full_text_parts).strip()

        return {
            "content": full_text,
            "pages": pages,
            "metadata": {
                "source": file_path,
                "file_name": path.name,
                "parser": "PDFParser",
                "page_count": len(pages),
                "pdf_title": pdf_metadata.get("title", ""),
                "pdf_author": pdf_metadata.get("author", ""),
                "pdf_subject": pdf_metadata.get("subject", ""),
            },
        }