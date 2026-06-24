from dataclasses import dataclass
from pathlib import Path


@dataclass
class ContentAnalysis:
    file_path: str
    file_name: str
    file_extension: str
    document_type: str
    has_tables: bool
    has_images: bool
    has_slides: bool
    has_text: bool
    complexity: str


class ContentAnalyzerAgent:
    """
    Analyzes the uploaded file and identifies what kind of content it contains.
    This helps the system decide how to chunk and retrieve the document later.
    """

    def analyze(self, file_path: str) -> ContentAnalysis:
        path = Path(file_path)
        extension = path.suffix.lower()

        document_type = self._detect_document_type(extension)

        has_tables = extension in [".csv", ".xlsx", ".xls"]
        has_images = extension in [".png", ".jpg", ".jpeg", ".webp"]
        has_slides = extension in [".pptx", ".ppt"]
        has_text = extension in [".pdf", ".docx", ".txt", ".md", ".pptx"]

        complexity = self._estimate_complexity(
            document_type=document_type,
            has_tables=has_tables,
            has_images=has_images,
            has_slides=has_slides,
            has_text=has_text,
        )

        return ContentAnalysis(
            file_path=str(path),
            file_name=path.name,
            file_extension=extension,
            document_type=document_type,
            has_tables=has_tables,
            has_images=has_images,
            has_slides=has_slides,
            has_text=has_text,
            complexity=complexity,
        )

    def _detect_document_type(self, extension: str) -> str:
        if extension == ".pdf":
            return "pdf_document"
        if extension == ".docx":
            return "word_document"
        if extension in [".pptx", ".ppt"]:
            return "presentation"
        if extension in [".csv", ".xlsx", ".xls"]:
            return "tabular_data"
        if extension in [".png", ".jpg", ".jpeg", ".webp"]:
            return "image"
        if extension in [".txt", ".md"]:
            return "plain_text"

        return "unknown"

    def _estimate_complexity(
        self,
        document_type: str,
        has_tables: bool,
        has_images: bool,
        has_slides: bool,
        has_text: bool,
    ) -> str:
        score = 0

        if has_text:
            score += 1
        if has_tables:
            score += 2
        if has_images:
            score += 2
        if has_slides:
            score += 2
        if document_type == "pdf_document":
            score += 1

        if score <= 1:
            return "low"
        if score <= 3:
            return "medium"

        return "high"