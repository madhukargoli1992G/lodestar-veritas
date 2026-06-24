from lodestar_veritas.graph import LodestarGraph
from lodestar_veritas.state import RAGState


def test_graph_retrieval_router_node_defaults_to_hybrid():
    graph = LodestarGraph()

    state = RAGState(
        query="What increased in 2024?",
        active_query="What increased in 2024?",
    )

    result = graph.retrieval_router_node(state)

    assert result.retrieval_strategy == "hybrid"
    assert result.retrieval_route_reason != ""
    assert "retrieval_router_node_completed" in result.events


def test_graph_retrieval_router_detects_keyword():
    graph = LodestarGraph()

    state = RAGState(
        query="Find the exact revenue amount",
        active_query="Find the exact revenue amount",
    )

    result = graph.retrieval_router_node(state)

    assert result.retrieval_strategy == "keyword"


def test_graph_retrieval_router_detects_semantic():
    graph = LodestarGraph()

    state = RAGState(
        query="Explain the financial risks",
        active_query="Explain the financial risks",
    )

    result = graph.retrieval_router_node(state)

    assert result.retrieval_strategy == "semantic"


def test_graph_retrieval_router_detects_metadata():
    graph = LodestarGraph()

    state = RAGState(
        query="What is on page 12?",
        active_query="What is on page 12?",
    )

    result = graph.retrieval_router_node(state)

    assert result.retrieval_strategy == "metadata"