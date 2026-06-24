from lodestar_veritas.retrieval.query_router import QueryRouter


def test_query_router_returns_hybrid_for_financial_question():
    router = QueryRouter()

    route = router.route("What was revenue in 2024?")

    assert route == "hybrid"