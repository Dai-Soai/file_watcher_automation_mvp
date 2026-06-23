from file_watcher.cli import print_watch_result
from file_watcher.contract import WatchEvent, WatchScanResult


def test_print_watch_result(capsys):
    result = WatchScanResult(
        status="ok",
        inbox_dir="data/inbox",
        workflow_path="workflows/sample.workflow.json",
        events=[
            WatchEvent(
                event_id="event-001",
                file_path="data/inbox/sample.txt",
                file_name="sample.txt",
                file_type="text",
                status="detected",
                workflow_path="workflows/sample.workflow.json",
                file_size=42,
                modified_at=123.0,
                reason="supported file detected",
            )
        ],
        message="Detected 1 supported file event(s).",
    )

    print_watch_result(result)

    captured = capsys.readouterr()

    assert "FILE WATCHER AUTOMATION MVP" in captured.out
    assert "Status: ok" in captured.out
    assert "Inbox: data/inbox" in captured.out
    assert "Workflow: workflows/sample.workflow.json" in captured.out
    assert "Events: 1" in captured.out
    assert "Summary: detected=1, ignored=0, unsupported=0" in captured.out
    assert "sample.txt" in captured.out
    assert "text" in captured.out
    assert "size=42" in captured.out
    assert "event-001" in captured.out
    assert "supported file detected" in captured.out
