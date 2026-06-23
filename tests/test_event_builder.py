from file_watcher.contract import WatchEvent, WatchScanResult
from file_watcher.event_builder import (
    build_scan_report,
    count_events_by_status,
    event_to_dict,
    scan_report_to_dict,
)


def make_event(
    file_name: str,
    file_type: str,
    status: str,
    reason: str,
) -> WatchEvent:
    return WatchEvent(
        event_id=f"event-{file_name}",
        file_path=f"data/inbox/{file_name}",
        file_name=file_name,
        file_type=file_type,
        status=status,
        workflow_path="workflows/sample.workflow.json",
        file_size=42,
        modified_at=123.0,
        reason=reason,
    )


def test_event_to_dict():
    event = make_event(
        file_name="sample.txt",
        file_type="text",
        status="detected",
        reason="supported file detected",
    )

    payload = event_to_dict(event)

    assert payload["event_id"] == "event-sample.txt"
    assert payload["file_path"] == "data/inbox/sample.txt"
    assert payload["file_name"] == "sample.txt"
    assert payload["file_type"] == "text"
    assert payload["status"] == "detected"
    assert payload["workflow_path"] == "workflows/sample.workflow.json"
    assert payload["file_size"] == 42
    assert payload["modified_at"] == 123.0
    assert payload["reason"] == "supported file detected"


def test_count_events_by_status():
    events = [
        make_event("sample.txt", "text", "detected", "supported file detected"),
        make_event(".gitkeep", "unknown", "ignored", "ignored file pattern"),
        make_event("sample.pdf", "pdf", "unsupported", "unsupported file type: pdf"),
    ]

    assert count_events_by_status(events, "detected") == 1
    assert count_events_by_status(events, "ignored") == 1
    assert count_events_by_status(events, "unsupported") == 1
    assert count_events_by_status(events, "missing") == 0


def test_build_scan_report():
    events = [
        make_event("sample.txt", "text", "detected", "supported file detected"),
        make_event(".gitkeep", "unknown", "ignored", "ignored file pattern"),
        make_event("sample.pdf", "pdf", "unsupported", "unsupported file type: pdf"),
    ]

    result = WatchScanResult(
        status="ok",
        inbox_dir="data/inbox",
        workflow_path="workflows/sample.workflow.json",
        events=events,
        message="Detected 1 supported file event(s).",
    )

    report = build_scan_report(result)

    assert report.scan_id
    assert report.status == "ok"
    assert report.inbox_dir == "data/inbox"
    assert report.workflow_path == "workflows/sample.workflow.json"
    assert report.total_events == 3
    assert report.detected_events == 1
    assert report.ignored_events == 1
    assert report.unsupported_events == 1
    assert len(report.events) == 3
    assert report.message == "Detected 1 supported file event(s)."


def test_scan_report_to_dict():
    events = [
        make_event("sample.txt", "text", "detected", "supported file detected"),
    ]

    result = WatchScanResult(
        status="ok",
        inbox_dir="data/inbox",
        workflow_path="workflows/sample.workflow.json",
        events=events,
        message="Detected 1 supported file event(s).",
    )

    report = build_scan_report(result)
    payload = scan_report_to_dict(report)

    assert payload["scan_id"] == report.scan_id
    assert payload["status"] == "ok"
    assert payload["inbox_dir"] == "data/inbox"
    assert payload["workflow_path"] == "workflows/sample.workflow.json"
    assert payload["summary"]["total_events"] == 1
    assert payload["summary"]["detected_events"] == 1
    assert payload["summary"]["ignored_events"] == 0
    assert payload["summary"]["unsupported_events"] == 0
    assert payload["events"][0]["file_name"] == "sample.txt"
    assert payload["message"] == "Detected 1 supported file event(s)."
