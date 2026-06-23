import json
from dataclasses import asdict
from pathlib import Path

from file_watcher.event_builder import WatchScanReport, scan_report_to_dict
from file_watcher.workflow_trigger import WorkflowTriggerResult


def trigger_result_to_dict(result: WorkflowTriggerResult) -> dict:
    payload = {
        "event_id": result.event_id,
        "file_path": result.file_path,
        "file_name": result.file_name,
        "status": result.status,
        "command": result.command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "message": result.message,
        "archive_result": None,
    }

    if result.archive_result is not None:
        payload["archive_result"] = asdict(result.archive_result)

    return payload


def build_event_log_payload(
    scan_report: WatchScanReport,
    trigger_results: list[WorkflowTriggerResult] | None = None,
) -> dict:
    return {
        "scan": scan_report_to_dict(scan_report),
        "triggers": [
            trigger_result_to_dict(result) for result in (trigger_results or [])
        ],
    }


def write_event_log(
    payload: dict,
    output_dir: str = "outputs/event_logs",
) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    scan_id = payload["scan"]["scan_id"]
    output_path = Path(output_dir) / f"{scan_id}.json"

    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return str(output_path)
