from lodestar_veritas.agents.content_analyzer_agent import ContentAnalyzerAgent
from lodestar_veritas.agents.chunk_strategy_planner import ChunkStrategyPlanner


def test_content_analyzer_for_pdf():
    analyzer = ContentAnalyzerAgent()

    result = analyzer.analyze("sample_report.pdf")

    assert result.file_name == "sample_report.pdf"
    assert result.file_extension == ".pdf"
    assert result.document_type == "pdf_document"
    assert result.has_text is True


def test_chunk_strategy_for_pdf():
    analyzer = ContentAnalyzerAgent()
    planner = ChunkStrategyPlanner()

    analysis = analyzer.analyze("sample_report.pdf")
    strategy = planner.plan(analysis)

    assert strategy.strategy_name == "toc_aware_hierarchical_chunking"
    assert strategy.use_metadata is True
    assert strategy.use_hierarchical_chunking is True
    assert strategy.use_toc_aware_chunking is True