from pathlib import Path

from file_watcher.contract import WatchConfig, WatchScanResult, build_watch_event


def scan_inbox(config: WatchConfig) -> WatchScanResult:
    inbox_path = Path(config.inbox_dir).expanduser()

    if not inbox_path.exists():
        raise FileNotFoundError(f"Inbox directory not found: {inbox_path}")

    files = [
        path
        for path in sorted(inbox_path.iterdir())
        if path.is_file() and path.name != ".gitkeep"
    ]

    events = [
        build_watch_event(
            file_path=str(path),
            workflow_path=config.workflow_path,
        )
        for path in files
    ]

    return WatchScanResult(
        status="ok",
        inbox_dir=str(inbox_path),
        workflow_path=config.workflow_path,
        events=events,
        message=f"Detected {len(events)} file event(s).",
    )
