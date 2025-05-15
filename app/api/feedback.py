from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

feedback_router = APIRouter()

class Feedback(BaseModel):
    user_id: str
    query: str
    answer: str
    vote: str = Field(..., regex ="^(up|down)$")
    rating: Optional[int] = Field(None, ge=1, le=5, description="User rating from 1 to 5")
    comment: Optional[str] = Field(None, max_length=1000)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
@feedback_router.post("/")
def submit_feedback(feedback: Feedback):
    # In production, save to a DB or event bus for downstream retraining and monitoring
    print("Received Feedback: ", feedback.dict())
    return {"message": "Feedback submitted successfully"}