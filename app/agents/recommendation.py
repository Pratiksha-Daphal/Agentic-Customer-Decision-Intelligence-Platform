from sqlalchemy import text
from app.core.database import SessionLocal


def generate_candidate_actions(features: dict) -> list[dict]:
    """
    Returns candidate actions for a customer.
    Thin wrapper over recommendation SQL logic.
    """

    # `customer_id` may be passed in features or provided separately
    customer_id = features.get("customer_id")
    session = SessionLocal()

    try:
        query = text("""
            SELECT
                action_id,
                action_type,
                score
            FROM candidate_actions
            WHERE customer_id = :customer_id
        """)

        rows = session.execute(
            query, {"customer_id": customer_id}
        ).fetchall()

        return [
            {
                "action_id": r.action_id,
                "action_type": r.action_type,
                "score": float(r.score),
            }
            for r in rows
        ]

    finally:
        session.close()