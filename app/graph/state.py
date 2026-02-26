from typing import Optional, List, Dict, Any, TypedDict

class DecisionState(TypedDict):
    customer_id: int
    features: Optional[Dict[str, Any]]
    cltv: Optional[Dict[str, Any]]
    insights: Optional[List[Dict[str, Any]]]   # 👈 NEW
    candidate_actions: Optional[List[Dict[str, Any]]]
    risk_assessment: Optional[List[Dict[str, Any]]]
    final_decision: Optional[Dict[str, Any]]