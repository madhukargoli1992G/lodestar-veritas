from lodestar_veritas.agents.query_rewrite_agent import QueryRewriteAgent


def test_query_rewrite_agent_returns_original_query_on_first_attempt():
    agent = QueryRewriteAgent()

    result = agent.rewrite(
        query="What increased in 2024?",
        retry_count=0,
    )

    assert result == "What increased in 2024?"


def test_query_rewrite_agent_expands_query_on_retry():
    agent = QueryRewriteAgent()

    result = agent.rewrite(
        query="What increased in 2024?",
        retry_count=1,
    )

    assert "What increased in 2024?" in result
    assert "financial" in result
    assert "regulatory" in result