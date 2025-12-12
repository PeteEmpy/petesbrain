#!/bin/bash
# PetesBrain Error Aggregator
# Scans all agent logs for recent errors and displays summary by agent
# Usage: ./check-recent-errors.sh [hours-back]
# Default: last 24 hours

HOURS_BACK=${1:-24}
LOG_DIR="$HOME"

echo "======================================"
echo "PetesBrain Error Report"
echo "Scanning last $HOURS_BACK hours"
echo "======================================"
echo ""

TOTAL_ERRORS=0
AGENTS_WITH_ERRORS=0

# Find all petesbrain error log files and count ERROR/CRITICAL/Exception lines
for log_file in "$LOG_DIR"/.petesbrain-*-error.log; do
    [ -f "$log_file" ] || continue

    # Extract agent name from filename
    filename=$(basename "$log_file")
    agent_name="${filename#.petesbrain-}"
    agent_name="${agent_name%-error.log}"

    # Count errors in file (simple line count with error patterns)
    error_count=$(grep -c "ERROR\|CRITICAL\|Exception\|Traceback\|failed\|Failed" "$log_file" 2>/dev/null || echo 0)

    if [ "$error_count" -gt 0 ]; then
        AGENTS_WITH_ERRORS=$((AGENTS_WITH_ERRORS + 1))
        TOTAL_ERRORS=$((TOTAL_ERRORS + error_count))

        # Show agent with error count
        printf "%-40s %5d errors\n" "$agent_name:" "$error_count"
    fi
done

echo ""
echo "======================================"
echo "Summary:"
echo "  Total agents with errors: $AGENTS_WITH_ERRORS"
echo "  Total error lines found: $TOTAL_ERRORS"
echo "======================================"
echo ""

if [ "$TOTAL_ERRORS" -eq 0 ]; then
    echo "✅ No errors found in last $HOURS_BACK hours!"
else
    echo "⚠️  Found errors. View detailed logs:"
    echo ""
    for log_file in "$LOG_DIR"/.petesbrain-*-error.log; do
        [ -f "$log_file" ] || continue
        error_count=$(grep -c "ERROR\|CRITICAL\|Exception\|Traceback\|failed\|Failed" "$log_file" 2>/dev/null || echo 0)
        if [ "$error_count" -gt 0 ]; then
            filename=$(basename "$log_file")
            agent_name="${filename#.petesbrain-}"
            agent_name="${agent_name%-error.log}"
            echo "  tail ~/.petesbrain-${agent_name}-error.log"
        fi
    done
fi
