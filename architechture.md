## 1 .High-Level Architecture:

PubMed / DrugBank / BioKG
          │
          ▼
   Entity & Relation Extraction
          │
   ┌──────┴────────┐
   │               │
Graph DB       Vector DB   
 (Neo4j)    (Chroma / FAISS)
   │               │
   └──────┬────────┘
          ▼
      RAG Pipeline
          │
          ▼
       LLM Answer
