from neo4j import GraphDatabase
import json
import os
from collections import defaultdict

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def build_graph(chunks_file=None, use_neo4j=False):
    if chunks_file is None:
        chunks_file = os.path.join(project_root, "data", "chunks_entities.json")
    
    with open(chunks_file) as f:
        chunks = json.load(f)
    
    if use_neo4j:
        # Neo4j version (requires Neo4j running)
        try:
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
            with driver.session() as session:
                print("Building graph in Neo4j...")
                for idx, c in enumerate(chunks):
                    if idx % 100 == 0:
                        print(f"Processing chunk {idx}/{len(chunks)}...")
                    ents = c.get("entities", [])
                    for e in ents:
                        session.run("MERGE (n:Entity {name:$e})", e=e)
                    for i in range(len(ents)):
                        for j in range(i+1,len(ents)):
                            session.run("""
                                MATCH (a:Entity {name:$a}), (b:Entity {name:$b})
                                MERGE (a)-[:CO_OCCURS_WITH]->(b)
                            """, a=ents[i], b=ents[j])
            driver.close()
            print("✅ Graph built in Neo4j")
        except Exception as e:
            print(f"❌ Neo4j connection failed: {e}")
            print("Falling back to JSON graph format...")
            use_neo4j = False
    
    if not use_neo4j:
        # JSON/NetworkX version (no Neo4j required)
        print("Building graph as JSON (Neo4j not available)...")
        entities = set()
        relationships = defaultdict(int)
        
        for idx, c in enumerate(chunks):
            if idx % 100 == 0:
                print(f"Processing chunk {idx}/{len(chunks)}...")
            ents = c.get("entities", [])
            entities.update(ents)
            
            # Create co-occurrence relationships
            for i in range(len(ents)):
                for j in range(i+1, len(ents)):
                    pair = tuple(sorted([ents[i], ents[j]]))
                    relationships[pair] += 1
        
        # Save graph as JSON
        graph_data = {
            "nodes": [{"id": e, "label": "Entity"} for e in entities],
            "edges": [
                {
                    "source": pair[0],
                    "target": pair[1],
                    "weight": count,
                    "type": "CO_OCCURS_WITH"
                }
                for pair, count in relationships.items()
            ]
        }
        
        output_file = os.path.join(project_root, "data", "knowledge_graph.json")
        with open(output_file, "w") as f:
            json.dump(graph_data, f, indent=2)
        
        print(f"✅ Graph built: {len(entities)} entities, {len(relationships)} relationships")
        print(f"   Saved to: {output_file}")

if __name__ == "__main__":
    build_graph()
