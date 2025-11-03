import faiss, pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Load FAISS + metadata
index = faiss.read_index("data/pubmed_faiss.index")
with open("data/chunk_meta.pkl", "rb") as f:
    chunks = pickle.load(f)

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Mistral-7B-v0.1 is a large model that is not available on the local machine, so we use the Microsoft Phi-2 model instead.
# qa_model = pipeline("text-generation", model="mistralai/Mistral-7B-v0.1", device_map="auto")
qa_model = pipeline("text-generation", model="microsoft/phi-2", torch_dtype="auto")

def retrieve(query, top_k=5):
    q_emb = embedder.encode([query])
    D, I = index.search(q_emb, top_k)
    return [chunks[i]["chunk"] for i in I[0]]

def answer_query(query):
    context = "\n\n".join(retrieve(query))
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer briefly and factually:"
    out = qa_model(prompt, max_new_tokens=100, temperature=0.2)
    return out[0]["generated_text"]

if __name__ == "__main__":
    q = "Which drugs are used to treat Alzheimer's disease?"
    print(answer_query(q))
