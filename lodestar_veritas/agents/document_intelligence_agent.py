"""
Document Intelligence Agent for Lodestar Veritas.
"""

from lodestar_veritas.document_detector import (
    detect_file_type,
    estimate_document_complexity,
    get_file_name,
)
from lodestar_veritas.state import LodestarState
from lodestar_veritas.utils.logger import get_logger


logger = get_logger(__name__)


def document_intelligence_agent(state: LodestarState) -> LodestarState:
    logger.info("Running Document Intelligence Agent")

    file_path = state.get("file_path")

    if not file_path:
        state["error"] = "Document Intelligence Agent failed: file_path is missing."
        return state

    file_type = detect_file_type(file_path)
    file_name = get_file_name(file_path)
    complexity = estimate_document_complexity(file_path, file_type)

    state["file_type"] = file_type
    state["file_name"] = file_name
    state["document_complexity"] = complexity

    return state