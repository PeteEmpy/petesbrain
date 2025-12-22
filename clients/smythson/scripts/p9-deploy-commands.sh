#!/bin/bash
# P9 Universal Budget Deployer Commands
# Execute these at the specified times

# Navigate to Universal Budget Deployer directory
cd /Users/administrator/Documents/PetesBrain.nosync/tools/universal-budget-deployer

echo "========================================="
echo "P9 BUDGET DEPLOYMENT COMMANDS"
echo "========================================="

# December 22 - Minimal budgets (run at 00:01)
echo ""
echo "DECEMBER 22 - MINIMAL PHASE (00:01)"
echo "Run this command:"
echo "python3 deploy.py --csv ../../../clients/smythson/spreadsheets/p9-dec-22-minimal-roas.csv --execute"

# December 24 - Sale launch (run at 17:45 / 5:45pm)
echo ""
echo "DECEMBER 24 - SALE LAUNCH (17:45 / 5:45pm)"
echo "Run this command:"
echo "python3 deploy.py --csv ../../../clients/smythson/spreadsheets/p9-dec-24-sale-launch-roas.csv --execute"

# December 25 - Christmas Day scale (run at 00:01)
echo ""
echo "DECEMBER 25 - CHRISTMAS DAY (00:01)"
echo "Run this command:"
echo "python3 deploy.py --csv ../../../clients/smythson/spreadsheets/p9-dec-25-christmas-scale.csv --execute"
echo "NOTE: Create p9-dec-25-christmas-scale.csv based on performance"

# December 26 - Boxing Day MAXIMUM (run at 00:01)
echo ""
echo "DECEMBER 26 - BOXING DAY MAXIMUM (00:01)"
echo "Run this command:"
echo "python3 deploy.py --csv ../../../clients/smythson/spreadsheets/p9-dec-26-boxing-day-maximum.csv --execute"

# December 27-28 - Sustained high (run at 00:01 each day)
echo ""
echo "DECEMBER 27-28 - SUSTAINED HIGH"
echo "Run these commands at 00:01 each day:"
echo "python3 deploy.py --csv ../../../clients/smythson/spreadsheets/p9-dec-27-sustained.csv --execute"
echo "python3 deploy.py --csv ../../../clients/smythson/spreadsheets/p9-dec-28-finish.csv --execute"
echo "NOTE: Create these CSVs based on Boxing Day performance"

echo ""
echo "========================================="
echo "VERIFICATION COMMANDS"
echo "========================================="

echo ""
echo "To verify changes WITHOUT executing:"
echo "python3 deploy.py --csv [csv-file] --dry-run"

echo ""
echo "To check current budgets:"
echo "python3 verify_budgets.py --accounts 8573235780,7808690871,7679616761,5556710725"

echo ""
echo "========================================="
echo "CRITICAL REMINDERS"
echo "========================================="
echo "1. Always run --dry-run first to verify"
echo "2. Monitor spend hourly after Dec 24 6pm launch"
echo "3. Have emergency budget ready for top performers"
echo "4. Check ROAS every 4 hours during peak days"
echo "5. Be ready to pause underperformers if needed"

echo ""
echo "TOP PERFORMERS TO WATCH:"
echo "- USA P Max Bags (1502% ROAS)"
echo "- EUR IT Search Brand (1903% ROAS)"
echo "- USA P Max Zombies (1295% ROAS)"
echo "- UK Semi Brand Diaries (943% ROAS)"