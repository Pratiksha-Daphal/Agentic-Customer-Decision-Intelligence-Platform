from app.core.database import SessionLocal


def get_customer_features(customer_id: int):
    # placeholder for actual DB reads
    with SessionLocal() as session:
        return {"customer_id": customer_id, "features": {}}
