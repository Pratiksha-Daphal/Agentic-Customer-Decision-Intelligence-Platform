from datetime import datetime
from typing import List, Dict, Any

MIN_UTILITY_THRESHOLD = 0.05  # business safety threshold


def choose_best_action(
    customer_id: int,
    candidates: List[Dict[str, Any]],
    features: Dict[str, Any],
    cltv: Dict[str, Any],
    insights: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:

    best_action = None
    best_utility = -1.0

    cltv_score = cltv.get("cltv_score", 0.0)
    cltv_weight = 0.5 + cltv_score

    for c in candidates:
        risk = c.get("risk", {})

        if risk.get("hard_block", False):
            continue

        base_score = c.get("score", 0.0)

        utility = (
            base_score
            * (1 - risk.get("churn_risk", 0.0))
            * (1 - risk.get("fatigue_risk", 0.0))
            * (1 - risk.get("delivery_risk", 0.0))
            * cltv_weight
        )

        if utility > best_utility:
            best_utility = utility
            best_action = {
                "customer_id": customer_id,
                "action": c["action_type"],
                "expected_utility": round(utility, 4),
                "explanation": {
                    "base_score": base_score,
                    "cltv_score": round(cltv_score, 3),
                    "cltv_weight": round(cltv_weight, 3),
                    "churn_risk": risk.get("churn_risk"),
                    "fatigue_risk": risk.get("fatigue_risk"),
                    "delivery_risk": risk.get("delivery_risk"),
                    "hard_block": False,
                    "decision_rule": "MAX_UTILITY_WITH_THRESHOLD",
                    "min_utility_threshold": MIN_UTILITY_THRESHOLD,
                    "similar_cases": insights or [],
                },
                "decided_at": datetime.utcnow(),
            }

    # 🔒 Threshold enforcement
    if not best_action or best_utility < MIN_UTILITY_THRESHOLD:
        return {
            "customer_id": customer_id,
            "action": "NO_ACTION",
            "reason": "Expected utility below minimum threshold",
            "expected_utility": round(best_utility, 4),
            "explanation": {
                "decision_rule": "UTILITY_THRESHOLD",
                "min_utility_threshold": MIN_UTILITY_THRESHOLD,
                "similar_cases": insights or [],
            },
            "decided_at": datetime.utcnow(),
        }

    return best_action