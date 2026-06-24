from lodestar_veritas.agents.retrieval_router_agent import RetrievalRouterAgent


def test_retrieval_router_defaults_to_hybrid():
    router = RetrievalRouterAgent()

    result = router.route("What increased in 2024?")

    assert result["strategy"] == "hybrid"


def test_retrieval_router_detects_keyword_query():
    router = RetrievalRouterAgent()

    result = router.route("Find the exact revenue amount")

    assert result["strategy"] == "keyword"


def test_retrieval_router_detects_semantic_query():
    router = RetrievalRouterAgent()

    result = router.route("Explain the risk factors")

    assert result["strategy"] == "semantic"


def test_retrieval_router_detects_metadata_query():
    router = RetrievalRouterAgent()

    result = router.route("What does page 5 say?")

    assert result["strategy"] == "metadata"