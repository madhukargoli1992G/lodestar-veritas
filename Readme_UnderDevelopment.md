# Lodestar Veritas

## Agentic Multimodal RAG Platform for Financial & Regulatory Intelligence

Lodestar Veritas is an enterprise-style Agentic AI platform designed to process large-scale financial and regulatory documents with high accuracy while minimizing hallucinations.

Unlike traditional RAG systems, Lodestar Veritas intelligently detects document types, applies adaptive chunking strategies, performs hybrid retrieval, reranks evidence, validates generated answers, and enforces guardrails before presenting responses.

---

## Features

- ✅ Agentic AI using LangGraph
- ✅ Adaptive Document Type Detection
- ✅ TOC-aware Metadata Chunking
- ✅ Hierarchical Chunking
- ✅ Table-aware Chunking
- ✅ Image-aware Chunking
- ✅ Hybrid Retrieval
    - Dense Semantic Search
    - BM25 Keyword Search
    - Reciprocal Rank Fusion (RRF)
- ✅ Cross Encoder Reranking
- ✅ Answer Verification
- ✅ Validation Loops
- ✅ Hallucination Guardrails
- ✅ Citation-based Answers
- ✅ Local LLMs using Ollama
- ✅ Local Vector Database (Qdrant)

---

## Supported Documents

- PDF
- Word (.docx)
- CSV
- PowerPoint (.pptx)
- Images

---

## Tech Stack

- Python
- LangGraph
- LangChain
- Ollama
- Qdrant
- Sentence Transformers
- BGE Reranker
- FastAPI
- Streamlit

---

## Architecture

Document Upload

↓

Document Detection Agent

↓

Parser Agent

↓

Adaptive Chunking Agent

↓

Embedding Agent

↓

Qdrant Vector Store

↓

Hybrid Retrieval

↓

RRF Fusion

↓

Cross Encoder Reranking

↓

Answer Generation

↓

Answer Verification

↓

Guardrails

↓

Final Response

---

## Current Status

🚧 Under Development

---

## Author

Madhukar Goli - AI Engineer(GEN AI & Agentic AI)