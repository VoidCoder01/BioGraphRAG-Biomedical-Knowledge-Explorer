import faiss, pickle, numpy as np
from app.config import FAISS_INDEX_PATH, CHUNK_META_PATH

_index = None
_chunks = None

def load_faiss():
    global _index, _chunks
    if _index is None:
        _index = faiss.read_index(FAISS_INDEX_PATH)
    if _chunks is None:
        with open(CHUNK_META_PATH, "rb") as f:
            _chunks = pickle.load(f)
    return _index, _chunks

def search_faiss(query_emb, top_k=5):
    index, chunks = load_faiss()
    D, I = index.search(np.array([query_emb]), top_k)
    return [chunks[i]["chunk"] for i in I[0]]
