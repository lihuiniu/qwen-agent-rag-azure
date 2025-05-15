from fastapi import APIRouter
router = APIRouter()

@router.post("/rerank")
def rerank_query(query: str, model: str = "qwen"):
    return {"reranked_answer": f"Using {model} to rerank: {query}"}