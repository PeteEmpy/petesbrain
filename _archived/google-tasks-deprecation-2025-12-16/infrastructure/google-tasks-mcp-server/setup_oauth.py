"""Setup OAuth for Google Tasks MCP Server"""

from tasks_service import tasks_service

def main():
    """Run OAuth flow and test connection."""
    print("Setting up Google Tasks OAuth...")
    print("This will open a browser window for authentication.")
    print()

    try:
        service = tasks_service()
        print("✓ OAuth setup successful!")
        print()

        # Test by listing task lists
        print("Testing connection by listing your task lists:")
        results = service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])

        if not items:
            print("  No task lists found. You may need to create one in Google Tasks first.")
        else:
            print(f"  Found {len(items)} task list(s):")
            for item in items:
                print(f"    - {item['title']} (ID: {item['id']})")

        print()
        print("✓ Google Tasks MCP server is ready!")
        print("  Restart Claude Code to load the server.")

    except Exception as e:
        print(f"✗ Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
