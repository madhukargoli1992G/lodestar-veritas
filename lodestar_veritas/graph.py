from lodestar_veritas.state import RAGState
from lodestar_veritas.agents.ingestion_agent import IngestionAgent
from lodestar_veritas.agents.retrieval_agent import RetrievalAgent
from lodestar_veritas.agents.answer_generator_agent import AnswerGeneratorAgent
from lodestar_veritas.agents.verification_agent import VerificationAgent
from lodestar_veritas.agents.guardrail_agent import GuardrailAgent
from lodestar_veritas.agents.query_rewrite_agent import QueryRewriteAgent
from lodestar_veritas.agents.context_evaluator_agent import ContextEvaluatorAgent
from lodestar_veritas.guardrails.rag_guardrails import RAGGuardrails
from lodestar_veritas.guardrails.safe_response_formatter import SafeResponseFormatter
from lodestar_veritas.agents.retrieval_router_agent import RetrievalRouterAgent
from lodestar_veritas.agents.confidence_retry_agent import ConfidenceRetryAgent


class LodestarGraph:
    """
    Agentic RAG workflow executor.

    Flow:
        guardrail check
        ingest documents
        rewrite query
        retrieve context
        evaluate context
        retry retrieval if context is weak
        generate answer
        verify answer
        apply RAG guardrails
        format final response
    """

    def __init__(self):
        self.guardrail_agent = GuardrailAgent()
        self.ingestion_agent = IngestionAgent()
        self.retrieval_agent = RetrievalAgent()
        self.query_rewrite_agent = QueryRewriteAgent()
        self.context_evaluator_agent = ContextEvaluatorAgent()
        self.answer_generator_agent = AnswerGeneratorAgent()
        self.verification_agent = VerificationAgent()
        self.rag_guardrails = RAGGuardrails()
        self.safe_response_formatter = SafeResponseFormatter()
        self.retrieval_router_agent = RetrievalRouterAgent()
        self.confidence_retry_agent = ConfidenceRetryAgent()

    def confidence_retry_node(self, state: RAGState) -> RAGState:
        state.route = "confidence_retry"

        result = self.confidence_retry_agent.should_retry(
            confidence=state.confidence,
            retry_count=state.retry_count,
            max_retries=state.max_retries,
        )

        if result["should_retry"]:
            state.retry_count += 1
            state.context_sufficient = False
            state.events.append("confidence_retry_triggered")
        else:
            state.events.append("confidence_retry_not_required")

        state.events.append("confidence_retry_node_completed")
        return state
    
    def retrieval_router_node(self, state: RAGState) -> RAGState:
        state.route = "retrieval_router"

        result = self.retrieval_router_agent.route(state.active_query)

        state.retrieval_strategy = result.get("strategy", "hybrid")
        state.retrieval_route_reason = result.get("reason", "")

        state.events.append("retrieval_router_node_completed")
        return state
    
    def run(self, query: str, file_paths: list[str]) -> RAGState:
        state = RAGState(query=query, file_paths=file_paths)
        state.active_query = query
        state.events.append("workflow_started")
        
        state = self.guardrail_node(state)

        if state.errors:
            state.events.append("workflow_stopped_by_guardrails")
            return state

        state = self.ingest_node(state)

        while state.retry_count <= state.max_retries:
            state = self.rewrite_query_node(state)
            state = self.retrieval_router_node(state)
            state = self.retrieve_node(state)
            state = self.evaluate_context_node(state)

            if state.context_sufficient:
                break

            state.retry_count += 1
            state.events.append("retry_triggered")

        state = self.answer_node(state)
        state = self.confidence_retry_node(state)

        if "confidence_retry_triggered" in state.events:
            while state.retry_count <= state.max_retries:
                state = self.rewrite_query_node(state)
                state = self.retrieval_router_node(state)
                state = self.retrieve_node(state)
                state = self.evaluate_context_node(state)

                if state.context_sufficient:
                    state = self.answer_node(state)
                    break

                state.retry_count += 1
                state.events.append("retry_triggered")

        state = self.verify_node(state)
        state = self.rag_guardrails_node(state)
        state = self.final_response_node(state)

        state.events.append("workflow_completed")
        return state

    def guardrail_node(self, state: RAGState) -> RAGState:
        state.route = "guardrails"

        result = self.guardrail_agent.validate_query(state.query)

        if not result["allowed"]:
            state.errors.append(result["reason"])
            state.answer = (
                "I cannot process this request because it failed "
                "guardrail validation."
            )

        state.events.append("guardrail_node_completed")
        return state

    def ingest_node(self, state: RAGState) -> RAGState:
        state.route = "ingest"

        for file_path in state.file_paths:
            try:
                ingestion_result = self.ingestion_agent.ingest(file_path)
                state.ingestion_results.append(ingestion_result)

                self.retrieval_agent.add_documents(
                    ingestion_result["embedded_chunks"]
                )

            except Exception as error:
                state.errors.append(
                    f"Ingestion failed for {file_path}: {error}"
                )

        state.events.append("ingest_node_completed")
        return state

    def rewrite_query_node(self, state: RAGState) -> RAGState:
        state.route = "rewrite_query"

        state.rewritten_query = self.query_rewrite_agent.rewrite(
            query=state.query,
            retry_count=state.retry_count,
        )

        state.active_query = state.rewritten_query or state.query
        state.events.append("rewrite_query_node_completed")

        return state

    def retrieve_node(self, state: RAGState) -> RAGState:
        state.route = "retrieve"

        try:
            state.retrieved_chunks = self.retrieval_agent.retrieve(
                query=state.active_query,
                top_k=5,
            )
            state.retrieved_count = len(state.retrieved_chunks)

        except Exception as error:
            state.errors.append(f"Retrieval failed: {error}")

        state.events.append("retrieve_node_completed")
        return state

    def evaluate_context_node(self, state: RAGState) -> RAGState:
        state.route = "evaluate_context"

        result = self.context_evaluator_agent.evaluate(
            state.retrieved_chunks
        )

        state.context_sufficient = result["context_sufficient"]
        state.retrieved_count = result["retrieved_count"]

        if not state.context_sufficient:
            state.events.append(result["reason"])

        state.events.append("evaluate_context_node_completed")
        return state

    def answer_node(self, state: RAGState) -> RAGState:
        state.route = "answer"

        try:
            answer_result = self.answer_generator_agent.generate(
                query=state.active_query,
                retrieved_chunks=state.retrieved_chunks,
            )

            state.answer_result = answer_result
            state.answer = answer_result["answer"]
            state.citations = answer_result.get("citations", [])
            state.sources = answer_result.get("sources", [])
            state.context_used = answer_result.get("context_used", "")
            state.confidence = answer_result.get("confidence", 0.0)

        except Exception as error:
            state.errors.append(f"Answer generation failed: {error}")

        state.events.append("answer_node_completed")
        return state

    def verify_node(self, state: RAGState) -> RAGState:
        state.route = "verify"

        try:
            state.verification = self.verification_agent.verify(
                {
                    "answer": state.answer,
                    "context_used": state.context_used,
                    "citations": state.citations,
                    "confidence": state.confidence,
                    "grounded": bool(state.retrieved_chunks),
                }
            )

        except Exception as error:
            state.errors.append(f"Verification failed: {error}")

        state.events.append("verify_node_completed")
        return state

    def rag_guardrails_node(self, state: RAGState) -> RAGState:
        state.route = "rag_guardrails"

        rag_result = {
            "answer": state.answer,
            "citations": state.citations,
            "sources": state.sources,
            "confidence": state.confidence,
            "verified": state.verification.get("verified", False),
            "is_grounded": state.verification.get("is_grounded", False),
            "verification": state.verification,
        }

        state.guardrails = self.rag_guardrails.apply(rag_result)
        state.safe_to_return = state.guardrails.get(
            "safe_to_return",
            False,
        )

        state.events.append("rag_guardrails_node_completed")
        return state

    def final_response_node(self, state: RAGState) -> RAGState:
        state.route = "final_response"

        rag_result = {
            "answer": state.answer,
            "citations": state.citations,
            "sources": state.sources,
            "confidence": state.confidence,
            "verified": state.verification.get("verified", False),
            "is_grounded": state.verification.get("is_grounded", False),
            "guardrails": state.guardrails,
        }

        state.final_response = self.safe_response_formatter.format(
            rag_result
        )

        state.events.append("final_response_node_completed")
        return state
    def build_langgraph(self):
        """
        Builds a real LangGraph workflow when langgraph is installed.

        This keeps the project compatible with environments where LangGraph
        is not installed, while still supporting true LangGraph execution.
        """
        try:
            from langgraph.graph import StateGraph, END
        except ImportError:
            return None

        workflow = StateGraph(RAGState)

        workflow.add_node("guardrails", self.guardrail_node)
        workflow.add_node("ingest", self.ingest_node)
        workflow.add_node("rewrite_query", self.rewrite_query_node)
        workflow.add_node("retrieve", self.retrieve_node)
        workflow.add_node("evaluate_context", self.evaluate_context_node)
        workflow.add_node("answer", self.answer_node)
        workflow.add_node("verify", self.verify_node)
        workflow.add_node("rag_guardrails", self.rag_guardrails_node)
        workflow.add_node("final_response", self.final_response_node)

        workflow.set_entry_point("guardrails")

        workflow.add_edge("guardrails", "ingest")
        workflow.add_edge("ingest", "rewrite_query")
        workflow.add_edge("rewrite_query", "retrieve")
        workflow.add_edge("retrieve", "evaluate_context")

        workflow.add_conditional_edges(
            "evaluate_context",
            self._route_after_context_evaluation,
            {
                "retry": "rewrite_query",
                "answer": "answer",
            },
        )

        workflow.add_edge("answer", "verify")
        workflow.add_edge("verify", "rag_guardrails")
        workflow.add_edge("rag_guardrails", "final_response")
        workflow.add_edge("final_response", END)

        return workflow.compile()

    def _route_after_context_evaluation(self, state: RAGState) -> str:
        if state.context_sufficient:
            return "answer"

        if state.retry_count < state.max_retries:
            state.retry_count += 1
            state.events.append("langgraph_retry_triggered")
            return "retry"

        return "answer"       