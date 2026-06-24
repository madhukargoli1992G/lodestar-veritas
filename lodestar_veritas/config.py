from dataclasses import dataclass


@dataclass
class AppConfig:
    app_name: str = "Lodestar Veritas"
    embedding_dimensions: int = 384
    default_top_k: int = 5
    chunk_size: int = 700
    chunk_overlap: int = 100
    vector_store_type: str = "in_memory"
    retrieval_mode: str = "hybrid"
    llm_provider: str = "placeholder"


def get_config() -> AppConfig:
    return AppConfig()