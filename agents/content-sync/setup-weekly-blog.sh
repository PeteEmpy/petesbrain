#!/bin/bash
# Setup script for Weekly Blog Generator

echo "=========================================="
echo "Weekly Blog Generator Setup"
echo "=========================================="
echo ""

# Check if WordPress credentials are provided
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "Usage: ./setup-weekly-blog.sh <wordpress_url> <username> <app_password>"
    echo ""
    echo "Example:"
    echo "  ./setup-weekly-blog.sh https://roksys.co.uk peter abc1-def2-ghij-klmn"
    echo ""
    echo "To get Application Password:"
    echo "  1. Log into WordPress: https://roksys.co.uk/wp-admin"
    echo "  2. Go to Users → Your Profile"
    echo "  3. Scroll to Application Passwords"
    echo "  4. Create new password named 'Weekly Blog Generator'"
    echo "  5. Copy the password (shown only once!)"
    exit 1
fi

WP_URL="$1"
WP_USERNAME="$2"
WP_PASSWORD="$3"

echo "Configuring WordPress connection..."
echo "  URL: $WP_URL"
echo "  Username: $WP_USERNAME"
echo ""

# Update LaunchAgent plist
PLIST_FILE="$HOME/Library/LaunchAgents/com.petesbrain.weekly-blog-generator.plist"
SOURCE_PLIST="/Users/administrator/Documents/PetesBrain/agents/launchagents/com.petesbrain.weekly-blog-generator.plist"

# Copy plist if it doesn't exist
if [ ! -f "$PLIST_FILE" ]; then
    echo "Copying LaunchAgent plist..."
    cp "$SOURCE_PLIST" "$PLIST_FILE"
fi

# Update WordPress credentials in plist
echo "Updating WordPress credentials..."
sed -i '' "s|YOUR_WORDPRESS_URL_HERE|$WP_URL|g" "$PLIST_FILE"
sed -i '' "s|YOUR_WORDPRESS_USERNAME_HERE|$WP_USERNAME|g" "$PLIST_FILE"
sed -i '' "s|YOUR_WORDPRESS_APP_PASSWORD_HERE|$WP_PASSWORD|g" "$PLIST_FILE"

echo "✓ LaunchAgent configured"
echo ""

# Load LaunchAgent
echo "Loading LaunchAgent..."
launchctl unload "$PLIST_FILE" 2>/dev/null
launchctl load "$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo "✓ LaunchAgent loaded successfully"
    echo ""
    echo "The blog generator will run every Monday at 8:00 AM"
    echo "Posts will be scheduled for 9:00 AM publication"
    echo ""
    echo "To test manually:"
    echo "  cd /Users/administrator/Documents/PetesBrain"
    echo "  export WORDPRESS_URL=\"$WP_URL\""
    echo "  export WORDPRESS_USERNAME=\"$WP_USERNAME\""
    echo "  export WORDPRESS_APP_PASSWORD=\"$WP_PASSWORD\""
    echo "  /Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3 agents/weekly-blog-generator/weekly-blog-generator.py"
    echo ""
    echo "Check logs:"
    echo "  tail -f ~/.petesbrain-weekly-blog.log"
else
    echo "✗ Failed to load LaunchAgent"
    echo "Check the plist file: $PLIST_FILE"
    exit 1
fi

