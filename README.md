# File Watcher Automation MVP

A lightweight folder watcher automation utility for triggering RADAR document workflows when new files appear.

## Current Status

M7 JSON Event Log.

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

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

watch-run data/inbox --workflow workflows/sample.workflow.json

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

file_watcher_automation_mvp/
├── data/
│   ├── inbox/
│   ├── processed/
│   └── failed/
├── file_watcher/
│   ├── cli.py
│   ├── contract.py
│   └── watcher.py
├── tests/
├── workflows/
├── pyproject.toml
└── README.md

## Roadmap

- [x] M1 Bootstrap
- [x] M2 Watch Contract
- [x] M3 File Detection Layer
- [x] M4 Event Builder
- [x] M5 Workflow Trigger Executor
- [x] M6 Processed / Failed Archive
- [x] M7 JSON Event Log
- [] M8 CLI Watch Options
- [] M9 Packaging & README
- [] M10 v0.1.0 Release
