from lodestar_veritas.chunking.chunk_models import DocumentChunk
from lodestar_veritas.metadata.metadata_builder import MetadataBuilder


class MetadataAgent:
    """
    Adds richer metadata to each document chunk.
    """

    def __init__(self):
        self.metadata_builder = MetadataBuilder()

    def enrich_chunks(self, chunks: list[DocumentChunk]) -> list[DocumentChunk]:
        enriched_chunks = []

        for chunk in chunks:
            enriched_metadata = self.metadata_builder.enrich(
                text=chunk.text,
                metadata=chunk.metadata,
            )

            enriched_chunks.append(
                DocumentChunk(
                    chunk_id=chunk.chunk_id,
                    text=chunk.text,
                    metadata=enriched_metadata,
                )
            )

        return enriched_chunks