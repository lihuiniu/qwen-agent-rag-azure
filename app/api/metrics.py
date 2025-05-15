from fastapi import APIRouter
router = APIRouter()

@router.get("/online")
def online_metrics():
    return {"engagement_score": 0.92}

@router.get("/offline")
def offline_metrics():
    return {"precision@5": 0.85, "factuality": 0.9}