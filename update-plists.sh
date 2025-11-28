#!/bin/bash

# Update all LaunchAgent plists with new agent paths
# Run this manually after verifying migration worked

cd ~/Library/LaunchAgents

for plist in com.petesbrain.*.plist; do
    echo "Updating: $plist"

    # Update shared/scripts paths
    sed -i '' 's|shared/scripts/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/content-sync paths
    sed -i '' 's|agents/content-sync/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/reporting paths
    sed -i '' 's|agents/reporting/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/system paths
    sed -i '' 's|agents/system/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/performance-monitoring paths
    sed -i '' 's|agents/performance-monitoring/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/budget-tracking paths
    sed -i '' 's|agents/budget-tracking/\(.*\)\.py|agents/\1/\1.py|g' "$plist"

    # Update agents/product-feeds paths
    sed -i '' 's|agents/product-feeds/\(.*\)\.py|agents/\1/\1.py|g' "$plist"
done

echo "✓ Plist files updated"
echo "Run: launchctl unload ~/Library/LaunchAgents/com.petesbrain.*.plist"
echo "Then: launchctl load ~/Library/LaunchAgents/com.petesbrain.*.plist"
