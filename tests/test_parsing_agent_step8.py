from lodestar_veritas.agents.parsing_agent import ParsingAgent


def test_parsing_agent_returns_analysis_and_strategy_for_unknown_file():
    agent = ParsingAgent()

    result = agent.parse("sample_report.unknown")

    assert "analysis" in result
    assert "chunk_strategy" in result
    assert "parsed_content" in result

    assert result["analysis"].document_type == "unknown"
    assert result["parsed_content"]["content"] == ""