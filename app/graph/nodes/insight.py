from app.graph.state import DecisionState
from app.rag.retriever import retrieve_insights


def insight_agent(state: DecisionState) -> DecisionState:
    features = state["features"]
    cltv = state["cltv"]

    # Build a context query using available signals ONLY
    query = (
        f"Customer with "
        f"total_orders {features.get('total_orders')}, "
        f"avg_order_value {features.get('avg_order_value')}, "
        f"orders_last_30d {features.get('orders_last_30d')}, "
        f"recency_days {features.get('days_since_last_order')}, "
        f"CLTV score {cltv.get('cltv_score')}"
    )

    insights = retrieve_insights(query)

    state["insights"] = insights
    return state