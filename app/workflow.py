from .services.embedding_service import EmbeddingService
from .stores.base import DocumentStore

class RagWorkflow:
    def __init__(self, store: DocumentStore, embedder: EmbeddingService):
        self.store = store
        self.embedder = embedder

    def add(self, text: str) -> int:
        vector = self.embedder.embed(text)
        return self.store.add(text=text, vector=vector)

    def ask(self, question: str) -> dict:
        qvec = self.embedder.embed(question)
        hits = self.store.search(query_text=question, query_vector=qvec, limit=2)
        context = "\n\n".join(hits) if hits else ""
        return {"question": question, "context": context, "hits": hits}

    def count(self) -> int:
        return self.store.count()

    def is_ready(self) -> bool:
        return self.store.is_ready()
