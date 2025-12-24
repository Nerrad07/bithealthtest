import os
from dataclasses import dataclass
from .services.embedding_service import EmbeddingService
from .stores.base import DocumentStore
from .stores.memory_store import InMemoryDocumentStore
from .stores.qdrant_store import QdrantDocumentStore
from .workflow import RagWorkflow


@dataclass(frozen=True)
class AppContainer:
    embedder: EmbeddingService
    store: DocumentStore
    workflow: RagWorkflow

    @staticmethod
    def from_env() -> "AppContainer":
        use_qdrant = os.getenv("USE_QDRANT", "0") == "1"
        vector_size = int(os.getenv("VECTOR_SIZE", "8"))
        embedder = EmbeddingService(dim=vector_size)

        if use_qdrant:
            url = os.getenv("QDRANT_URL", "http://localhost:6333")
            collection = os.getenv("QDRANT_COLLECTION", "docs")
            store = QdrantDocumentStore(url=url, collection_name=collection, vector_size=vector_size)
        else:
            store = InMemoryDocumentStore()

        workflow = RagWorkflow(store=store, embedder=embedder)
        return AppContainer(embedder=embedder, store=store, workflow=workflow)
