from file_watcher.cli import print_watch_result
from file_watcher.watcher import WatchResult


def test_print_watch_result(capsys):
    result = WatchResult(
        status="ok",
        inbox_dir="data/inbox",
        workflow_path="workflows/sample.workflow.json",
        detected_files=["data/inbox/sample.txt"],
        message="Detected 1 file(s).",
    )

    print_watch_result(result)

    captured = capsys.readouterr()

    assert "FILE WATCHER AUTOMATION MVP" in captured.out
    assert "Status: ok" in captured.out
    assert "Inbox: data/inbox" in captured.out
    assert "Workflow: workflows/sample.workflow.json" in captured.out
    assert "Detected: 1 file(s)" in captured.out
    assert "data/inbox/sample.txt" in captured.out
