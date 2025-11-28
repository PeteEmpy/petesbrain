#!/bin/bash
#
# Setup automatic email sync with cron
# Runs sync 4 times per day: 9am, 12pm, 3pm, 6pm
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SYNC_SCRIPT="$SCRIPT_DIR/sync_emails.py"
LOG_DIR="$SCRIPT_DIR/logs"
VENV_DIR="$SCRIPT_DIR/.venv"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Pete's Brain - Email Sync Cron Setup"
echo "=========================================="
echo ""

# Check if script exists
if [ ! -f "$SYNC_SCRIPT" ]; then
    echo -e "${RED}Error: sync_emails.py not found!${NC}"
    exit 1
fi

# Create log directory
mkdir -p "$LOG_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install -r "$SCRIPT_DIR/requirements.txt"
    echo -e "${GREEN}✓ Virtual environment created${NC}"
    echo ""
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
    echo ""
fi

# Create cron job entry
CRON_CMD="$VENV_DIR/bin/python3 $SYNC_SCRIPT >> $LOG_DIR/sync.log 2>&1"

# Cron schedule: 9am, 12pm, 3pm, 6pm daily
CRON_SCHEDULE="0 9,12,15,18 * * *"

CRON_ENTRY="$CRON_SCHEDULE $CRON_CMD"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "sync_emails.py"; then
    echo -e "${YELLOW}Cron job already exists!${NC}"
    echo ""
    echo "Current cron jobs for email sync:"
    crontab -l | grep "sync_emails.py"
    echo ""
    read -p "Do you want to replace it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi

    # Remove old entry
    (crontab -l 2>/dev/null | grep -v "sync_emails.py") | crontab -
fi

# Add cron job
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo -e "${GREEN}✓ Cron job installed successfully!${NC}"
echo ""
echo "Schedule: 4 times daily (9am, 12pm, 3pm, 6pm)"
echo "Logs: $LOG_DIR/sync.log"
echo ""
echo "To view current crontab:"
echo "  crontab -l"
echo ""
echo "To view sync logs:"
echo "  tail -f $LOG_DIR/sync.log"
echo ""
echo "To remove cron job:"
echo "  crontab -e  # then delete the sync_emails.py line"
echo ""

# Test run
echo -e "${YELLOW}Would you like to run a test sync now? (y/N):${NC} "
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running test sync (dry-run mode)..."
    echo ""
    source "$VENV_DIR/bin/activate"
    python3 "$SYNC_SCRIPT" --dry-run
fi

echo ""
echo -e "${GREEN}Setup complete!${NC}"
