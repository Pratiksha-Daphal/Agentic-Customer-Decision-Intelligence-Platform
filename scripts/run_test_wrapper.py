import sys
sys.path.append(r'c:/Users/pratiksha daphal/Desktop/agentic-customer-decision-platform')
from app.graph.nodes.feature import feature_agent
from app.graph.nodes.cltv import cltv_agent

state = {"customer_id": 1}
state = feature_agent(state)
print("features after feature_agent:", state["features"])
try:
    state = cltv_agent(state)
    print("cltv output:", state.get("cltv"))
except Exception as e:
    import traceback
    traceback.print_exc()
