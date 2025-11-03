from neo4j import GraphDatabase
import json

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

def build_graph(chunks_file="data/chunks_entities.json"):
    with open(chunks_file) as f:
        chunks = json.load(f)
    with driver.session() as session:
        for c in chunks:
            ents = c.get("entities", [])
            for e in ents:
                session.run("MERGE (n:Entity {name:$e})", e=e)
            for i in range(len(ents)):
                for j in range(i+1,len(ents)):
                    session.run("""
                        MATCH (a:Entity {name:$a}), (b:Entity {name:$b})
                        MERGE (a)-[:CO_OCCURS_WITH]->(b)
                    """, a=ents[i], b=ents[j])
    print("Graph built in Neo4j")

if __name__ == "__main__":
    build_graph()
