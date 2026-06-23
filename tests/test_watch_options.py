from argparse import Namespace
from unittest.mock import patch

from file_watcher.cli import run_watch_cycle


def make_args(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    sample = inbox / "sample.txt"
    sample.write_text("RADAR watch options", encoding="utf-8")

    return Namespace(
        inbox=str(inbox),
        workflow="workflows/sample.workflow.json",
        processed_dir=str(tmp_path / "processed"),
        failed_dir=str(tmp_path / "failed"),
        trigger=False,
        dry_run=False,
        archive=False,
        log_json=False,
        log_dir=str(tmp_path / "logs"),
        once=True,
        interval=0,
        max_cycles=1,
    )


def test_run_watch_cycle_prints_result(tmp_path, capsys):
    args = make_args(tmp_path)

    run_watch_cycle(args)

    captured = capsys.readouterr()

    assert "FILE WATCHER AUTOMATION MVP" in captured.out
    assert "Events: 1" in captured.out
    assert "Summary: detected=1" in captured.out


def test_run_watch_cycle_with_log_json(tmp_path, capsys):
    args = make_args(tmp_path)
    args.log_json = True

    run_watch_cycle(args)

    captured = capsys.readouterr()

    assert "JSON event log written:" in captured.out
    assert list((tmp_path / "logs").glob("*.json"))


def test_run_watch_cycle_with_trigger_dry_run(tmp_path, capsys):
    args = make_args(tmp_path)
    args.trigger = True
    args.dry_run = True

    run_watch_cycle(args)

    captured = capsys.readouterr()

    assert "Workflow Triggers:" in captured.out
    assert "[dry-run] sample.txt" in captured.out
