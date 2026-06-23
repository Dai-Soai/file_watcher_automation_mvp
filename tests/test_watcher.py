from pathlib import Path

from file_watcher.contract import resolve_watch_config
from file_watcher.watcher import scan_inbox


def test_resolve_watch_config():
    config = resolve_watch_config(
        inbox_dir="data/inbox",
        workflow_path="workflows/sample.workflow.json",
    )

    assert config.inbox_dir == "data/inbox"
    assert config.workflow_path == "workflows/sample.workflow.json"
    assert config.processed_dir == "data/processed"
    assert config.failed_dir == "data/failed"


def test_scan_inbox_detects_files(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    sample_file = inbox / "sample.txt"
    sample_file.write_text("RADAR watcher test", encoding="utf-8")

    config = resolve_watch_config(
        inbox_dir=str(inbox),
        workflow_path="workflows/sample.workflow.json",
    )

    result = scan_inbox(config)

    assert result.status == "ok"
    assert len(result.detected_files) == 1
    assert str(sample_file) in result.detected_files
    assert "Detected 1 file(s)." in result.message


def test_scan_inbox_ignores_gitkeep(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    gitkeep = inbox / ".gitkeep"
    gitkeep.write_text("", encoding="utf-8")

    config = resolve_watch_config(
        inbox_dir=str(inbox),
        workflow_path="workflows/sample.workflow.json",
    )

    result = scan_inbox(config)

    assert result.status == "ok"
    assert result.detected_files == []
    assert "Detected 0 file(s)." in result.message
