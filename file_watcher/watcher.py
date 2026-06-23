from pathlib import Path

from file_watcher.contract import WatchConfig, WatchScanResult, build_watch_event


def scan_inbox(config: WatchConfig) -> WatchScanResult:
    inbox_path = Path(config.inbox_dir).expanduser()

    if not inbox_path.exists():
        raise FileNotFoundError(f"Inbox directory not found: {inbox_path}")

    files = [path for path in sorted(inbox_path.iterdir()) if path.is_file()]

    events = [
        build_watch_event(
            file_path=str(path),
            workflow_path=config.workflow_path,
        )
        for path in files
    ]

    detected_count = len([event for event in events if event.status == "detected"])

    return WatchScanResult(
        status="ok",
        inbox_dir=str(inbox_path),
        workflow_path=config.workflow_path,
        events=events,
        message=f"Detected {detected_count} supported file event(s).",
    )
