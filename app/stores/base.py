from abc import ABC, abstractmethod

class DocumentStore(ABC):
    @abstractmethod
    def add(self, text: str, vector: list[float]) -> int:
        raise NotImplementedError

    @abstractmethod
    def search(self, query_text: str, query_vector: list[float], limit: int = 2) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def is_ready(self) -> bool:
        raise NotImplementedError
