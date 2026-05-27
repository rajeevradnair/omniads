import json
import time
from typing import Any


def log_event(
    service_name: str,
    operation_name: str,
    status: str,
    trace_id: str | None = None,
    request_id: str | None = None,
    decision_id: str | None = None,
    latency_ms: float | None = None,
    error_type: str | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    """Write a structured JSON log event to stdout.

    Args:
        service_name: Name of the service producing the log.
        operation_name: Name of the operation being logged.
        status: Operation status such as started, success, failed.
        trace_id: Distributed trace identifier.
        request_id: Request identifier.
        decision_id: Ad decision identifier.
        latency_ms: Operation latency in milliseconds.
        error_type: Optional error category.
        extra: Optional additional fields.
    """

    event = {
        "timestamp_epoch_ms": int(time.time() * 1000),
        "trace_id": trace_id,
        "request_id": request_id,
        "decision_id": decision_id,
        "latency_ms": latency_ms,
        "service_name": service_name,
        "operation_name": operation_name,
        "status": status,
        "error_type": error_type,
    }

    if extra:
        event.update(extra)

    print(json.dumps(event))