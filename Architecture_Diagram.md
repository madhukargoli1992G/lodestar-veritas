```bash

                    ┌────────────────────────────┐
                    │        User Query          │
                    └────────────┬───────────────┘
                                 │
                                 ▼
                   ┌────────────────────────────┐
                   │     Guardrail Agent        │
                   └────────────┬───────────────┘
                                │
                                ▼
                   ┌────────────────────────────┐
                   │   Query Rewrite Agent      │
                   └────────────┬───────────────┘
                                ▼
                   ┌────────────────────────────┐
                   │ Retrieval Router Agent     │
                   └───────┬─────────┬──────────┘
                           │         │
                  Dense    BM25   Metadata
                           │
                           ▼
                 Hybrid Retrieval (RRF)
                           │
                           ▼
                    Context Evaluator
                           │
                     Retry if Needed
                           │
                           ▼
                  Answer Generator (Ollama)
                           │
                           ▼
                  Verification Agent
                           │
                           ▼
                Hallucination Checker
                           │
                           ▼
                     RAG Guardrails
                           │
                           ▼
                Safe Response Formatter
                           │
                           ▼
                    Final API Response


```