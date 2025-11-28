#!/bin/bash
# Quick setup script - run after getting Meta credentials

if [ $# -ne 2 ]; then
    echo "Usage: ./quick-setup.sh <APP_ID> <APP_SECRET>"
    echo "Example: ./quick-setup.sh 1234567890 abc123def456"
    exit 1
fi

APP_ID=$1
APP_SECRET=$2

echo "Creating .env file..."
cat > .env << EOF
# Meta (Facebook) Ads API Configuration
META_APP_ID=$APP_ID
META_APP_SECRET=$APP_SECRET
EOF

chmod 600 .env
echo "✅ .env file created"

echo ""
echo "Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"

echo ""
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✅ Dependencies installed"

echo ""
echo "Testing configuration..."
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('✅ App ID loaded:', os.getenv('META_APP_ID')[:4] + '...')
print('✅ Configuration successful!')
"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next: Restart Claude Desktop and test with:"
echo '  "List all my Meta ad accounts"'
echo ""

