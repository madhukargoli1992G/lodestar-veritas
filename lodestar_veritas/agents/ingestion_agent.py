from lodestar_veritas.agents.parsing_agent import ParsingAgent
from lodestar_veritas.agents.chunking_agent import ChunkingAgent
from lodestar_veritas.agents.metadata_agent import MetadataAgent
from lodestar_veritas.agents.embedding_agent import EmbeddingAgent


class IngestionAgent:
    """
    Full ingestion pipeline:

    file path
        -> content analysis
        -> chunk strategy planning
        -> parsing
        -> chunking
        -> metadata enrichment
        -> embedding
    """

    def __init__(self):
        self.parsing_agent = ParsingAgent()
        self.chunking_agent = ChunkingAgent()
        self.metadata_agent = MetadataAgent()
        self.embedding_agent = EmbeddingAgent()

    def ingest(self, file_path: str) -> dict:
        parsed_result = self.parsing_agent.parse(file_path)

        chunks = self.chunking_agent.chunk(parsed_result)
        enriched_chunks = self.metadata_agent.enrich_chunks(chunks)
        embedded_chunks = self.embedding_agent.embed_chunks(enriched_chunks)

        return {
            "file_path": file_path,
            "analysis": parsed_result["analysis"],
            "chunk_strategy": parsed_result["chunk_strategy"],
            "parsed_content": parsed_result["parsed_content"],
            "chunks": enriched_chunks,
            "chunk_count": len(enriched_chunks),
            "embedded_chunks": embedded_chunks,
            "embedded_chunk_count": len(embedded_chunks),
        }