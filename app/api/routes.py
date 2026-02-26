from fastapi import APIRouter
from app.services.decision_service import run_decision_flow
from app.services.explaination_service import generate_natural_language_explanation
from app.models.schemas import HealthResponse, NextBestActionResponse

router = APIRouter()

@router.post("/explain-decision")
def explain_decision(decision: dict):
    return {
        "explanation": generate_natural_language_explanation(decision)
    }

@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}

@router.get(
    "/next-best-action/{customer_id}",
    response_model=NextBestActionResponse
)
def next_best_action(customer_id: int):
    return run_decision_flow(customer_id)