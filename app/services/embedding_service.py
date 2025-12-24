import random
from typing import List

class EmbeddingService:
    def __init__(self, dim: int = 128):
        self.dim = dim

    def embed(self, text: str) -> List[float]:
        seed = abs(hash(text)) % 10000
        rng = random.Random(seed)
        return [rng.random() for _ in range(self.dim)]
