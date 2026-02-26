from pydantic import BaseModel
from typing import Any, Dict, Optional
from datetime import datetime


class HealthResponse(BaseModel):
    status: str


class NextBestActionResponse(BaseModel):
    customer_id: int
    action: str

    expected_utility: Optional[float] = None
    explanation: Optional[Dict[str, Any]] = None
    decided_at: Optional[datetime] = None

    # fallback case
    reason: Optional[str] = None