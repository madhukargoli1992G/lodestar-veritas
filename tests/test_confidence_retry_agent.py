from lodestar_veritas.agents.confidence_retry_agent import ConfidenceRetryAgent


def test_confidence_retry_agent_retries_low_confidence():
    agent = ConfidenceRetryAgent(minimum_confidence=0.60)

    result = agent.should_retry(
        confidence=0.40,
        retry_count=0,
        max_retries=2,
    )

    assert result["should_retry"] is True
    assert result["reason"] == "low_confidence_retry"


def test_confidence_retry_agent_does_not_retry_high_confidence():
    agent = ConfidenceRetryAgent(minimum_confidence=0.60)

    result = agent.should_retry(
        confidence=0.90,
        retry_count=0,
        max_retries=2,
    )

    assert result["should_retry"] is False


def test_confidence_retry_agent_stops_at_max_retries():
    agent = ConfidenceRetryAgent(minimum_confidence=0.60)

    result = agent.should_retry(
        confidence=0.40,
        retry_count=2,
        max_retries=2,
    )

    assert result["should_retry"] is False
    assert result["retry_allowed"] is False