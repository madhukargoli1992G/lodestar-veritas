from lodestar_veritas.agents.ingestion_agent import IngestionAgent
from lodestar_veritas.agents.retrieval_agent import RetrievalAgent
from lodestar_veritas.agents.answer_generator_agent import AnswerGeneratorAgent
from lodestar_veritas.agents.verification_agent import VerificationAgent
from lodestar_veritas.guardrails.rag_guardrails import RAGGuardrails
from lodestar_veritas.guardrails.safe_response_formatter import SafeResponseFormatter


class RAGOrchestratorAgent:
    """
    Coordinates the complete RAG workflow:

    1. Ingest documents
    2. Retrieve relevant chunks
    3. Generate grounded answer
    4. Verify answer grounding
    5. Apply guardrails
    6. Format safe final response
    7. Return final structured response
    """

    def __init__(self):
        self.ingestion_agent = IngestionAgent()
        self.retrieval_agent = RetrievalAgent()
        self.answer_generator_agent = AnswerGeneratorAgent()
        self.verification_agent = VerificationAgent()
        self.guardrails = RAGGuardrails()
        self.safe_response_formatter = SafeResponseFormatter()

    def ingest_file(self, file_path: str) -> dict:
        ingestion_result = self.ingestion_agent.ingest(file_path)

        self.retrieval_agent.add_documents(
            ingestion_result["embedded_chunks"]
        )

        return ingestion_result

    def ask(self, query: str, top_k: int = 5) -> dict:
        retrieved_chunks = self.retrieval_agent.retrieve(
            query=query,
            top_k=top_k,
        )

        answer_result = self.answer_generator_agent.generate(
            query=query,
            retrieved_chunks=retrieved_chunks,
        )

        verification = self.verification_agent.verify(
            answer=answer_result["answer"],
            retrieved_chunks=retrieved_chunks,
        )

        rag_result = {
            "query": query,
            "retrieved_chunks": retrieved_chunks,
            "retrieved_count": len(retrieved_chunks),
            "answer": answer_result["answer"],
            "citations": answer_result["citations"],
            "sources": answer_result["sources"],
            "context_used": answer_result["context_used"],
            "confidence": answer_result.get("confidence", 0.0),
            "verified": verification.get("verified", False),
            "is_grounded": verification.get("is_grounded", False),
            "verification": verification,
            "metadata": {
                "answer_generation": answer_result.get("metadata", {}),
                "verification_status": verification.get("status", "unknown"),
            },
        }

        guardrails = self.guardrails.apply(rag_result)
        rag_result["guardrails"] = guardrails
        rag_result["safe_to_return"] = guardrails.get("safe_to_return", False)
        rag_result["final_response"] = self.safe_response_formatter.format(
            rag_result
        )

        return rag_result