import spacy, json
nlp = spacy.load("en_ner_bionlp13cg_md")

def extract_entities(chunks_file="data/chunks.json"):
    with open(chunks_file) as f:
        chunks = json.load(f)
    for c in chunks:
        doc = nlp(c["chunk"])
        c["entities"] = list({ent.text for ent in doc.ents})
    with open("data/chunks_entities.json","w") as f:
        json.dump(chunks,f)
    print("Entities extracted:", len(chunks))

if __name__ == "__main__":
    extract_entities()
