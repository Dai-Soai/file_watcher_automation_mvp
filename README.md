# File Watcher Automation MVP

A lightweight folder watcher automation utility for triggering RADAR document workflows when new files appear.

## Current Status

M3 File Detection Layer.

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

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

watch-run data/inbox --workflow workflows/sample.workflow.json

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
- [] M4 Event Builder
- [] M5 Workflow Trigger Executor
- [] M6 Processed / Failed Archive
- [] M7 JSON Event Log
- [] M8 CLI Watch Options
- [] M9 Packaging & README
- [] M10 v0.1.0 Release
