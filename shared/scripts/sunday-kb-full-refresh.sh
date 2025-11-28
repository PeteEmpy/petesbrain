#!/bin/bash
# Sunday Knowledge Base Full Refresh
# Runs KB processor, industry news, and AI news monitors multiple times
# to ensure comprehensive weekend coverage

set -e

VENV="/Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3"
BASE_DIR="/Users/administrator/Documents/PetesBrain"

cd "$BASE_DIR"

echo "=== Sunday KB Full Refresh Starting at $(date) ==="

# Cycle 1
echo "[Cycle 1] Running knowledge-base-processor..."
$VENV agents/knowledge-base-processor/knowledge-base-processor.py
sleep 900  # 15 minutes

echo "[Cycle 1] Running industry-news-monitor..."
$VENV agents/industry-news-monitor/industry-news-monitor.py
sleep 900

echo "[Cycle 1] Running ai-news-monitor..."
$VENV agents/ai-news-monitor/ai-news-monitor.py
sleep 900

# Cycle 2
echo "[Cycle 2] Running knowledge-base-processor..."
$VENV agents/knowledge-base-processor/knowledge-base-processor.py
sleep 900

echo "[Cycle 2] Running industry-news-monitor..."
$VENV agents/industry-news-monitor/industry-news-monitor.py
sleep 900

echo "[Cycle 2] Running ai-news-monitor..."
$VENV agents/ai-news-monitor/ai-news-monitor.py
sleep 900

# Final cycle
echo "[Cycle 3] Running knowledge-base-processor..."
$VENV agents/knowledge-base-processor/knowledge-base-processor.py

echo "=== Sunday KB Full Refresh Completed at $(date) ==="
