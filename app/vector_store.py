from typing import Dict, List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from .models import Entity

# Simple in-memory vector store (per process)
# Good enough for a portfolio project

class VectorStore:
    def __init__(self):
        self._model = SentenceTransformer("all-MiniLM-L6-v2")
        self._embeddings: Dict[int, np.ndarray] = {}

    def add_or_update(self, entity: Entity):
        text = entity.description or f"{entity.type.value} - {entity.value}"
        embedding = self._model.encode(text)
        self._embeddings[entity.id] = embedding

    def search(self, query: str, k: int = 5) -> List[Tuple[int, float]]:
        if not self._embeddings:
            return []

        query_emb = self._model.encode(query)
        results: List[Tuple[int, float]] = []
        for entity_id, emb in self._embeddings.items():
            # cosine similarity
            denom = np.linalg.norm(emb) * np.linalg.norm(query_emb)
            if denom == 0:
                score = 0.0
            else:
                score = float(np.dot(emb, query_emb) / denom)
            results.append((entity_id, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

vector_store = VectorStore()
