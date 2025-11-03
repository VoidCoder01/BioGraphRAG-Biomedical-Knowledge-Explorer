from fastapi import APIRouter, Query
from app.core.rag_engine import generate_answer

router = APIRouter(prefix="/ask", tags=["Ask"])

@router.get("/")
def ask_endpoint(question: str = Query(...)):
    return generate_answer(question)
