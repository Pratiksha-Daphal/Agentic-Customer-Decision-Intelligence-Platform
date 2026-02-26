from app.services.decision_service import run_decision_flow

def test_decision_flow_returns_list():
    result = run_decision_flow(1)
    assert isinstance(result, list)
