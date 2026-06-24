from lodestar_veritas.graph import LodestarGraph


def test_lodestar_graph_runs_phase2_flow_with_no_files():
    graph = LodestarGraph()

    state = graph.run(
        query="What increased in 2024?",
        file_paths=[],
    )

    assert state.query == "What increased in 2024?"
    assert "workflow_started" in state.events
    assert "rewrite_query_node_completed" in state.events
    assert "retrieve_node_completed" in state.events
    assert "evaluate_context_node_completed" in state.events
    assert "answer_node_completed" in state.events
    assert "verify_node_completed" in state.events
    assert "rag_guardrails_node_completed" in state.events
    assert "final_response_node_completed" in state.events
    assert "workflow_completed" in state.events
    assert isinstance(state.final_response, dict)


def test_lodestar_graph_tracks_retry_events_when_context_missing():
    graph = LodestarGraph()

    state = graph.run(
        query="What increased in 2024?",
        file_paths=[],
    )

    assert state.retry_count >= 1
    assert "retry_triggered" in state.events
    assert state.context_sufficient is False