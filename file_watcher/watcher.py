from dataclasses import dataclass
from pathlib import Path

from file_watcher.contract import WatchConfig


@dataclass
class WatchResult:
    status: str
    inbox_dir: str
    workflow_path: str
    detected_files: list[str]
    message: str


def scan_inbox(config: WatchConfig) -> WatchResult:
    inbox_path = Path(config.inbox_dir).expanduser()

    if not inbox_path.exists():
        raise FileNotFoundError(f"Inbox directory not found: {inbox_path}")

    detected_files = [
        str(path)
        for path in sorted(inbox_path.iterdir())
        if path.is_file() and path.name != ".gitkeep"
    ]

    return WatchResult(
        status="ok",
        inbox_dir=str(inbox_path),
        workflow_path=config.workflow_path,
        detected_files=detected_files,
        message=f"Detected {len(detected_files)} file(s).",
    )
