from dataclasses import dataclass, field
from typing import Any


@dataclass
class RAGState:
    """
    Shared state object for the Lodestar Veritas Agentic RAG workflow.

    This state travels through the graph nodes:
    guardrails -> ingest -> retrieve -> evaluate context -> rewrite query
    -> answer -> verify -> final response.
    """

    query: str = ""
    file_paths: list[str] = field(default_factory=list)

    # Query rewriting / routing
    rewritten_query: str = ""
    active_query: str = ""
    route: str = "start"
    retrieval_strategy: str = "hybrid"
    retrieval_route_reason: str = ""

    # Retry loop controls
    retry_count: int = 0
    max_retries: int = 2

    # Ingestion and retrieval
    ingestion_results: list[dict[str, Any]] = field(default_factory=list)
    retrieved_chunks: list[dict[str, Any]] = field(default_factory=list)
    retrieved_count: int = 0
    context_sufficient: bool = False

    # Answer generation
    answer: str = ""
    citations: list[dict[str, Any]] = field(default_factory=list)
    sources: list[dict[str, Any]] = field(default_factory=list)
    context_used: str = ""
    confidence: float = 0.0
    answer_result: dict[str, Any] = field(default_factory=dict)

    # Verification and final response
    verification: dict[str, Any] = field(default_factory=dict)
    guardrails: dict[str, Any] = field(default_factory=dict)
    final_response: dict[str, Any] = field(default_factory=dict)
    safe_to_return: bool = False

    # Debugging / observability
    errors: list[str] = field(default_factory=list)
    events: list[str] = field(default_factory=list)


# Backward compatibility for older agents/tests
LodestarState = RAGState