from fastapi import APIRouter, Query
from app.core.graph_db import get_driver

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search_entities(q: str = Query(...)):
    driver = get_driver()
    query = """
    MATCH (e:Entity)
    WHERE toLower(e.name) CONTAINS toLower($q)
    RETURN e.name AS name LIMIT 10
    """
    with driver.session() as session:
        res = session.run(query, q=q)
        return [r["name"] for r in res]
