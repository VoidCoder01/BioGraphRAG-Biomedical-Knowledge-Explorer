import json
from transformers import pipeline

# Use BioBERT for biomedical NER - automatically downloads model
print("Loading BioBERT NER model...")
ner_pipeline = pipeline("ner", model="d4data/biomedical-ner-all", aggregation_strategy="simple")

def extract_entities(chunks_file="E:\\Anushka\\BioGraphRAG-Biomedical-Knowledge-Explorer\\data\\chunks.json"):
    with open(chunks_file) as f:
        chunks = json.load(f)
    
    print(f"Extracting entities from {len(chunks)} chunks...")
    
    for idx, c in enumerate(chunks):
        if idx % 100 == 0:
            print(f"Processing chunk {idx}/{len(chunks)}...")
        
        # Extract entities using BioBERT
        try:
            entities = ner_pipeline(c["chunk"][:512])  # Limit to 512 tokens
            # Extract unique entity texts
            c["entities"] = list({ent["word"].strip() for ent in entities if ent["score"] > 0.5})
        except Exception as e:
            print(f"Error processing chunk {idx}: {e}")
            c["entities"] = []
    
    with open("E:\\Anushka\\BioGraphRAG-Biomedical-Knowledge-Explorer\\data\\chunks_entities.json", "w") as f:
        json.dump(chunks, f, indent=2)
    
    total_entities = sum(len(c["entities"]) for c in chunks)
    print(f"✅ Entities extracted: {len(chunks)} chunks, {total_entities} total entities")

if __name__ == "__main__":
    extract_entities()
