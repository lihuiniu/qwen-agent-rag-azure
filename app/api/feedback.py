from fastapi import APIRouter
router = APIRouter()

@router.post("/vote")
def submit_feedback(item_id: str, vote: int):
    return {"status": "received", "item": item_id, "vote": vote}