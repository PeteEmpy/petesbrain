#!/bin/bash
# CRITICAL SECURITY FIX - December 22, 2025
# Remove exposed credentials from git history and local files

set -e

echo "========================================="
echo "SECURITY FIX - Remove Exposed Credentials"
echo "========================================="
echo ""

# Step 1: Delete remaining rollback snapshots locally
echo "Step 1: Removing remaining rollback snapshot directories..."
rm -rf infrastructure/rollback-snapshots/20251211_143600
rm -rf infrastructure/rollback-snapshots/20251211_150404
rm -rf infrastructure/rollback-snapshots/20251211_150719
rm -rf infrastructure/rollback-snapshots/20251216_080003
rm -rf infrastructure/rollback-snapshots/20251217_080000
rm -rf infrastructure/rollback-snapshots/20251218_080003
rm -rf infrastructure/rollback-snapshots/20251219_080002
rm -rf infrastructure/rollback-snapshots/20251221_080001
rm -rf infrastructure/rollback-snapshots/20251222_080001

echo "✅ Local snapshot directories removed"
echo ""

# Step 2: Stage all deletions
echo "Step 2: Staging all file deletions..."
git add -A
echo "✅ Changes staged"
echo ""

# Step 3: Commit the removals
echo "Step 3: Creating commit..."
git commit -m "Security: Remove rollback snapshots containing credentials

CRITICAL SECURITY FIX:
- Removed all rollback snapshot directories
- These contained exposed service account credentials
- Google Cloud Platform flagged publicly exposed keys
- This commit removes them from working directory

Next steps:
1. Purge from git history using git filter-repo
2. Rotate all service account keys
3. Update .gitignore to prevent future exposure"

echo "✅ Commit created"
echo ""

echo "========================================="
echo "⚠️  NEXT STEPS (Manual):"
echo "========================================="
echo ""
echo "1. Install git-filter-repo:"
echo "   brew install git-filter-repo"
echo ""
echo "2. Purge credentials from history:"
echo "   git filter-repo --path infrastructure/rollback-snapshots --invert-paths --force"
echo ""
echo "3. Force push to GitHub (REWRITES HISTORY):"
echo "   git push origin main --force"
echo ""
echo "4. Rotate ALL service account keys in Google Cloud Console:"
echo "   - mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
echo "   - Any other service accounts that were in snapshots"
echo ""
echo "5. Update local credentials with new keys"
echo ""
echo "========================================="
