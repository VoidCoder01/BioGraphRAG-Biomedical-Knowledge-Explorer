from neo4j import GraphDatabase
from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

_driver = None

def get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return _driver

def get_entity_connections(entity: str):
    query = """
    MATCH (a:Entity {name:$entity})-[r:CO_OCCURS_WITH]-(b)
    RETURN a.name AS source, b.name AS target LIMIT 25
    """
    driver = get_driver()
    with driver.session() as session:
        results = session.run(query, entity=entity)
        edges = [{"source": r["source"], "target": r["target"]} for r in results]
    return edges
