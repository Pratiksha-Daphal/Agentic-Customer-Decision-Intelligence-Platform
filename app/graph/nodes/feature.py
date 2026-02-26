from app.features.snapshot_service import get_customer_features
from app.graph.state import DecisionState


def feature_agent(state: DecisionState) -> DecisionState:
    print("▶ FeatureAgent")
    
    customer_id = state["customer_id"]

    features = get_customer_features(customer_id)
    # Normalize: some implementations return {"customer_id": id, "features": {...}}
    raw = features.get("features", features) if isinstance(features, dict) else {}

    # Ensure required keys exist with safe defaults
    required = [
        "total_orders",
        "total_spend",
        "avg_order_value",
        "customer_tenure_days",
        "orders_last_30d",
        "days_since_last_order",
        "category_diversity",
        "delivery_risk",
    ]

    normalized = {k: raw.get(k, 0.0) for k in required}

    # features should only contain actual numeric/derived values
    # instead of returning the entire state (which duplicates customer_id and
    # causes langgraph to treat it as a multi-update), return only the new
    # key/value pair that this node is responsible for.
    return {"features": normalized}