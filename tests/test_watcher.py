from file_watcher.contract import (
    build_watch_event,
    detect_file_type,
    resolve_watch_config,
)
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


def test_detect_file_type_text():
    assert detect_file_type("sample.txt") == "text"
    assert detect_file_type("sample.md") == "text"


def test_detect_file_type_image():
    assert detect_file_type("sample.png") == "image"
    assert detect_file_type("sample.jpg") == "image"
    assert detect_file_type("sample.jpeg") == "image"
    assert detect_file_type("sample.webp") == "image"


def test_detect_file_type_pdf():
    assert detect_file_type("sample.pdf") == "pdf"


def test_detect_file_type_json():
    assert detect_file_type("sample.json") == "json"


def test_detect_file_type_unknown():
    assert detect_file_type("sample.unknown") == "unknown"
    assert detect_file_type("sample") == "unknown"


def test_build_watch_event():
    event = build_watch_event(
        file_path="data/inbox/sample.txt",
        workflow_path="workflows/sample.workflow.json",
    )

    assert event.event_id
    assert event.file_path == "data/inbox/sample.txt"
    assert event.file_name == "sample.txt"
    assert event.file_type == "text"
    assert event.status == "detected"
    assert event.workflow_path == "workflows/sample.workflow.json"


def test_scan_inbox_detects_events(tmp_path):
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
    assert len(result.events) == 1
    assert result.events[0].file_name == "sample.txt"
    assert result.events[0].file_type == "text"
    assert result.events[0].status == "detected"
    assert "Detected 1 file event(s)." in result.message


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
    assert result.events == []
    assert "Detected 0 file event(s)." in result.message
