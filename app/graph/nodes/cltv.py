from app.agents.cltv import estimate_cltv
from app.graph.state import DecisionState


def cltv_agent(state: DecisionState) -> DecisionState:
    cltv = estimate_cltv(state["features"])
    return {"cltv": cltv}