from app.graph.state import DecisionState
from app.agents.recommendation import generate_candidate_actions


def recommendation_agent(state: DecisionState) -> DecisionState:
    print("▶ RecommendationAgent")
    features = state["features"]
    customer_id = state.get("customer_id")

    # recommendation logic historically pulled customer_id out of features
    payload = {**features}
    if customer_id is not None:
        payload["customer_id"] = customer_id

    candidates = generate_candidate_actions(payload)
    return {"candidate_actions": candidates}