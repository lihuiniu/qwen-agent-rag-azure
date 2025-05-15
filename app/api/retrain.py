from fastapi import APIRouter
import subprocess

router = APIRouter()

@router.post("/trigger")
def trigger_retrain(model: str):
    return {"message": f"Retraining model: {model}"}
    

@retrain_router.post("/")
def trigger_retraining():
    result = subprocess.run(["python", "scripts/azure/trigger_aml_job.py"], capture_output=True, text=True)
    return {"output": result.stdout}