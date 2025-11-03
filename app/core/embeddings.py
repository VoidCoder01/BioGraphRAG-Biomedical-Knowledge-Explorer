from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL

_model = None

def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

def embed_text(text: str):
    model = get_embedder()
    return model.encode([text], convert_to_numpy=True)[0]
