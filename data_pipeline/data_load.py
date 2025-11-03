from kagglehub import load_dataset, KaggleDatasetAdapter
import pandas as pd

def load_pubmed(limit=500):
    df = load_dataset(KaggleDatasetAdapter.PANDAS, "bonhart/pubmed-abstracts")
    df = df[["title", "abstract"]].dropna()
    df["text"] = df["title"] + ". " + df["abstract"]
    return df.head(limit)

if __name__ == "__main__":
    df = load_pubmed()
    df.to_parquet("data/pubmed_sample.parquet", index=False)
