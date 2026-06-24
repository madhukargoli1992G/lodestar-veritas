from lodestar_veritas.evaluation.retrieval_metrics import RetrievalMetrics


def test_reciprocal_rank():
    metrics = RetrievalMetrics()

    score = metrics.reciprocal_rank(
        retrieved_ids=["chunk_3", "chunk_2", "chunk_1"],
        relevant_ids={"chunk_2"},
    )

    assert score == 0.5


def test_recall_at_k():
    metrics = RetrievalMetrics()

    score = metrics.recall_at_k(
        retrieved_ids=["chunk_1", "chunk_2"],
        relevant_ids={"chunk_1", "chunk_3"},
        k=2,
    )

    assert score == 0.5