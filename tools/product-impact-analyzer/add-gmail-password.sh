#!/bin/bash
#
# Add Gmail App Password to Environment
#
# Usage:
#   ./add-gmail-password.sh YOUR_16_CHAR_APP_PASSWORD
#
# To get a Gmail app password:
# 1. Go to https://myaccount.google.com/security
# 2. Enable 2-Step Verification
# 3. Click "App passwords"
# 4. Generate new password for "Mail"
# 5. Copy the 16-character password (no spaces)

set -e

if [ -z "$1" ]; then
    echo "ERROR: Gmail app password required"
    echo ""
    echo "Usage:"
    echo "  ./add-gmail-password.sh YOUR_16_CHAR_APP_PASSWORD"
    echo ""
    echo "To get a Gmail app password:"
    echo "  1. Go to https://myaccount.google.com/security"
    echo "  2. Enable 2-Step Verification (if not already enabled)"
    echo "  3. Search for 'App passwords' or go to:"
    echo "     https://myaccount.google.com/apppasswords"
    echo "  4. Select 'Mail' and 'Mac' (or 'Other')"
    echo "  5. Click 'Generate'"
    echo "  6. Copy the 16-character password (without spaces)"
    echo ""
    exit 1
fi

PASSWORD="$1"

# Validate password format (roughly)
if [ ${#PASSWORD} -lt 16 ]; then
    echo "WARNING: Gmail app passwords are usually 16 characters"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Add to bashrc
echo "" >> ~/.bashrc
echo "# Gmail App Password for automated email delivery" >> ~/.bashrc
echo "export GMAIL_APP_PASSWORD=\"$PASSWORD\"" >> ~/.bashrc

echo "✓ Gmail app password added to ~/.bashrc"
echo ""
echo "To activate in current shell, run:"
echo "  source ~/.bashrc"
echo ""
echo "Or open a new terminal window."
echo ""
echo "To test email delivery:"
echo "  cd /Users/administrator/Documents/PetesBrain/tools/product-impact-analyzer"
echo "  .venv/bin/python3 run_automated_analysis.py --dry-run"
