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

class DecisionTraceStep(BaseModel):
    """One step in the ad decision workflow."""

    service_name: str
    operation_name: str
    status: str
    input_count: int | None = None
    output_count: int | None = None
    latency_ms: float | None = None
    reasons: list[str] = Field(default_factory=list)


class DecisionTraceSummary(BaseModel):
    """Debug-friendly summary of the ad decision workflow."""

    request_id: str
    trace_id: str
    decision_id: str
    viewer_id: str
    session_id: str
    content_id: str
    placement_id: str
    ad_break_id: str
    final_status: str
    steps: list[DecisionTraceStep] = Field(default_factory=list)