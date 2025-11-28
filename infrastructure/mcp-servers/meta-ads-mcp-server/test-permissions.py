#!/usr/bin/env python3
"""
Test what permissions are available
"""
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('META_APP_ID')
APP_SECRET = os.getenv('META_APP_SECRET')

print("=" * 60)
print("Meta App Permissions Check")
print("=" * 60)
print()
print(f"App ID: {APP_ID}")
print()
print("For Development mode apps, the following approaches work:")
print()
print("Option 1: Add yourself as a Test User")
print("  - Go to Roles → Test Users in your app")
print("  - Add a test user")
print("  - Test users automatically get all permissions")
print()
print("Option 2: Use Marketing API with Business Integration")
print("  - Go to Use Cases → Manage app ads")
print("  - Make sure your Business Portfolio is connected")
print("  - Add your ad account IDs")
print("  - This gives you access without needing ads_read approval")
print()
print("Option 3: Request Advanced Access")
print("  - Go to App Review → Permissions and Features")
print("  - Request 'ads_read' permission")
print("  - Requires verification (may take time)")
print()
print("=" * 60)
print()
print("Quick fix: Let's try using the access token directly")
print("from Meta's Graph API Explorer instead of OAuth")
print()
