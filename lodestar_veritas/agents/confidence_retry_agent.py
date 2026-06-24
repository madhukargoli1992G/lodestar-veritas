class ConfidenceRetryAgent:
    """
    Decides whether the workflow should retry based on answer confidence.

    This is useful when retrieval succeeds but the generated answer is weak.
    """

    def __init__(self, minimum_confidence: float = 0.60):
        self.minimum_confidence = minimum_confidence

    def should_retry(self, confidence: float, retry_count: int, max_retries: int) -> dict:
        retry_allowed = retry_count < max_retries
        low_confidence = confidence < self.minimum_confidence

        should_retry = low_confidence and retry_allowed

        return {
            "should_retry": should_retry,
            "low_confidence": low_confidence,
            "retry_allowed": retry_allowed,
            "confidence": confidence,
            "minimum_confidence": self.minimum_confidence,
            "reason": "low_confidence_retry"
            if should_retry
            else "retry_not_required",
        }