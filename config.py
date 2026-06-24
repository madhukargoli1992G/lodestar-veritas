"""
Global configuration for Lodestar Veritas.

Supports environment-variable overrides for production, Docker, and local development.
"""

import os
from pathlib import Path


def get_env_str(name: str, default: str) -> str:
    return os.getenv(name, default)


def get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)

    if value is None:
        return default

    return int(value)


def get_env_float(name: str, default: float) -> float:
    value = os.getenv(name)

    if value is None:
        return default

    return float(value)


###########################################################
# Project Directories
###########################################################

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
IMAGE_DIR = DATA_DIR / "images"
INDEX_DIR = DATA_DIR / "indexes"
LOG_DIR = PROJECT_ROOT / "logs"

###########################################################
# Ollama Models
###########################################################

TEXT_MODEL = get_env_str("TEXT_MODEL", "qwen2.5:3b")
VISION_MODEL = get_env_str("VISION_MODEL", "qwen2.5vl:3b")

OLLAMA_MODEL = get_env_str("OLLAMA_MODEL", TEXT_MODEL)
OLLAMA_URL = get_env_str("OLLAMA_URL", "http://localhost:11434")

###########################################################
# Embeddings
###########################################################

EMBEDDING_MODEL = get_env_str(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

EMBEDDING_DIMENSION = get_env_int("EMBEDDING_DIMENSION", 384)

###########################################################
# Retrieval
###########################################################

VECTOR_DB = get_env_str("VECTOR_DB", "qdrant")
COLLECTION_NAME = get_env_str("COLLECTION_NAME", "lodestar_veritas")

TOP_K_VECTOR = get_env_int("TOP_K_VECTOR", 15)
TOP_K_BM25 = get_env_int("TOP_K_BM25", 15)
TOP_K_RRF = get_env_int("TOP_K_RRF", 10)
TOP_K_RERANK = get_env_int("TOP_K_RERANK", 5)

DEFAULT_TOP_K = get_env_int("DEFAULT_TOP_K", 5)

###########################################################
# Chunking
###########################################################

DEFAULT_CHUNK_SIZE = get_env_int("DEFAULT_CHUNK_SIZE", 900)
DEFAULT_CHUNK_OVERLAP = get_env_int("DEFAULT_CHUNK_OVERLAP", 150)

###########################################################
# Verification
###########################################################

MIN_CONFIDENCE_SCORE = get_env_float("MIN_CONFIDENCE_SCORE", 0.70)
MAX_VERIFICATION_ATTEMPTS = get_env_int("MAX_VERIFICATION_ATTEMPTS", 2)
MAX_RETRIES = get_env_int("MAX_RETRIES", 2)

###########################################################
# API
###########################################################

API_HOST = get_env_str("API_HOST", "0.0.0.0")
API_PORT = get_env_int("API_PORT", 8000)

QDRANT_URL = get_env_str("QDRANT_URL", "http://localhost:6333")

###########################################################
# Logging
###########################################################

LOG_LEVEL = get_env_str("LOG_LEVEL", "INFO")