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
    using_qdrant: bool

    @staticmethod
    def from_env() -> "AppContainer":
        disable_qdrant = os.getenv("DISABLE_QDRANT", "0") == "1"

        vector_size = int(os.getenv("VECTOR_SIZE", "128"))
        embedder = EmbeddingService(dim=vector_size)

        using_qdrant = False
        store: DocumentStore

        if not disable_qdrant:
            url = os.getenv("QDRANT_URL", "http://localhost:6333")
            collection = os.getenv("QDRANT_COLLECTION", "demo_collection")
            try:
                store = QdrantDocumentStore(url=url, collection_name=collection, vector_size=vector_size)
                using_qdrant = True
            except Exception:
                store = InMemoryDocumentStore()
        else:
            store = InMemoryDocumentStore()

        workflow = RagWorkflow(store=store, embedder=embedder)
        return AppContainer(embedder=embedder, store=store, workflow=workflow, using_qdrant=using_qdrant)
