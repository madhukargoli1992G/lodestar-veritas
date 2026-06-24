from lodestar_veritas.verification.answer_verifier import AnswerVerifier
from lodestar_veritas.verification.hallucination_checker import HallucinationChecker


class VerificationAgent:
    """
    Agent-level wrapper around answer verification and hallucination checks.

    Supports two calling styles:

    1. verify(generated_result)
    2. verify(answer=answer, retrieved_chunks=retrieved_chunks)
    """

    def __init__(self, minimum_confidence: float = 0.60):
        self.minimum_confidence = minimum_confidence
        self.answer_verifier = AnswerVerifier(
            minimum_confidence=minimum_confidence
        )
        self.hallucination_checker = HallucinationChecker(
            minimum_confidence=minimum_confidence
        )

    def verify(self, generated_result: dict | None = None, **kwargs) -> dict:
        if generated_result is None:
            generated_result = self._build_generated_result_from_kwargs(kwargs)

        answer = generated_result.get("answer", "")
        context_used = generated_result.get("context_used", "")
        citations = generated_result.get("citations", [])
        confidence = generated_result.get("confidence", 0.75)
        grounded = generated_result.get("grounded", True)

        verification_result = self.answer_verifier.verify_answer(
            answer=answer,
            context_used=context_used,
            citations=citations,
            confidence=confidence,
        )

        hallucination_result = self.hallucination_checker.check(
            answer=answer,
            context_used=context_used,
            citations=citations,
            confidence=confidence,
        )

        if hallucination_result["hallucination_risk"]:
            verification_result["verified"] = False
            verification_result["status"] = "failed"

            for risk in hallucination_result["risks"]:
                if risk not in verification_result["issues"]:
                    verification_result["issues"].append(risk)

        if not grounded:
            verification_result["verified"] = False
            verification_result["status"] = "failed"

            if "not_grounded" not in verification_result["issues"]:
                verification_result["issues"].append("not_grounded")

        verification_result["is_grounded"] = verification_result["verified"]
        verification_result["hallucination_check"] = hallucination_result

        return verification_result

    def _build_generated_result_from_kwargs(self, kwargs: dict) -> dict:
        answer = kwargs.get("answer", "")
        retrieved_chunks = kwargs.get("retrieved_chunks", [])

        context_used = self._build_context_from_chunks(retrieved_chunks)
        citations = self._build_citations_from_chunks(retrieved_chunks)

        return {
            "answer": answer,
            "retrieved_chunks": retrieved_chunks,
            "context_used": context_used,
            "citations": citations,
            "confidence": 0.75 if retrieved_chunks else 0.0,
            "grounded": bool(answer and retrieved_chunks),
        }

    def _build_context_from_chunks(self, retrieved_chunks: list[dict]) -> str:
        context_parts = []

        for idx, chunk in enumerate(retrieved_chunks, start=1):
            text = chunk.get("text", "").strip()

            if text:
                context_parts.append(f"[{idx}] {text}")

        return "\n".join(context_parts)

    def _build_citations_from_chunks(
        self,
        retrieved_chunks: list[dict],
    ) -> list[dict]:
        citations = []

        for idx, chunk in enumerate(retrieved_chunks, start=1):
            metadata = chunk.get("metadata", {})

            citation = {
                "source": metadata.get(
                    "source",
                    metadata.get("file_name", "unknown_source"),
                ),
                "chunk": metadata.get("chunk_number", idx),
            }

            citations.append(citation)

        return citations