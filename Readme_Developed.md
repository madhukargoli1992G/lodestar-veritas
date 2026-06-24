# Lodestar Veritas

Lodestar Veritas is an agentic multimodal RAG platform for financial, regulatory, and business documents.

## Features

- Document type detection
- Content analyzer agent
- Chunk strategy planner
- Recursive chunking
- Metadata enrichment
- Local embedding wrapper
- In-memory vector store
- Dense retrieval
- BM25 keyword retrieval
- Hybrid retrieval with Reciprocal Rank Fusion
- Simple reranking
- Citation-aware answer generation
- Answer verification
- Guardrails
- Lightweight LangGraph-style workflow
- Retrieval evaluation metrics
- FastAPI endpoint
- CLI runner

## Architecture

```text
File
  -> Content Analyzer
  -> Chunk Strategy Planner
  -> Parser
  -> Chunking Agent
  -> Metadata Agent
  -> Embedding Agent
  -> Vector Store
  -> Hybrid Retrieval
  -> Reranker
  -> Answer Generator
  -> Verification Agent
```

## Verification and Guardrails Layer

The project now includes a verification and guardrails layer after answer generation.

### Flow

```text
Retrieved Chunks
      ↓
Answer Generator Agent
      ↓
Verification Agent
      ↓
Hallucination Checker
      ↓
RAG Guardrails
      ↓
Safe Response Formatter
      ↓
Final 
```

## Final Orchestrator Output

The orchestrator now returns:

{## Components

### 🤖 Answer Generator Agent

Responsible for generating grounded answers using the retrieved document chunks.

**Responsibilities**

* Generates answers from the retrieved document context.
* Uses **Ollama** as the local Large Language Model (LLM) when available.
* Falls back to context stitching if the LLM is unavailable.
* Produces structured output including:

  * Answer
  * Citations
  * Source information
  * Confidence score
  * Grounding metadata

---

### ✅ Verification Agent

Acts as the verification layer between answer generation and the final response.

**Responsibilities**

* Verifies that the generated answer is supported by the retrieved documents.
* Integrates answer verification and hallucination detection.
* Supports both:

  * Direct verification using a generated result object.
  * Orchestrator-based verification using the answer and retrieved chunks.
* Returns verification status, grounding information, and validation issues.

---

### 🔍 Answer Verifier

Performs deterministic validation of the generated answer.

**Checks Performed**

* Answer is not empty.
* Supporting context exists.
* Citations are present.
* Confidence score meets the configured threshold.

This component ensures that only sufficiently supported answers proceed to the next stage.

---

### 🧠 Hallucination Checker

Identifies potential hallucinations before the response is returned.

**Checks Performed**

* Answer exists without supporting context.
* Answer exists without citations.
* Confidence score is below the minimum threshold.

Instead of attempting to detect hallucinations perfectly, this component provides a practical risk assessment that can be used by downstream guardrails.

---

### 🛡️ RAG Guardrails

Applies safety and quality rules before the response is returned to the user.

**Responsibilities**

* Prevents unsafe or low-quality responses from being treated as verified.
* Detects:

  * Empty answers
  * Missing citations
  * Hallucination risks
  * Failed verification
* Produces:

  * Safety status
  * Warning messages
  * Response eligibility (`safe_to_return`)

---

### 📦 Safe Response Formatter

Formats the final API-ready response after all verification stages have completed.

**Responsibilities**

* Returns a clean, user-facing response.
* Preserves:

  * Answer
  * Citations
  * Sources
  * Confidence score
  * Verification status
* Returns a safe fallback message whenever the response fails the configured guardrails.

This component serves as the final presentation layer before the response is delivered to the user.

```

    "answer": "...",
    "citations": [...],
    "sources": [...],
    "confidence": 0.95,
    "verified": True,
    "is_grounded": True,
    "guardrails": {...},
    "safe_to_return": True,
    "final_response": {...}
}
```

## 💼 Explanation

In this project, I did not directly return the LLM answer. After retrieval and answer generation, I added a verification layer to check grounding, confidence, citations, and hallucination risk. Then I applied guardrails and formatted a safe final response. This makes the RAG system more production-ready because it reduces unsupported answers and gives clear metadata for debugging and evaluation.


Then run:

```bash

pytest

Expected:

64 passed

```
After that, this phase is complete.

## Phase 2: Agentic RAG Workflow

Phase 2 upgrades the project from a procedural RAG pipeline into an agentic workflow.

Instead of simply retrieving context and generating an answer, the system now performs query rewriting, context evaluation, retry logic, answer verification, hallucination checks, guardrails, and final safe response formatting.

### Agentic Workflow

```text
User Query
    ↓
Query Guardrail Check
    ↓
Document Ingestion
    ↓
Query Rewrite Agent
    ↓
Retrieval Agent
    ↓
Context Evaluator Agent
    ↓
Is context sufficient?
    ├── No → Rewrite query and retrieve again
    └── Yes
          ↓
Answer Generator Agent
    ↓
Verification Agent
    ↓
RAG Guardrails
    ↓
Safe Response Formatter
    ↓
Final Response
```
# 🚀 Phase 2: Agentic RAG Workflow

Phase 2 transforms **Lodestar Veritas** from a traditional Retrieval-Augmented Generation (RAG) pipeline into an **Agentic RAG workflow**.

Instead of performing a single retrieval followed by answer generation, the system now evaluates the retrieved context, rewrites the query when necessary, retries retrieval, verifies the generated answer, applies safety guardrails, and returns a structured, production-ready response.

---

## 🎯 Objectives

* Introduce an **Agentic AI workflow** using a shared workflow state.
* Improve retrieval quality through **query rewriting**.
* Evaluate retrieved context before generating an answer.
* Support **automatic retry loops** when insufficient context is found.
* Increase answer reliability through **verification and hallucination detection**.
* Produce safe, structured, API-ready responses.

---

# 🏗️ Agentic Workflow

```text
                   User Query
                        │
                        ▼
             Query Guardrail Check
                        │
                        ▼
              Document Ingestion
                        │
                        ▼
              Query Rewrite Agent
                        │
                        ▼
               Retrieval Agent
                        │
                        ▼
           Context Evaluator Agent
                        │
            ┌───────────┴───────────┐
            │                       │
            │ Context Sufficient?   │
            │                       │
            └───────┬───────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
      No ▼                     ▼ Yes
 Rewrite Query            Generate Answer
        │                       │
        └──────────────┬────────┘
                       ▼
              Verification Agent
                       │
                       ▼
                RAG Guardrails
                       │
                       ▼
          Safe Response Formatter
                       │
                       ▼
                Final Response
```

---

# 🧩 Phase 2 Components

## 📌 RAGState

The shared workflow state used by every node in the graph.

### Responsibilities

* Stores the original user query.
* Stores rewritten queries during retry loops.
* Tracks retrieved document chunks.
* Stores generated answers.
* Maintains verification and guardrail results.
* Records workflow events for debugging and observability.
* Preserves workflow state across every graph node.

---

## 🔄 Query Rewrite Agent

Improves retrieval quality by rewriting or expanding the user's query whenever retrieved context is insufficient.

### Responsibilities 

* Cleans the original query.
* Expands the query during retry attempts.
* Produces retrieval-friendly search queries.
* Increases the likelihood of retrieving relevant document chunks.

---

## 📊 Context Evaluator Agent

Determines whether the retrieved document context is sufficient for answer generation.

### Evaluation Criteria

* Number of retrieved chunks.
* Average retrieval score.
* Minimum confidence threshold.

### Responsibilities

* Determines whether the workflow should continue.
* Triggers another retrieval attempt if necessary.
* Prevents answer generation using weak or insufficient context.

---

## 🕸️ LodestarGraph

The central workflow engine responsible for coordinating every stage of the Agentic RAG pipeline.

### Workflow Responsibilities

1. Validate the incoming query.
2. Ingest documents.
3. Rewrite the query when required.
4. Retrieve relevant document chunks.
5. Evaluate retrieved context.
6. Retry retrieval if context is insufficient.
7. Generate a grounded answer.
8. Verify the generated answer.
9. Apply safety guardrails.
10. Format the final API-ready response.

---

## 🔁 Retry Loop

Unlike traditional one-shot RAG systems, Lodestar Veritas supports **automatic retrieval retries**.

When insufficient context is retrieved:

1. The query is rewritten.
2. Retrieval is executed again.
3. Context is re-evaluated.
4. The workflow proceeds only after sufficient context is available or the retry limit is reached.

This significantly improves retrieval quality and answer reliability.

---

## 📈 Workflow Events

Every graph node records execution events.

Example events include:

* `workflow_started`
* `guardrail_node_completed`
* `ingest_node_completed`
* `rewrite_query_node_completed`
* `retrieve_node_completed`
* `evaluate_context_node_completed`
* `retry_triggered`
* `answer_node_completed`
* `verify_node_completed`
* `rag_guardrails_node_completed`
* `final_response_node_completed`
* `workflow_completed`

These events improve:

* Debugging
* Observability
* Workflow tracing
* Production monitoring
* Interview demonstrations

---

# ⭐ Key Improvements Over Traditional RAG

| Traditional RAG             | Lodestar Veritas Phase 2                            |
| --------------------------- | --------------------------------------------------- |
| Single retrieval attempt    | Multiple retrieval attempts with retry logic        |
| Static user query           | Dynamic query rewriting                             |
| Immediate answer generation | Context evaluation before generation                |
| No workflow state           | Shared workflow state (`RAGState`)                  |
| Limited observability       | Full workflow event tracking                        |
| No retry mechanism          | Automatic retry loop                                |
| Minimal validation          | Verification + Hallucination Detection + Guardrails |

---

# 💼 Explanation

Lodestar Veritas implements an **Agentic Retrieval-Augmented Generation (RAG)** architecture rather than a traditional linear RAG pipeline.

The system maintains a shared workflow state throughout execution. After retrieving document chunks, it evaluates whether the retrieved context is sufficient to answer the user's question. If the retrieved information is inadequate, the workflow automatically rewrites the query and performs another retrieval attempt.

Once sufficient context has been collected, the workflow generates a grounded answer, verifies its quality, performs hallucination detection, applies safety guardrails, and formats a clean, API-ready response.

This iterative workflow provides greater robustness, improved retrieval quality, better traceability, enhanced observability, and safer responses, making the system suitable for production-grade enterprise AI applications.

---

# ✅ Phase 2 Highlights

* Agentic workflow execution
* Shared workflow state management
* Intelligent query rewriting
* Context sufficiency evaluation
* Automatic retrieval retry loop
* Workflow event tracking
* Verification and hallucination detection
* Guardrails for response safety
* Safe API response formatting
* Production-ready modular architecture
