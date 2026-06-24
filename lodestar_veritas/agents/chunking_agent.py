from lodestar_veritas.chunking.page_aware_chunker import PageAwareChunker


class ChunkingAgent:
    """
    Uses the selected chunk strategy to chunk parsed document content.
    Preserves page/slide/paragraph/table/row metadata when available.
    """

    def __init__(self):
        self.page_aware_chunker = PageAwareChunker()

    def chunk(self, parsed_result: dict) -> list:
        strategy = parsed_result["chunk_strategy"]
        parsed_content = parsed_result["parsed_content"]

        return self.page_aware_chunker.chunk(
            parsed_content=parsed_content,
            strategy=strategy,
        )