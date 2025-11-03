from fastapi import APIRouter, Query
from app.core.graph_db import get_entity_connections

router = APIRouter(prefix="/graph", tags=["Graph"])

@router.get("/")
def graph_endpoint(entity: str = Query(...)):
    return {"edges": get_entity_connections(entity)}
