from transformers import pipeline
from app.core.embeddings import embed_text
from app.core.faiss_store import search_faiss
from app.config import GENERATION_MODEL

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = pipeline("text-generation", model=GENERATION_MODEL, device_map="auto")
    return _llm

def generate_answer(question: str):
    query_emb = embed_text(question)
    retrieved = search_faiss(query_emb, top_k=5)
    context = "\n\n".join(retrieved)
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer factually and concisely:"
    llm = get_llm()
    result = llm(prompt, max_new_tokens=100, temperature=0.2)[0]["generated_text"]
    return {"answer": result, "context": retrieved}
