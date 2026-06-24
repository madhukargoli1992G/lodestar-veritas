# Changelog

## v1.0.0 - Lodestar Veritas Initial Release

### Added

- Agentic multimodal RAG workflow
- Shared `RAGState` workflow state
- LangGraph-compatible graph execution
- Query guardrail validation
- Query rewrite agent
- Retrieval router agent
- Context evaluator agent
- Confidence retry agent
- Multi-format document ingestion
- PDF parser
- DOCX parser
- PPTX parser
- CSV parser
- XLSX parser
- Image parser
- Text parser
- Metadata-aware parsing
- TOC-aware chunking
- Page-aware chunking
- Recursive chunking
- Local embedding model support
- Dense retrieval
- BM25 retrieval
- Hybrid retrieval
- Reciprocal Rank Fusion
- Reranking
- Answer generation with Ollama support
- LLM fallback response generation
- Citation formatting
- Answer verification
- Hallucination risk checking
- RAG guardrails
- Safe response formatter
- FastAPI application
- `/ask` endpoint
- `/health` endpoint
- `/version` endpoint
- Interactive CLI
- Dockerfile
- Docker Compose support
- Environment-based configuration
- Centralized logger
- Automated pytest test suite

### API

- `GET /`
- `GET /health`
- `GET /version`
- `POST /ask`

### Testing

- Added automated unit and integration tests for:
  - Agents
  - Retrieval
  - Verification
  - Guardrails
  - Graph workflow
  - API endpoints
  - CLI entrypoint

### Notes

This release establishes Lodestar Veritas as a production-style Agentic RAG platform for financial and regulatory document intelligence.