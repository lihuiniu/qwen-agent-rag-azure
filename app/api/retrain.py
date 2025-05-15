from fastapi import APIRouter
router = APIRouter()

@router.post("/trigger")
def trigger_retrain(model: str):
    return {"message": f"Retraining model: {model}"}