from app.graph.state import DecisionState
from app.agents.decision import choose_best_action


def decision_agent(state: DecisionState) -> DecisionState:
    state["final_decision"] = choose_best_action(
        customer_id=state["customer_id"],
        candidates=state["candidate_actions"],
        features=state["features"],
        cltv=state["cltv"],
        insights=state.get("insights"),
    )
    return state