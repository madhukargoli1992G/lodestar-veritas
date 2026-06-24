from lodestar_veritas.agents.chunking_agent import ChunkingAgent
from lodestar_veritas.agents.content_analyzer_agent import ContentAnalyzerAgent
from lodestar_veritas.agents.chunk_strategy_planner import ChunkStrategyPlanner


def test_chunking_agent_chunks_parsed_content():
    analyzer = ContentAnalyzerAgent()
    planner = ChunkStrategyPlanner()
    chunking_agent = ChunkingAgent()

    analysis = analyzer.analyze("sample.txt")
    strategy = planner.plan(analysis)

    parsed_result = {
        "analysis": analysis,
        "chunk_strategy": strategy,
        "parsed_content": {
            "content": "This is a test document. " * 100,
            "metadata": {
                "source": "sample.txt",
                "parser": "TestParser",
            },
        },
    }

    chunks = chunking_agent.chunk(parsed_result)

    assert len(chunks) > 1
    assert chunks[0].metadata["source"] == "sample.txt"
    assert chunks[0].metadata["chunk_strategy"] == strategy.strategy_name