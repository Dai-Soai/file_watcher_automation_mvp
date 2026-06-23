import argparse
import time

from file_watcher.contract import resolve_watch_config
from file_watcher.event_builder import build_scan_report
from file_watcher.event_log import build_event_log_payload, write_event_log
from file_watcher.watcher import scan_inbox
from file_watcher.workflow_trigger import trigger_workflows_for_scan


def print_watch_result(result):
    print("=" * 60)
    print("FILE WATCHER AUTOMATION MVP")
    print("=" * 60)
    print(f"Status: {result.status}")
    print(f"Inbox: {result.inbox_dir}")
    print(f"Workflow: {result.workflow_path}")
    print(f"Events: {len(result.events)}")

    report = build_scan_report(result)

    print(
        "Summary: "
        f"detected={report.detected_events}, "
        f"ignored={report.ignored_events}, "
        f"unsupported={report.unsupported_events}"
    )

    if result.events:
        print()
        print("Events:")
        for event in result.events:
            print(
                f"- [{event.status}] "
                f"{event.file_name} "
                f"({event.file_type}) "
                f"size={event.file_size} "
                f"id={event.event_id}"
            )
            print(f"  reason: {event.reason}")

    print()
    print(result.message)


def main():
    parser = argparse.ArgumentParser(
        prog="watch-run",
        description="File Watcher Automation MVP",
    )

    parser.add_argument(
        "inbox",
        help="Directory to scan for new files",
    )

    parser.add_argument(
        "--workflow",
        required=True,
        help="Workflow contract path to trigger for detected files",
    )

    parser.add_argument(
        "--processed-dir",
        default="data/processed",
        help="Directory for processed files",
    )

    parser.add_argument(
        "--failed-dir",
        default="data/failed",
        help="Directory for failed files",
    )

    parser.add_argument(
        "--trigger",
        action="store_true",
        help="Trigger workflow for detected files",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build trigger commands without executing workflow",
    )

    parser.add_argument(
        "--archive",
        action="store_true",
        help="Move successfully triggered files to processed dir and failed files to failed dir",
    )

    parser.add_argument(
        "--log-json",
        action="store_true",
        help="Write scan and trigger results to JSON event log",
    )

    parser.add_argument(
        "--log-dir",
        default="outputs/event_logs",
        help="Directory for JSON event logs",
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one scan cycle and exit",
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=0,
        help="Seconds between watch cycles. 0 means run once.",
    )

    parser.add_argument(
        "--max-cycles",
        type=int,
        default=1,
        help="Maximum number of watch cycles to run.",
    )

    args = parser.parse_args()

    max_cycles = 1 if args.once or args.interval <= 0 else args.max_cycles

    for cycle in range(max_cycles):
        if max_cycles > 1:
            print()
            print(f"Watch Cycle: {cycle + 1}/{max_cycles}")

        run_watch_cycle(args)

        if cycle < max_cycles - 1:
            time.sleep(args.interval)


def run_watch_cycle(args):
    config = resolve_watch_config(
        inbox_dir=args.inbox,
        workflow_path=args.workflow,
        processed_dir=args.processed_dir,
        failed_dir=args.failed_dir,
    )

    result = scan_inbox(config)

    print_watch_result(result)

    scan_report = build_scan_report(result)
    trigger_results = []

    if args.trigger:
        trigger_results = trigger_workflows_for_scan(
            result,
            dry_run=args.dry_run,
            archive=args.archive,
            processed_dir=args.processed_dir,
            failed_dir=args.failed_dir,
        )

        print()
        print("Workflow Triggers:")

        if not trigger_results:
            print("- No detected files to trigger.")

        for trigger_result in trigger_results:
            print(
                f"- [{trigger_result.status}] "
                f"{trigger_result.file_name} "
                f"returncode={trigger_result.returncode}"
            )
            print(f"  command: {' '.join(trigger_result.command)}")
            print(f"  message: {trigger_result.message}")

            if trigger_result.archive_result is not None:
                archive_result = trigger_result.archive_result
                print(f"  archive: {archive_result.status}")
                print(f"  destination: {archive_result.destination_path}")

    if args.log_json:
        payload = build_event_log_payload(
            scan_report=scan_report,
            trigger_results=trigger_results,
        )

        log_path = write_event_log(
            payload=payload,
            output_dir=args.log_dir,
        )

        print()
        print(f"JSON event log written: {log_path}")


if __name__ == "__main__":
    main()
