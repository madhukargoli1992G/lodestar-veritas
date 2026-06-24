class PromptBuilder:
    """
    Builds grounded RAG prompts for local LLM answer generation.
    """

    def build_answer_prompt(
        self,
        query: str,
        retrieved_chunks: list[dict],
        max_context_chars: int = 6000,
    ) -> str:
        context_blocks = []

        for index, chunk in enumerate(retrieved_chunks, start=1):
            metadata = chunk.get("metadata", {})

            source = metadata.get("file_name") or metadata.get("source", "unknown")
            page = metadata.get("page_number")
            slide = metadata.get("slide_number")
            row = metadata.get("row_number")

            location_parts = []

            if page is not None:
                location_parts.append(f"page {page}")

            if slide is not None:
                location_parts.append(f"slide {slide}")

            if row is not None:
                location_parts.append(f"row {row}")

            location = ", ".join(location_parts) if location_parts else "uploaded document"

            context_blocks.append(
                f"[{index}] Source: {source} | {location}\n"
                f"{chunk.get('text', '')}"
            )

        context = "\n\n".join(context_blocks)
        context = context[:max_context_chars]

        return f"""
You are Lodestar Veritas, a careful document analysis assistant.

Use ONLY the document context below to answer the user.

Important:
- The document context is valid evidence.
- If the context directly contains the answer, answer using it.
- Cite the source using bracket citations like [1].
- Do not say there is not enough evidence when the answer is clearly present in the context.
- Be concise and professional.

User question:
{query}

Document context:
{context}

Answer:
""".strip()