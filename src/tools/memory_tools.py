import math
from typing import Dict, Any, List, Tuple

class MemoryBank:
    def __init__(self, dim: int = 128):
        self._store = {}   # id -> {"text","meta","vec"}
        self.dim = dim

    def _embed(self, text: str):
        vec = [0.0] * self.dim
        for ch in text:
            vec[ord(ch) % self.dim] += 1.0
        norm = math.sqrt(sum(x*x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def upsert(self, key: str, text: str, meta: Dict[str, Any]):
        self._store[key] = {"text": text, "meta": meta, "vec": self._embed(text)}

    def query(self, text: str, top_k: int = 5) -> List[Tuple[str, float, Dict[str, Any]]]:
        q = self._embed(text)
        def dot(a,b): return sum(x*y for x,y in zip(a,b))
        scored = [(k, dot(q,v["vec"]), v["meta"]) for k,v in self._store.items()]
        scored.sort(key=lambda t: t[1], reverse=True)
        return scored[:top_k]

# singleton instance for demo
memory_bank = MemoryBank()
