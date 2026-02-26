from langgraph.graph import StateGraph, END
from app.graph.state import DecisionState

from app.graph.nodes.feature import feature_agent
from app.graph.nodes.cltv import cltv_agent
from app.graph.nodes.insight import insight_agent
from app.graph.nodes.recommendation import recommendation_agent
from app.graph.nodes.risk import risk_agent
from app.graph.nodes.decision import decision_agent


def build_decision_graph():
    graph = StateGraph(DecisionState)

    # --- Nodes ---
    graph.add_node("feature_agent", feature_agent)
    graph.add_node("cltv_agent", cltv_agent)
    graph.add_node("insight_agent", insight_agent)
    graph.add_node("recommendation_agent", recommendation_agent)
    graph.add_node("risk_agent", risk_agent)
    graph.add_node("decision_agent", decision_agent)

    # --- Entry ---
    graph.set_entry_point("feature_agent")

    # --- Edges (explicit orchestration) ---
    graph.add_edge("feature_agent", "cltv_agent")
    graph.add_edge("cltv_agent", "insight_agent")
    graph.add_edge("insight_agent", "recommendation_agent")
    graph.add_edge("recommendation_agent", "risk_agent")
    graph.add_edge("risk_agent", "decision_agent")
    graph.add_edge("decision_agent", END)

    return graph.compile()