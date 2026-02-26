from sqlalchemy import text
from app.core.database import SessionLocal
from app.graph.graph import build_decision_graph

graph = build_decision_graph()


def run_decision_flow(customer_id: int):
    initial_state = {
        "customer_id": customer_id,
        "features": None,
        "candidate_actions": None,
        "risk_assessment": None,
        "final_decision": None,
    }

    result = graph.invoke(initial_state)
    return result["final_decision"]

# def get_next_best_action(customer_id: int):
#     session = SessionLocal()
#     try:
#         query = text("""
#             SELECT
#                 d.decision_id,
#                 ca.action_type,
#                 d.expected_utility,
#                 d.explanation,
#                 d.decided_at
#             FROM decisions d
#             JOIN candidate_actions ca
#               ON d.chosen_action = ca.action_id
#             WHERE d.customer_id = :customer_id
#             ORDER BY d.decided_at DESC
#             LIMIT 1
#         """)
#         result = session.execute(query, {"customer_id": customer_id}).fetchone()

#         if not result:
#             return {
#                 "customer_id": customer_id,
#                 "action": "NO_ACTION",
#                 "reason": "No decision found"
#             }

#         return {
#             "customer_id": customer_id,
#             "action": result.action_type,
#             "expected_utility": float(result.expected_utility),
#             "explanation": result.explanation,
#             "decided_at": result.decided_at.isoformat()
#         }

#     finally:
#         session.close()