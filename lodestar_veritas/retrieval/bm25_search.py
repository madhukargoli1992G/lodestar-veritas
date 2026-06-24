import math
import re
from collections import Counter


class BM25Search:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents = []
        self.doc_tokens = []
        self.doc_freqs = Counter()
        self.avg_doc_len = 0.0

    def add_documents(self, documents: list[dict]) -> None:
        self.documents = documents
        self.doc_tokens = [self._tokenize(doc["text"]) for doc in documents]

        self.doc_freqs = Counter()
        for tokens in self.doc_tokens:
            for token in set(tokens):
                self.doc_freqs[token] += 1

        total_length = sum(len(tokens) for tokens in self.doc_tokens)
        self.avg_doc_len = total_length / len(self.doc_tokens) if self.doc_tokens else 0.0

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        query_tokens = self._tokenize(query)
        results = []

        for index, document in enumerate(self.documents):
            score = self._score(query_tokens, self.doc_tokens[index])

            results.append(
                {
                    **document,
                    "score": score,
                    "retrieval_method": "bm25",
                }
            )

        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:top_k]

    def _score(self, query_tokens: list[str], doc_tokens: list[str]) -> float:
        if not doc_tokens or self.avg_doc_len == 0:
            return 0.0

        score = 0.0
        token_counts = Counter(doc_tokens)
        doc_len = len(doc_tokens)
        total_docs = len(self.documents)

        for token in query_tokens:
            if token not in token_counts:
                continue

            doc_freq = self.doc_freqs.get(token, 0)
            idf = math.log(1 + (total_docs - doc_freq + 0.5) / (doc_freq + 0.5))

            tf = token_counts[token]
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (
                1 - self.b + self.b * doc_len / self.avg_doc_len
            )

            score += idf * numerator / denominator

        return score

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r"\b\w+\b", text.lower())