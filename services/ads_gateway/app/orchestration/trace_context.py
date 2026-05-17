from uuid import uuid4

from libs.contracts.decision_trace import DecisionTrace

def create_decision_trace():
    return DecisionTrace.create(
        request_id=f"req_{uuid4().hex}",
        trace_id=f"trace_{uuid4().hex}",
        decision_id=f"decision_{uuid4().hex}"
    )