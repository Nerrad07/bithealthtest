import hashlib
import random
from typing import List

class EmbeddingService:
    def __init__(self, dim: int = 8):
        self.dim = dim

    def embed(self, text: str) -> List[float]:
        seed_bytes = hashlib.sha256(text.encode("utf-8")).digest()[:8]
        seed = int.from_bytes(seed_bytes, "little", signed=False)
        rng = random.Random(seed)
        return [rng.random() for _ in range(self.dim)]
