"""
Document type detection for Lodestar Veritas.

This module identifies the uploaded file type and validates
whether the document is supported by the system.
"""

from pathlib import Path
from typing import Dict


SUPPORTED_FILE_TYPES: Dict[str, str] = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".csv": "csv",
    ".pptx": "pptx",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".webp": "image",
}


def detect_file_type(file_path: str) -> str:
    """
    Detect file type based on file extension.

    Args:
        file_path: Path to uploaded file.

    Returns:
        A normalized file type string.

    Raises:
        ValueError: If the file type is unsupported.
    """

    suffix = Path(file_path).suffix.lower()

    if suffix not in SUPPORTED_FILE_TYPES:
        supported = ", ".join(SUPPORTED_FILE_TYPES.keys())
        raise ValueError(
            f"Unsupported file type '{suffix}'. "
            f"Supported file types are: {supported}"
        )

    return SUPPORTED_FILE_TYPES[suffix]


def get_file_name(file_path: str) -> str:
    """
    Extract file name from file path.
    """

    return Path(file_path).name


def is_supported_file(file_path: str) -> bool:
    """
    Check if uploaded file type is supported.
    """

    suffix = Path(file_path).suffix.lower()
    return suffix in SUPPORTED_FILE_TYPES


def estimate_document_complexity(file_path: str, file_type: str) -> str:
    """
    Estimate document complexity.

    This is intentionally lightweight at this stage.
    Later, we can enhance it using page count, row count,
    image count, table count, and section count.
    """

    file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)

    if file_type in ["pdf", "docx", "pptx"]:
        if file_size_mb < 2:
            return "simple"
        if file_size_mb < 15:
            return "moderate"
        return "complex"

    if file_type == "csv":
        if file_size_mb < 5:
            return "simple"
        if file_size_mb < 50:
            return "moderate"
        return "complex"

    if file_type == "image":
        return "simple"

    return "unknown"