try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd, json

def chunk_text(df_path):
    df = pd.read_csv(df_path)
    texts = df["text"].tolist()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = [{"doc_id": i, "chunk": c} for i, t in enumerate(texts) for c in splitter.split_text(t)]
    with open("data/chunks.json","w") as f: json.dump(chunks, f)
    print("Chunks:", len(chunks))

if __name__ == "__main__":
    chunk_text("data/pubmed_sample.csv")
    