from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

SUPPORTED_FILE_TYPES = {"text", "image"}


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
    file_size: int = 0
    modified_at: float = 0.0
    reason: str = ""


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


def is_supported_file_type(file_type: str) -> bool:
    return file_type in SUPPORTED_FILE_TYPES


def should_ignore_file(file_path: str) -> bool:
    path = Path(file_path)
    name = path.name

    if name == ".gitkeep":
        return True

    if name.startswith("."):
        return True

    if name.endswith("~"):
        return True

    if name.endswith(".tmp"):
        return True

    if name.endswith(".swp"):
        return True

    return False


def build_watch_event(
    file_path: str,
    workflow_path: str,
) -> WatchEvent:
    path = Path(file_path)
    file_type = detect_file_type(str(path))

    file_size = 0
    modified_at = 0.0

    if path.exists():
        stat = path.stat()
        file_size = stat.st_size
        modified_at = stat.st_mtime

    if should_ignore_file(str(path)):
        status = "ignored"
        reason = "ignored file pattern"
    elif not is_supported_file_type(file_type):
        status = "unsupported"
        reason = f"unsupported file type: {file_type}"
    else:
        status = "detected"
        reason = "supported file detected"

    return WatchEvent(
        event_id=str(uuid4()),
        file_path=str(path),
        file_name=path.name,
        file_type=file_type,
        status=status,
        workflow_path=workflow_path,
        file_size=file_size,
        modified_at=modified_at,
        reason=reason,
    )
