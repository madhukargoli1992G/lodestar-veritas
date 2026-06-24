from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentChunk:
    chunk_id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)