import sys
sys.path.append(r'c:/Users/pratiksha daphal/Desktop/agentic-customer-decision-platform')
from app.services.decision_service import run_decision_flow

print(run_decision_flow(1))
