import json
from dataclasses import dataclass
from pathlib import Path

from file_watcher.archive import ArchiveResult
from file_watcher.contract import WatchEvent, WatchScanResult
from file_watcher.event_builder import build_scan_report
from file_watcher.event_log import (
    build_event_log_payload,
    trigger_result_to_dict,
    write_event_log,
)
from file_watcher.workflow_trigger import WorkflowTriggerResult


def make_trigger_result() -> WorkflowTriggerResult:
    return WorkflowTriggerResult(
        event_id="event-sample.txt",
        file_path="data/inbox/sample.txt",
        file_name="sample.txt",
        status="ok",
        command=[
            "auto-run",
            "workflows/sample.workflow.json",
            "--target",
            "data/inbox",
        ],
        returncode=0,
        stdout="workflow ok",
        stderr="",
        message="Workflow trigger ok for: sample.txt",
        archive_result=ArchiveResult(
            source_path="data/inbox/sample.txt",
            destination_path="data/processed/sample.txt",
            status="archived",
            message="Archived file to: data/processed/sample.txt",
        ),
    )


def make_scan_report():
    event = WatchEvent(
        event_id="event-sample.txt",
        file_path="data/inbox/sample.txt",
        file_name="sample.txt",
        file_type="text",
        status="detected",
        workflow_path="workflows/sample.workflow.json",
        file_size=42,
        modified_at=123.0,
        reason="supported file detected",
    )

    scan_result = WatchScanResult(
        status="ok",
        inbox_dir="data/inbox",
        workflow_path="workflows/sample.workflow.json",
        events=[event],
        message="Detected 1 supported file event(s).",
    )

    return build_scan_report(scan_result)


def test_trigger_result_to_dict_with_archive():
    result = make_trigger_result()

    payload = trigger_result_to_dict(result)

    assert payload["event_id"] == "event-sample.txt"
    assert payload["file_name"] == "sample.txt"
    assert payload["status"] == "ok"
    assert payload["returncode"] == 0
    assert payload["archive_result"]["status"] == "archived"
    assert payload["archive_result"]["destination_path"] == "data/processed/sample.txt"


def test_build_event_log_payload():
    scan_report = make_scan_report()
    trigger_result = make_trigger_result()

    payload = build_event_log_payload(
        scan_report=scan_report,
        trigger_results=[trigger_result],
    )

    assert payload["scan"]["scan_id"] == scan_report.scan_id
    assert payload["scan"]["summary"]["total_events"] == 1
    assert payload["scan"]["summary"]["detected_events"] == 1
    assert len(payload["triggers"]) == 1
    assert payload["triggers"][0]["file_name"] == "sample.txt"


def test_build_event_log_payload_without_triggers():
    scan_report = make_scan_report()

    payload = build_event_log_payload(scan_report=scan_report)

    assert payload["scan"]["scan_id"] == scan_report.scan_id
    assert payload["triggers"] == []


def test_write_event_log(tmp_path):
    scan_report = make_scan_report()
    trigger_result = make_trigger_result()

    payload = build_event_log_payload(
        scan_report=scan_report,
        trigger_results=[trigger_result],
    )

    output_path = write_event_log(
        payload=payload,
        output_dir=str(tmp_path),
    )

    path = Path(output_path)

    assert path.exists()
    assert path.name == f"{scan_report.scan_id}.json"

    loaded = json.loads(path.read_text(encoding="utf-8"))

    assert loaded["scan"]["scan_id"] == scan_report.scan_id
    assert loaded["triggers"][0]["status"] == "ok"
