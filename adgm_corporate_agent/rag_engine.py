import os
from typing import List, Tuple

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    import faiss
    _HAS_FAISS = True
except Exception:
    _HAS_FAISS = False

class RAGEngine:
    def __init__(self, ref_dir="legal_refs", model_name="all-MiniLM-L6-v2"):
        self.ref_dir = ref_dir
        self.chunks = []
        self.sources = []
        if _HAS_FAISS:
            self.model = SentenceTransformer(model_name)
            self._load_and_index(ref_dir)
        else:
            self._load_raw(ref_dir)

    def _load_raw(self, ref_dir):
        self.raw_texts = {}
        for fname in os.listdir(ref_dir):
            if fname.endswith(".txt") or fname.endswith(".md"):
                path = os.path.join(ref_dir, fname)
                with open(path, "r", encoding="utf-8") as f:
                    self.raw_texts[fname] = f.read()

    def _chunk_text(self, text: str, chunk_size=400, overlap=50):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks

    def _load_and_index(self, ref_dir):
        for fname in os.listdir(ref_dir):
            if fname.endswith(".txt") or fname.endswith(".md"):
                path = os.path.join(ref_dir, fname)
                with open(path, "r", encoding="utf-8") as f:
                    t = f.read()
                cks = self._chunk_text(t)
                for c in cks:
                    self.chunks.append(c)
                    self.sources.append(fname)
        if not self.chunks:
            return
        embeddings = self.model.encode(self.chunks, show_progress_bar=False)
        self._embeddings = embeddings.astype("float32")
        self.index = faiss.IndexFlatL2(self._embeddings.shape[1])
        self.index.add(self._embeddings)

    def retrieve(self, query: str, top_k=2) -> List[Tuple[str, str, float]]:
        if not query or not query.strip():
            return []
        if _HAS_FAISS and hasattr(self, "index"):
            q_emb = self.model.encode([query]).astype("float32")
            D, I = self.index.search(q_emb, top_k)
            results = []
            for dist, idx in zip(D[0], I[0]):
                if idx < len(self.chunks):
                    results.append((self.chunks[idx], self.sources[idx], float(dist)))
            return results
        else:
            results = []
            query_words = [w.lower() for w in query.split()]
            for fname, txt in self.raw_texts.items():
                txt_lower = txt.lower()
                if all(word in txt_lower for word in query_words):
                    idx = min(txt_lower.index(word) for word in query_words if word in txt_lower)
                    start = max(0, idx - 200)
                    end = min(len(txt), idx + 400)
                    snippet = txt[start:end].replace("\n", " ").strip()
                    results.append((snippet, fname, 0.0))
            return results[:top_k]

    def get_citation(self, query: str):
        results = self.retrieve(query, top_k=1)
        if results:
            snippet, source, _ = results[0]
            return {"citation": snippet, "citation_rule": source}
        return None
