#!/bin/bash
# File Organizer Skill - Easy ad-hoc execution
# Usage: organize-files [--dry-run] [--client CLIENT_NAME] [--undo LOG_FILE]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

# Use system Python3
python3 "$SCRIPT_DIR/file-organizer.py" "$@"

