from .base import DocumentStore

class InMemoryDocumentStore(DocumentStore):
    def __init__(self):
        self._docs: list[str] = []

    def add(self, text: str, vector: list[float]) -> int:
        doc_id = len(self._docs)
        self._docs.append(text)
        return doc_id

    def search(self, query_text: str, query_vector: list[float], limit: int = 2) -> list[str]:
        q = query_text.lower()
        results = []
        seen = set()

        for doc in self._docs:
            if q in doc.lower() and doc not in seen:
                results.append(doc)
                seen.add(doc)
                if len(results) >= limit:
                    return results

        if not results and self._docs:
            return [self._docs[0]]

        return results


    def count(self) -> int:
        return len(self._docs)

    def is_ready(self) -> bool:
        return True
