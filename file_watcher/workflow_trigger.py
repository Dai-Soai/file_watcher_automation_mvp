import subprocess
from dataclasses import dataclass

from file_watcher.archive import ArchiveResult, archive_file
from file_watcher.contract import WatchEvent, WatchScanResult


@dataclass
class WorkflowTriggerResult:
    event_id: str
    file_path: str
    file_name: str
    status: str
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    message: str
    archive_result: ArchiveResult | None = None


def build_workflow_command(
    workflow_path: str,
    target: str,
) -> list[str]:
    return [
        "auto-run",
        workflow_path,
        "--target",
        target,
        "--export-json",
        "--export-markdown",
        "--publish",
    ]


def trigger_workflow_for_event(
    event: WatchEvent,
    target: str,
    dry_run: bool = False,
    archive: bool = False,
    processed_dir: str = "data/processed",
    failed_dir: str = "data/failed",
) -> WorkflowTriggerResult:
    if event.status != "detected":
        return WorkflowTriggerResult(
            event_id=event.event_id,
            file_path=event.file_path,
            file_name=event.file_name,
            status="skipped",
            command=[],
            returncode=0,
            stdout="",
            stderr="",
            message=f"Skipped event with status: {event.status}",
        )

    command = build_workflow_command(
        workflow_path=event.workflow_path,
        target=target,
    )

    if dry_run:
        return WorkflowTriggerResult(
            event_id=event.event_id,
            file_path=event.file_path,
            file_name=event.file_name,
            status="dry-run",
            command=command,
            returncode=0,
            stdout="",
            stderr="",
            message=f"Dry run workflow trigger for: {event.file_name}",
        )

    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )

    status = "ok" if completed.returncode == 0 else "failed"

    archive_result = None

    if archive:
        archive_dir = processed_dir if status == "ok" else failed_dir

        archive_result = archive_file(
            file_path=event.file_path,
            archive_dir=archive_dir,
        )

    return WorkflowTriggerResult(
        event_id=event.event_id,
        file_path=event.file_path,
        file_name=event.file_name,
        status=status,
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        message=f"Workflow trigger {status} for: {event.file_name}",
        archive_result=archive_result,
    )


def trigger_workflows_for_scan(
    result: WatchScanResult,
    dry_run: bool = False,
    archive: bool = False,
    processed_dir: str = "data/processed",
    failed_dir: str = "data/failed",
) -> list[WorkflowTriggerResult]:
    return [
        trigger_workflow_for_event(
            event=event,
            target=result.inbox_dir,
            dry_run=dry_run,
            archive=archive,
            processed_dir=processed_dir,
            failed_dir=failed_dir,
        )
        for event in result.events
        if event.status == "detected"
    ]
