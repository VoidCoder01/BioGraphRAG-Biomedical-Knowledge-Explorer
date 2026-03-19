from sentence_transformers import SentenceTransformer
import json, faiss, numpy as np, pickle

def build_index(chunks_file="data/chunks_entities.json"):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    with open(chunks_file) as f: chunks = json.load(f)
    texts = [c["chunk"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, "data/pubmed_faiss.index")
    with open("data/chunk_meta.pkl","wb") as f: pickle.dump(chunks,f)
    print("FAISS index created with", len(chunks), "chunks")

if __name__ == "__main__":
    build_index()
