from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

def clear_graph():
    with driver.session() as s:
        s.run("MATCH (n) DETACH DELETE n")
    print("Graph cleared")

if __name__ == "__main__":
    clear_graph()
