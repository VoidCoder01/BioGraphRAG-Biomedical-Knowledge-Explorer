import pandas as pd
import ast
import os

def load_pubmed(limit=500):
    """
    Load PubMed abstracts from local CSV file.
    The CSV format has tuples stored as strings: (['abstract text'], 'title text')
    """
    csv_path = "pubmed_abstracts.csv"
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    print(f"Reading CSV from: {csv_path}")
    
    # Read the CSV - the data columns contain string representations of tuples
    df = pd.read_csv(csv_path, encoding="utf-8")
    
    print(f"Dataset shape: {df.shape}")
    print(f"Available columns: {df.columns.tolist()[:5]}...")  # Show first 5 columns
    
    # The relevant columns appear to be topic-specific (e.g., 'deep_learning', 'covid_19', etc.)
    # Each contains tuples like: (['abstract'], 'title')
    # Let's collect all non-null entries from all topic columns
    
    data_records = []
    
    # Get all columns except the index column
    topic_columns = [col for col in df.columns if col not in ['', 'Unnamed: 0'] and not col.endswith('_links')]
    
    print(f"Processing {len(topic_columns)} topic columns...")
    
    for col in topic_columns:
        for idx, value in df[col].items():
            if pd.notna(value) and value != '[]':
                try:
                    # Parse the string representation of tuple
                    parsed = ast.literal_eval(value)
                    
                    if isinstance(parsed, tuple) and len(parsed) == 2:
                        abstract_list, title = parsed
                        
                        # Extract abstract from list
                        if isinstance(abstract_list, list) and len(abstract_list) > 0:
                            abstract = abstract_list[0]
                        else:
                            abstract = ""
                        
                        # Only add if both title and abstract exist
                        if title and abstract and len(abstract) > 50:
                            data_records.append({
                                'title': title,
                                'abstract': abstract,
                                'topic': col
                            })
                except (ValueError, SyntaxError) as e:
                    # Skip malformed entries
                    continue
    
    # Create DataFrame from collected records
    df_clean = pd.DataFrame(data_records)
    
    # Remove duplicates based on title
    df_clean = df_clean.drop_duplicates(subset=['title'], keep='first')
    
    print(f"Extracted {len(df_clean)} unique articles")
    
    # Create combined text field
    df_clean["text"] = df_clean["title"].str.strip() + ". " + df_clean["abstract"].str.strip()
    
    # Return limited number of records
    return df_clean.head(limit)

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    df = load_pubmed()
    
    # Try to save as parquet, fall back to CSV if pyarrow is not installed
    try:
        df.to_parquet("data/pubmed_sample.parquet", index=False)
        print(f"✅ Loaded and saved {len(df)} rows to data/pubmed_sample.parquet")
    except ImportError:
        df.to_csv("data/pubmed_sample.csv", index=False)
        print(f"✅ Loaded and saved {len(df)} rows to data/pubmed_sample.csv")
        print("💡 Tip: Install pyarrow for better performance: pip install pyarrow")
