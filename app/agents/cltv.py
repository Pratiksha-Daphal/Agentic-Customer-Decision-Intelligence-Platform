import torch
import numpy as np
from cltv.model import CLTVModel

MODEL_PATH = "cltv_model.pt"

model = CLTVModel(input_dim=8)
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()


def estimate_cltv(features: dict) -> dict:
    x = np.array([
        features["total_orders"],
        features["total_spend"],
        features["avg_order_value"],
        features["customer_tenure_days"],
        features["orders_last_30d"],
        features["days_since_last_order"],
        features["category_diversity"],
        features["delivery_risk"],
    ], dtype=np.float32)

    with torch.no_grad():
        cltv_score = model(torch.tensor(x).unsqueeze(0)).item()

    # Normalize into 0–1 range (simple scaling)
    cltv_norm = min(1.0, max(0.0, cltv_score / 5000))

    return {
        "cltv_score": cltv_norm,
        "raw_prediction": cltv_score
    }