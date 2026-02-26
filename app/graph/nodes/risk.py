from app.graph.state import DecisionState
from app.agents.risk import assess_risks


def risk_agent(state: DecisionState) -> DecisionState:
    print("▶ RiskAgent")
    
    candidates = state["candidate_actions"]
    features = state["features"]

    risks = assess_risks(candidates, features)
    return {"risk_assessment": risks}