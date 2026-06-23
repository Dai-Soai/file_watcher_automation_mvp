from dataclasses import dataclass
from uuid import uuid4

from file_watcher.contract import WatchEvent, WatchScanResult


@dataclass
class WatchScanReport:
    scan_id: str
    status: str
    inbox_dir: str
    workflow_path: str
    total_events: int
    detected_events: int
    ignored_events: int
    unsupported_events: int
    events: list[dict]
    message: str


def event_to_dict(event: WatchEvent) -> dict:
    return {
        "event_id": event.event_id,
        "file_path": event.file_path,
        "file_name": event.file_name,
        "file_type": event.file_type,
        "status": event.status,
        "workflow_path": event.workflow_path,
        "file_size": event.file_size,
        "modified_at": event.modified_at,
        "reason": event.reason,
    }


def count_events_by_status(events: list[WatchEvent], status: str) -> int:
    return len([event for event in events if event.status == status])


def build_scan_report(result: WatchScanResult) -> WatchScanReport:
    detected_events = count_events_by_status(result.events, "detected")
    ignored_events = count_events_by_status(result.events, "ignored")
    unsupported_events = count_events_by_status(result.events, "unsupported")

    return WatchScanReport(
        scan_id=str(uuid4()),
        status=result.status,
        inbox_dir=result.inbox_dir,
        workflow_path=result.workflow_path,
        total_events=len(result.events),
        detected_events=detected_events,
        ignored_events=ignored_events,
        unsupported_events=unsupported_events,
        events=[event_to_dict(event) for event in result.events],
        message=result.message,
    )


def scan_report_to_dict(report: WatchScanReport) -> dict:
    return {
        "scan_id": report.scan_id,
        "status": report.status,
        "inbox_dir": report.inbox_dir,
        "workflow_path": report.workflow_path,
        "summary": {
            "total_events": report.total_events,
            "detected_events": report.detected_events,
            "ignored_events": report.ignored_events,
            "unsupported_events": report.unsupported_events,
        },
        "events": report.events,
        "message": report.message,
    }
