from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from fastapi import Request
from fastapi.responses import JSONResponse
from scripts.langchain_eval_runner import evaluate_batch

# Simulated cache to store evaluation pass/fail
EVAL_GATE = {}

eval_router = APIRouter()

class EvalItem(BaseModel):
    query: str
    prediction: str
    expected: str


@eval_router.post("/batch")
def evaluate(eval_data: List[EvalItem]):
    examples = [{"query": e.query, "expected": e.expected} for e in eval_data]
    predictions = [{"result": e.prediction} for e in eval_data]
    results = evaluate_batch(examples, predictions)
    return {"eval_results": results}

@eval_router.post("/gatekeeper/{agent_version}")
def check_eval_gate(agent_version: str, eval_data: List[EvalItem]):
    examples = [{"query": e.query, "expected": e.expected} for e in eval_data]
    predictions = [{"result": e.prediction} for e in eval_data]
    results = evaluate_batch(examples, predictions)
    # Example threshold logic: 0.7
    passes = [r.get("score", 0) >= 0.7 for r in results]
    all_passed = all(passes)
    EVAL_GATE[agent_version] = all_passed
    return {
    "agent_version": agent_version,
    "passed": all_passed,
    "details": results
    }
@eval_router.get("/gatekeeper/{agent_version}/status")
def get_eval_gate_status(agent_version: str):
    status = EVAL_GATE.get(agent_version, False)
    return {"agent_version": agent_version, "passed": status}