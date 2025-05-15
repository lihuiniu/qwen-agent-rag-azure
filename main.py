from fastapi import FastAPI
from app.api import feedback, rag, retrain, metrics, vectorops

app = FastAPI()
app.include_router(feedback.router, prefix="/feedback")
app.include_router(rag.router, prefix="/rag")
app.include_router(retrain.router, prefix="/retrain")
app.include_router(metrics.router, prefix="/metrics")
app.include_router(vectorops.router, prefix="/vector")