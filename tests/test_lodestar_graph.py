from pathlib import Path

from lodestar_veritas.graph import LodestarGraph


def test_lodestar_graph_runs_end_to_end(tmp_path: Path):
    sample_file = tmp_path / "sample.txt"

    sample_file.write_text(
        "Revenue increased by 25% in 2024 due to subscription growth. "
        "Risk factors include inflation and market volatility. "
        * 100,
        encoding="utf-8",
    )

    graph = LodestarGraph()

    state = graph.run(
        query="What increased in 2024?",
        file_paths=[str(sample_file)],
    )

    assert state.answer
    assert len(state.ingestion_results) == 1
    assert len(state.retrieved_chunks) > 0
    assert len(state.citations) > 0
    assert "is_grounded" in state.verification
    assert state.errors == []