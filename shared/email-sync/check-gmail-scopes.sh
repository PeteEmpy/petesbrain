#!/bin/bash
# Check Gmail OAuth token has correct scopes
# Run this before email sync to verify scopes are correct

TOKEN_FILE="$(dirname "$0")/token.json"

if [ ! -f "$TOKEN_FILE" ]; then
    echo "❌ No token.json file found - need to authenticate"
    exit 1
fi

SCOPES=$(cat "$TOKEN_FILE" | python3 -c "import json, sys; data=json.load(sys.stdin); print(','.join(data.get('scopes', [])))")

# ONLY gmail.modify is needed (includes read access)
if [[ "$SCOPES" == *"gmail.modify"* ]]; then
    echo "✅ Token has correct scope:"
    echo "   - gmail.modify ✓ (includes read, label, and send permissions)"
    exit 0
else
    echo "❌ Token has INCORRECT scopes:"
    echo "   Current: $SCOPES"
    echo "   Required: gmail.modify"
    echo ""
    echo "🔧 FIX: Delete token.json and re-authenticate:"
    echo "   cd ~/Documents/PetesBrain/shared/email-sync"
    echo "   rm token.json"
    echo "   .venv/bin/python3 sync_emails.py"
    exit 1
fi
