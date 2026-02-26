from app.agents.risk import assess_risk

def test_risk_score():
    score = assess_risk({})
    assert isinstance(score, float)
