from sqlalchemy import text
from app.core.database import SessionLocal


def assess_risks(candidates: list[dict], features: dict) -> list[dict]:
    """
    Attaches risk metrics + hard_block flag to candidate actions.
    """

    if not candidates:
        return []

    session = SessionLocal()

    try:
        action_ids = tuple(c["action_id"] for c in candidates)

        query = text("""
            SELECT
                ra.action_id,
                ra.churn_risk,
                ra.fatigue_risk,
                ra.delivery_risk,
                ra.hard_block
            FROM risk_assessments ra
            WHERE ra.action_id IN :action_ids
        """)

        rows = session.execute(
            query, {"action_ids": action_ids}
        ).fetchall()

        risk_map = {
            r.action_id: {
                "churn_risk": float(r.churn_risk),
                "fatigue_risk": float(r.fatigue_risk),
                "delivery_risk": float(r.delivery_risk),
                "hard_block": r.hard_block,
            }
            for r in rows
        }

        for c in candidates:
            c["risk"] = risk_map.get(c["action_id"], {})

        return candidates

    finally:
        session.close()