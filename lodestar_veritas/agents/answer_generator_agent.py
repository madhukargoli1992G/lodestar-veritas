from lodestar_veritas.llm.ollama_client import OllamaClient
from lodestar_veritas.llm.prompt_builder import PromptBuilder
from lodestar_veritas.retrieval.citation_formatter import CitationFormatter


class AnswerGeneratorAgent:
    """
    Generates grounded answers using Ollama when available.
    Falls back to context stitching if Ollama is unavailable.
    """

    def __init__(self, use_llm: bool = True):
        self.use_llm = use_llm
        self.ollama_client = OllamaClient()
        self.prompt_builder = PromptBuilder()
        self.citation_formatter = CitationFormatter()

    def generate(self, query: str, retrieved_chunks: list[dict]) -> dict:
        if not retrieved_chunks:
            return {
                "query": query,
                "answer": "I could not find relevant information in the indexed documents.",
                "citations": [],
                "sources": [],
                "context_used": "",
                "grounded": False,
                "confidence": 0.0,
                "metadata": {
                    "retrieved_chunks": 0,
                    "llm_used": False,
                    "status": "no_context_found",
                },
            }

        context_used = self._build_context_used(retrieved_chunks)
        citations = self.citation_formatter.format(retrieved_chunks)
        sources = self._build_sources(retrieved_chunks)

        llm_used = False

        if self.use_llm:
            try:
                prompt = self.prompt_builder.build_answer_prompt(
                    query=query,
                    context=context_used,
                )

                answer = self.ollama_client.generate(prompt)

                if not answer or not answer.strip():
                    answer = self._fallback_answer(retrieved_chunks)

                llm_used = True

            except Exception:
                answer = self._fallback_answer(retrieved_chunks)
        else:
            answer = self._fallback_answer(retrieved_chunks)

        confidence = self._estimate_confidence(retrieved_chunks)

        return {
            "query": query,
            "answer": answer.strip(),
            "citations": citations,
            "sources": sources,
            "context_used": context_used,
            "grounded": True,
            "confidence": confidence,
            "metadata": {
                "retrieved_chunks": len(retrieved_chunks),
                "llm_used": llm_used,
                "status": "answer_generated",
            },
        }

    def _build_context_used(self, retrieved_chunks: list[dict]) -> str:
        context_blocks = []

        for idx, chunk in enumerate(retrieved_chunks, start=1):
            text = chunk.get("text", "")
            metadata = chunk.get("metadata", {})

            source = metadata.get("source", "unknown_source")
            page = metadata.get("page", "N/A")
            chunk_id = chunk.get("chunk_id", metadata.get("chunk_id", f"chunk_{idx}"))

            block = (
                f"[{idx}]\n"
                f"Source: {source}\n"
                f"Page: {page}\n"
                f"Chunk ID: {chunk_id}\n"
                f"Text:\n{text}"
            )

            context_blocks.append(block)

        return "\n\n---\n\n".join(context_blocks)

    def _build_sources(self, retrieved_chunks: list[dict]) -> list[dict]:
        sources = []

        for chunk in retrieved_chunks:
            metadata = chunk.get("metadata", {})

            source = {
                "source": metadata.get("source", "unknown_source"),
                "page": metadata.get("page", "N/A"),
                "chunk_id": chunk.get("chunk_id", metadata.get("chunk_id", "N/A")),
                "score": chunk.get("score", None),
            }

            sources.append(source)

        return sources

    def _fallback_answer(self, retrieved_chunks: list[dict]) -> str:
        answer_parts = []

        for idx, chunk in enumerate(retrieved_chunks, start=1):
            text = chunk.get("text", "").strip()

            if text:
                answer_parts.append(f"Relevant context {idx}: {text}")

        if not answer_parts:
            return "Relevant documents were retrieved, but no readable text was available."

        return "\n\n".join(answer_parts)

    def _estimate_confidence(self, retrieved_chunks: list[dict]) -> float:
        if not retrieved_chunks:
            return 0.0

        scores = []

        for chunk in retrieved_chunks:
            score = chunk.get("score")

            if isinstance(score, (int, float)):
                scores.append(float(score))

        if not scores:
            return 0.75

        avg_score = sum(scores) / len(scores)

        if avg_score > 1:
            avg_score = avg_score / 100

        return round(min(max(avg_score, 0.0), 1.0), 2)