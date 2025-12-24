from fastapi import FastAPI
from .api import make_routes
from .services.embedding import EmbeddingService
from .stores.memory_store import InMemoryDocumentStore
from .rag_workflow import RagWorkflow

app = FastAPI(title="Learning RAG Demo")

def build_store():
    try:
        from .stores.qdrant_store import QdrantDocumentStore
        return QdrantDocumentStore(
            url="http://localhost:6333",
            collection_name="demo_collection",
            vector_size=128,
        )
    except Exception:
        return InMemoryDocumentStore()

embedder = EmbeddingService()
store = build_store()
workflow = RagWorkflow(store=store, embedder=embedder)

app.include_router(make_routes(workflow))
