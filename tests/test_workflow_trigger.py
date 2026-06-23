from unittest.mock import Mock, patch

from file_watcher.contract import WatchEvent, WatchScanResult
from file_watcher.workflow_trigger import (
    build_workflow_command,
    trigger_workflow_for_event,
    trigger_workflows_for_scan,
)


def make_event(
    status: str = "detected",
    file_name: str = "sample.txt",
) -> WatchEvent:
    return WatchEvent(
        event_id=f"event-{file_name}",
        file_path=f"data/inbox/{file_name}",
        file_name=file_name,
        file_type="text",
        status=status,
        workflow_path="workflows/sample.workflow.json",
        file_size=42,
        modified_at=123.0,
        reason="test event",
    )


def test_build_workflow_command():
    command = build_workflow_command(
        workflow_path="workflows/sample.workflow.json",
        target="data/inbox",
    )

    assert command == [
        "auto-run",
        "workflows/sample.workflow.json",
        "--target",
        "data/inbox",
        "--export-json",
        "--export-markdown",
        "--publish",
    ]


def test_trigger_workflow_for_event_dry_run():
    event = make_event()

    result = trigger_workflow_for_event(
        event=event,
        target="data/inbox",
        dry_run=True,
    )

    assert result.event_id == "event-sample.txt"
    assert result.file_name == "sample.txt"
    assert result.status == "dry-run"
    assert result.returncode == 0
    assert result.command[0] == "auto-run"
    assert "--target" in result.command
    assert "Dry run workflow trigger" in result.message


def test_trigger_workflow_for_event_skips_non_detected():
    event = make_event(status="ignored", file_name=".hidden")

    result = trigger_workflow_for_event(
        event=event,
        target="data/inbox",
        dry_run=True,
    )

    assert result.file_name == ".hidden"
    assert result.status == "skipped"
    assert result.command == []
    assert result.returncode == 0
    assert "Skipped event with status: ignored" in result.message


def test_trigger_workflows_for_scan_dry_run_only_detected():
    events = [
        make_event(status="detected", file_name="sample.txt"),
        make_event(status="ignored", file_name=".hidden"),
        make_event(status="unsupported", file_name="sample.pdf"),
    ]

    scan_result = WatchScanResult(
        status="ok",
        inbox_dir="data/inbox",
        workflow_path="workflows/sample.workflow.json",
        events=events,
        message="Detected 1 supported file event(s).",
    )

    results = trigger_workflows_for_scan(
        scan_result,
        dry_run=True,
    )

    assert len(results) == 1
    assert results[0].file_name == "sample.txt"
    assert results[0].status == "dry-run"


def test_trigger_workflow_for_event_archive_ok(tmp_path):
    source = tmp_path / "sample.txt"
    source.write_text("RADAR archive trigger", encoding="utf-8")

    processed = tmp_path / "processed"

    event = WatchEvent(
        event_id="event-sample.txt",
        file_path=str(source),
        file_name="sample.txt",
        file_type="text",
        status="detected",
        workflow_path="workflows/sample.workflow.json",
        file_size=42,
        modified_at=123.0,
        reason="test event",
    )

    completed = Mock()
    completed.returncode = 0
    completed.stdout = "workflow ok"
    completed.stderr = ""

    with patch("file_watcher.workflow_trigger.subprocess.run", return_value=completed):
        result = trigger_workflow_for_event(
            event=event,
            target="data/inbox",
            archive=True,
            processed_dir=str(processed),
            failed_dir=str(tmp_path / "failed"),
        )

    assert result.status == "ok"
    assert result.archive_result is not None
    assert result.archive_result.status == "archived"
    assert not source.exists()
    assert (processed / "sample.txt").exists()


def test_trigger_workflow_for_event_archive_failed(tmp_path):
    source = tmp_path / "sample.txt"
    source.write_text("RADAR failed archive trigger", encoding="utf-8")

    failed = tmp_path / "failed"

    event = WatchEvent(
        event_id="event-sample.txt",
        file_path=str(source),
        file_name="sample.txt",
        file_type="text",
        status="detected",
        workflow_path="workflows/sample.workflow.json",
        file_size=42,
        modified_at=123.0,
        reason="test event",
    )

    completed = Mock()
    completed.returncode = 1
    completed.stdout = ""
    completed.stderr = "workflow failed"

    with patch("file_watcher.workflow_trigger.subprocess.run", return_value=completed):
        result = trigger_workflow_for_event(
            event=event,
            target="data/inbox",
            archive=True,
            processed_dir=str(tmp_path / "processed"),
            failed_dir=str(failed),
        )

    assert result.status == "failed"
    assert result.archive_result is not None
    assert result.archive_result.status == "archived"
    assert not source.exists()
    assert (failed / "sample.txt").exists()


def test_trigger_workflow_for_event_dry_run_does_not_archive(tmp_path):
    source = tmp_path / "sample.txt"
    source.write_text("RADAR dry run archive", encoding="utf-8")

    event = WatchEvent(
        event_id="event-sample.txt",
        file_path=str(source),
        file_name="sample.txt",
        file_type="text",
        status="detected",
        workflow_path="workflows/sample.workflow.json",
        file_size=42,
        modified_at=123.0,
        reason="test event",
    )

    result = trigger_workflow_for_event(
        event=event,
        target="data/inbox",
        dry_run=True,
        archive=True,
        processed_dir=str(tmp_path / "processed"),
        failed_dir=str(tmp_path / "failed"),
    )

    assert result.status == "dry-run"
    assert result.archive_result is None
    assert source.exists()
