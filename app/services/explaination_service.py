import subprocess
import json
from typing import Dict, Any


def _format_percentage(value):
    if value is None:
        return None
    return round(value * 100, 1)


def generate_natural_language_explanation(decision: Dict[str, Any]) -> str:
    explanation = decision.get("explanation", {})

    # ---- Normalise & ground values ----
    churn_pct = _format_percentage(explanation.get("churn_risk"))
    delivery_pct = _format_percentage(explanation.get("delivery_risk"))
    fatigue_pct = _format_percentage(explanation.get("fatigue_risk"))
    cltv_score = explanation.get("cltv_score")

    context = {
        "action": decision.get("action"),
        "expected_utility": decision.get("expected_utility"),
        "customer_value": (
            "Low" if cltv_score == 0 else "Medium/High"
            if cltv_score is not None else "Unknown"
        ),
        "churn_risk_pct": churn_pct,
        "delivery_risk_pct": delivery_pct,
        "fatigue_risk_pct": fatigue_pct,
    }

    prompt = f"""
You are explaining a customer decision to a business stakeholder.

You MUST strictly use the information below.
If a value is marked as "Unknown", say that data is unavailable.
DO NOT invent numbers or scenarios.

Decision signals (ground truth):
{json.dumps(context, indent=2)}

Write the explanation using ONLY bullet points, in this exact structure:

Decision Summary:
- Recommended action
- Expected business impact (interpret the expected utility number)

Key Factors Considered:
- Customer long-term value
  - Current assessment
  - Best case (high lifetime value customer)
  - Worst case (low or uncertain value)
- Churn risk
  - Current level (use percentage if available)
  - Best case: 0% (very stable)
  - Worst case: 100% (very likely to churn)
- Delivery experience risk
  - Current level (use percentage if available)
  - Best case: consistently on-time
  - Worst case: frequent delays harming trust
- Engagement fatigue risk
  - Current level (use percentage if available)
  - Best case: receptive to outreach
  - Worst case: disengagement due to over-contact

Business Rationale:
- 1–2 bullets explaining why this decision is safer for long-term revenue and customer trust

Rules:
- Bullet points only
- Business language only
- If data is unavailable, explicitly say so
- Never contradict numeric meaning
- Do NOT mention AI, models, ML, or algorithms
"""

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        text=True,
        capture_output=True,
    )

    return result.stdout.strip() or (
        "- Decision Summary:\n"
        "  - Recommended action: No action\n"
        "  - Expected business impact: Very limited upside\n\n"
        "- Key Factors Considered:\n"
        "  - Customer long-term value: Unknown\n"
        "  - Churn risk: Unknown\n"
        "  - Delivery experience risk: Unknown\n"
        "  - Engagement fatigue risk: Unknown\n\n"
        "- Business Rationale:\n"
        "  - Avoiding outreach reduces the risk of unnecessary customer disengagement."
    )