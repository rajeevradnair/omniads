from datetime import datetime, timezone

from pydantic import BaseModel, Field

class DecisionTrace(BaseModel):
    request_id: str
    trace_id: str 
    decision_id: str 
    service_name: str = "ads_gateway"
    timestamp: datetime

    @classmethod 
    def create(cls, request_id:str, trace_id:str, decision_id: str):
        return cls(
            request_id=request_id,
            trace_id=trace_id,
            decision_id=decision_id,
            timestamp=datetime.now(timezone.utc)
        )