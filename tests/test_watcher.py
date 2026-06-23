from file_watcher.contract import (
    build_watch_event,
    detect_file_type,
    is_supported_file_type,
    resolve_watch_config,
    should_ignore_file,
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


def test_is_supported_file_type():
    assert is_supported_file_type("text") is True
    assert is_supported_file_type("image") is True
    assert is_supported_file_type("pdf") is False
    assert is_supported_file_type("json") is False
    assert is_supported_file_type("unknown") is False


def test_should_ignore_file():
    assert should_ignore_file(".gitkeep") is True
    assert should_ignore_file(".hidden") is True
    assert should_ignore_file("sample.txt~") is True
    assert should_ignore_file("sample.tmp") is True
    assert should_ignore_file("sample.swp") is True
    assert should_ignore_file("sample.txt") is False


def test_build_watch_event_supported_file(tmp_path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("RADAR watcher test", encoding="utf-8")

    event = build_watch_event(
        file_path=str(sample_file),
        workflow_path="workflows/sample.workflow.json",
    )

    assert event.event_id
    assert event.file_path == str(sample_file)
    assert event.file_name == "sample.txt"
    assert event.file_type == "text"
    assert event.status == "detected"
    assert event.workflow_path == "workflows/sample.workflow.json"
    assert event.file_size > 0
    assert event.modified_at > 0
    assert event.reason == "supported file detected"


def test_build_watch_event_unsupported_file(tmp_path):
    sample_file = tmp_path / "sample.pdf"
    sample_file.write_text("PDF placeholder", encoding="utf-8")

    event = build_watch_event(
        file_path=str(sample_file),
        workflow_path="workflows/sample.workflow.json",
    )

    assert event.file_name == "sample.pdf"
    assert event.file_type == "pdf"
    assert event.status == "unsupported"
    assert event.reason == "unsupported file type: pdf"


def test_build_watch_event_ignored_file(tmp_path):
    sample_file = tmp_path / ".hidden"
    sample_file.write_text("hidden", encoding="utf-8")

    event = build_watch_event(
        file_path=str(sample_file),
        workflow_path="workflows/sample.workflow.json",
    )

    assert event.file_name == ".hidden"
    assert event.status == "ignored"
    assert event.reason == "ignored file pattern"


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
    assert "Detected 1 supported file event(s)." in result.message


def test_scan_inbox_marks_ignored_and_unsupported(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    (inbox / ".gitkeep").write_text("", encoding="utf-8")
    (inbox / "sample.pdf").write_text("PDF placeholder", encoding="utf-8")
    (inbox / "sample.txt").write_text("text", encoding="utf-8")

    config = resolve_watch_config(
        inbox_dir=str(inbox),
        workflow_path="workflows/sample.workflow.json",
    )

    result = scan_inbox(config)

    statuses = {event.file_name: event.status for event in result.events}

    assert statuses[".gitkeep"] == "ignored"
    assert statuses["sample.pdf"] == "unsupported"
    assert statuses["sample.txt"] == "detected"
    assert "Detected 1 supported file event(s)." in result.message
