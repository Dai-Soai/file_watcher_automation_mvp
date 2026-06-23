from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4


@dataclass
class WatchConfig:
    inbox_dir: str
    workflow_path: str
    processed_dir: str = "data/processed"
    failed_dir: str = "data/failed"


@dataclass
class WatchEvent:
    event_id: str
    file_path: str
    file_name: str
    file_type: str
    status: str
    workflow_path: str


@dataclass
class WatchScanResult:
    status: str
    inbox_dir: str
    workflow_path: str
    events: list[WatchEvent]
    message: str


def resolve_watch_config(
    inbox_dir: str,
    workflow_path: str,
    processed_dir: str = "data/processed",
    failed_dir: str = "data/failed",
) -> WatchConfig:
    return WatchConfig(
        inbox_dir=str(Path(inbox_dir).expanduser()),
        workflow_path=str(Path(workflow_path).expanduser()),
        processed_dir=str(Path(processed_dir).expanduser()),
        failed_dir=str(Path(failed_dir).expanduser()),
    )


def detect_file_type(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()

    if suffix in {".txt", ".md"}:
        return "text"

    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return "image"

    if suffix == ".pdf":
        return "pdf"

    if suffix == ".json":
        return "json"

    return "unknown"


def build_watch_event(
    file_path: str,
    workflow_path: str,
) -> WatchEvent:
    path = Path(file_path)

    return WatchEvent(
        event_id=str(uuid4()),
        file_path=str(path),
        file_name=path.name,
        file_type=detect_file_type(str(path)),
        status="detected",
        workflow_path=workflow_path,
    )
