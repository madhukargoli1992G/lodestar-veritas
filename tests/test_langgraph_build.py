from lodestar_veritas.graph import LodestarGraph


def test_lodestar_graph_exposes_langgraph_builder():
    graph = LodestarGraph()

    assert hasattr(graph, "build_langgraph")
    assert callable(graph.build_langgraph)


def test_lodestar_graph_langgraph_builder_is_safe_without_dependency():
    graph = LodestarGraph()

    compiled_graph = graph.build_langgraph()

    assert compiled_graph is None or hasattr(compiled_graph, "invoke")