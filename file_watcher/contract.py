from dataclasses import dataclass
from pathlib import Path


@dataclass
class WatchConfig:
    inbox_dir: str
    workflow_path: str
    processed_dir: str = "data/processed"
    failed_dir: str = "data/failed"


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
