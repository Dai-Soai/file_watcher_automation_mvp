# File Watcher Automation MVP

A lightweight folder watcher automation utility for triggering RADAR document workflows when new files appear.

## Current Status

Current Status: v0.1.0 Release.

## Purpose

This utility is designed to move the RADAR AI Utility Ecosystem from manual workflow execution to event-driven automation.

It will watch an inbox folder, detect new files, and trigger workflow automation.

## Features

- CLI command: `watch-run`
- Watch config contract
- Inbox folder scan
- File detection placeholder
- Pytest foundation
- Watch event contract
- Watch scan result contract
- File type detection
- Event ID generation
- Supported file type detection
- Ignored file pattern detection
- Unsupported file status
- File size metadata
- Modified time metadata
- Event reason field
- Event-to-dict serialization
- Scan report builder
- Event status counters
- JSON-ready scan report payload
- CLI scan summary
- Workflow trigger executor
- `auto-run` command builder
- Trigger dry-run mode
- Trigger only detected events
- Skip ignored and unsupported events
- JSON event log writer
- Scan report payload export
- Trigger result payload export
- Archive result payload export
- `--log-json` CLI option
- Custom log directory with `--log-dir`
- One-shot watch mode
- Interval-based watch cycles
- Maximum cycle limit
- Reusable watch cycle runner
- `--once`
- `--interval`
- `--max-cycles`
- Package build support
- Wheel distribution support
- Editable install support

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```
## Build Package

```bash
pip install build
rm -rf dist build *.egg-info
python -m build
```
## Install Built Package

```bash
pip uninstall file-watcher-automation-mvp -y
pip install dist/*.whl
watch-run --help
```
## For continued development:

pip install -e ".[dev]"

## Testing

```bash
pytest
```

## Latest result:

37 passed

## Expected outputs:

file_watcher_automation_mvp-0.1.0-py3-none-any.whl
file_watcher_automation_mvp-0.1.0.tar.gz

## Generated under:

```text
dist/
```

## Release Notes

### v0.1.0

Initial release of File Watcher Automation MVP.

Includes:

- Inbox folder scanning
- Watch event contract
- File detection layer
- Event builder
- Workflow trigger executor
- Processed / failed archive
- JSON event log
- CLI watch options
- One-shot mode
- Interval watch cycles
- Pytest coverage

## Usage

### Quick Start

```bash
watch-run data/inbox \
  --workflow workflows/sample.workflow.json
```

### Trigger Workflow Dry Run

```bash
watch-run data/inbox \
  --workflow workflows/sample.workflow.json \
  --trigger \
  --dry-run
```

### Trigger Workflow

```bash
watch-run data/inbox \
  --workflow workflows/sample.workflow.json \
  --trigger
```

### Write JSON Event Log

```bash
watch-run data/inbox \
  --workflow workflows/sample.workflow.json \
  --log-json
```

### Trigger, Archive, and Write JSON Event Log

```bash
watch-run data/inbox \
  --workflow workflows/sample.workflow.json \
  --trigger \
  --archive \
  --log-json
```

### Run Once

```bash
watch-run data/inbox \
  --workflow workflows/sample.workflow.json \
  --once
```

### Run Multiple Watch Cycles

```bash
watch-run data/inbox \
  --workflow workflows/sample.workflow.json \
  --interval 2 \
  --max-cycles 3 \
  --log-json
```

## Local Utility Dependencies

```bash
pip install -e ../workflow_automation_mvp
pip install -e ../document_pipeline_mvp
pip install -e ../radar_knowledge_search
```

```bash
which auto-run
which doc-pipe
which radar-search
```

## Project Structure

```text
file_watcher_automation_mvp/
├── data/
│   ├── inbox/
│   ├── processed/
│   └── failed/
├── file_watcher/
│   ├── __init__.py
│   ├── archive.py
│   ├── cli.py
│   ├── contract.py
│   ├── event_builder.py
│   ├── event_log.py
│   ├── watcher.py
│   └── workflow_trigger.py
├── tests/
│   ├── test_archive.py
│   ├── test_cli.py
│   ├── test_event_builder.py
│   ├── test_event_log.py
│   ├── test_watch_options.py
│   ├── test_watcher.py
│   └── test_workflow_trigger.py
├── workflows/
│   └── sample.workflow.json
├── pyproject.toml
├── README.md
└── .gitignore
```

## Roadmap

- [x] M1 Bootstrap
- [x] M2 Watch Contract
- [x] M3 File Detection Layer
- [x] M4 Event Builder
- [x] M5 Workflow Trigger Executor
- [x] M6 Processed / Failed Archive
- [x] M7 JSON Event Log
- [x] M8 CLI Watch Options
- [x] M9 Packaging & README
- [x] M10 v0.1.0 Release

## Version

Current Version:

v0.1.0

Status:

Release
