from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from .base import DocumentStore

class QdrantDocumentStore(DocumentStore):
    def __init__(self, url: str, collection_name: str, vector_size: int):
        self.collection_name = collection_name
        self.vector_size = vector_size
        self._client = QdrantClient(url)
        self._id_counter = 0

        self._client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
        )

    def add(self, text: str, vector: list[float]) -> int:
        doc_id = self._id_counter
        self._id_counter += 1

        self._client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(id=doc_id, vector=vector, payload={"text": text})],
        )
        return doc_id

    def search(self, query_text: str, query_vector: list[float], limit: int = 2) -> list[str]:
        hits = self._client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
        )
        return [hit.payload["text"] for hit in hits if hit.payload]

    def count(self) -> int:
        return self._id_counter

    def is_ready(self) -> bool:
        return True
