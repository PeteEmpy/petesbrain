"""Setup OAuth for Google Tasks + Calendar with combined scopes"""

import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Request both Tasks and Calendar scopes (including write access for calendar)
SCOPES = [
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/calendar",  # Full access (read + write)
]


def main():
    """Run OAuth flow for Tasks + Calendar and test connections."""
    print("Setting up Google Tasks + Calendar OAuth...")
    print("This will open a browser window for authentication.")
    print("You'll need to grant access to BOTH Google Tasks and Google Calendar.")
    print()

    server_dir = Path(__file__).parent
    token_path = server_dir / "token.json"
    credentials_path = server_dir / "credentials.json"

    try:
        if not credentials_path.exists():
            raise ValueError(f"OAuth credentials file not found at {credentials_path}")

        # Run OAuth flow with both scopes
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_path), SCOPES
        )
        creds = flow.run_local_server(port=0)

        # Save credentials
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

        print("✓ OAuth setup successful!")
        print()

        # Test Tasks API
        print("Testing Google Tasks connection:")
        tasks_service = build("tasks", "v1", credentials=creds)
        results = tasks_service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])

        if not items:
            print("  No task lists found.")
        else:
            print(f"  ✓ Found {len(items)} task list(s)")
            for item in items[:3]:
                print(f"    - {item['title']}")

        print()

        # Test Calendar API
        print("Testing Google Calendar connection:")
        calendar_service = build("calendar", "v3", credentials=creds)
        calendar_list = calendar_service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])

        if not calendars:
            print("  No calendars found.")
        else:
            print(f"  ✓ Found {len(calendars)} calendar(s)")
            for cal in calendars[:3]:
                print(f"    - {cal.get('summary', 'Unknown')}")

        print()
        print("✓ Both Google Tasks and Google Calendar are ready!")
        print("  Token saved with combined scopes.")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
