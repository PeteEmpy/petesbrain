#!/usr/bin/env python3
"""
Setup script for Google Slides API credentials.

This script helps you set up the Google API credentials needed for
automated monthly report generation.

Usage:
    python3 setup_google_api.py
"""

import os
import sys
import json

CREDENTIALS_DIR = os.path.expanduser('~/Documents/PetesBrain/shared/credentials')
CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, 'google-slides-credentials.json')


def main():
    print("=" * 70)
    print("Google Slides API Setup")
    print("=" * 70)

    print("\nThis script will help you set up Google API credentials for")
    print("automated monthly report generation.")

    print("\n" + "=" * 70)
    print("STEP 1: Create Google Cloud Project")
    print("=" * 70)

    print("""
1. Go to: https://console.cloud.google.com/
2. Create a new project (or select existing one): "PetesBrain Reports"
3. Note the project ID
""")

    input("Press Enter when you've created the project...")

    print("\n" + "=" * 70)
    print("STEP 2: Enable Google Slides API")
    print("=" * 70)

    print("""
1. Go to: https://console.cloud.google.com/apis/library
2. Search for "Google Slides API"
3. Click "Enable"
4. Also enable "Google Drive API" (needed for file access)
""")

    input("Press Enter when you've enabled the APIs...")

    print("\n" + "=" * 70)
    print("STEP 3: Create Service Account")
    print("=" * 70)

    print("""
1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click "Create Service Account"
3. Name: "monthly-report-generator"
4. Description: "Automated monthly report generation for Devonshire Hotels"
5. Click "Create and Continue"
6. Skip granting roles (click "Continue")
7. Click "Done"
""")

    input("Press Enter when you've created the service account...")

    print("\n" + "=" * 70)
    print("STEP 4: Create and Download Key")
    print("=" * 70)

    print("""
1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON"
5. Click "Create"
6. A JSON file will download
""")

    input("Press Enter when you've downloaded the key...")

    print("\n" + "=" * 70)
    print("STEP 5: Move Credentials File")
    print("=" * 70)

    # Create credentials directory if it doesn't exist
    os.makedirs(CREDENTIALS_DIR, exist_ok=True)

    print(f"""
Move the downloaded JSON file to:
{CREDENTIALS_FILE}

Or run this command:
    mv ~/Downloads/[your-key-file].json {CREDENTIALS_FILE}
""")

    input("Press Enter when you've moved the file...")

    # Check if file exists
    if os.path.exists(CREDENTIALS_FILE):
        print("\n✅ Credentials file found!")

        # Validate JSON
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                creds = json.load(f)

            if 'type' in creds and creds['type'] == 'service_account':
                print("✅ Credentials file is valid!")
                print(f"   Service account: {creds.get('client_email')}")
            else:
                print("❌ Invalid credentials file format")
                sys.exit(1)

        except Exception as e:
            print(f"❌ Error reading credentials: {e}")
            sys.exit(1)
    else:
        print(f"\n❌ Credentials file not found at: {CREDENTIALS_FILE}")
        print("Please move the file and run this script again.")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("STEP 6: Share Folder with Service Account (IMPORTANT!)")
    print("=" * 70)

    with open(CREDENTIALS_FILE, 'r') as f:
        creds = json.load(f)
        service_email = creds.get('client_email')

    print(f"""
The service account needs permission to create presentations in your Google Drive.

Service Account Email:
    {service_email}

To grant access:
1. Go to your Google Drive
2. Find the folder where you want reports created (or create one)
3. Right-click → Share
4. Paste the service account email above
5. Give it "Editor" access
6. Click "Send"

This allows the script to create presentations in that folder.
""")

    input("Press Enter when you've shared the folder...")

    print("\n" + "=" * 70)
    print("STEP 7: Install Python Dependencies")
    print("=" * 70)

    print("""
Installing required Python packages...
""")

    os.system("pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib")

    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)

    print(f"""
Your Google Slides API is now configured!

Credentials stored at:
    {CREDENTIALS_FILE}

You can now run the report generator:
    python3 generate_devonshire_slides.py --month 2025-10

The generated presentation will appear in the Google Drive folder
you shared with the service account.
""")


if __name__ == '__main__':
    main()
