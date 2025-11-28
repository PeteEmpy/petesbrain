"""
Google Calendar Client for PetesBrain

Simple wrapper around Google Calendar API for fetching today's calendar events
from PetesBrain agents.
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Calendar scope - token may have readonly or full access, either works for reading
CALENDAR_SCOPE = "https://www.googleapis.com/auth/calendar"


class GoogleCalendarClient:
    """Client for interacting with Google Calendar API"""

    def __init__(self):
        """Initialize the Google Calendar client with OAuth credentials"""
        self.service = self._get_service()

    def _get_service(self):
        """Create and return a Google Calendar service instance using OAuth"""
        # Use same credentials as Tasks (they share the same OAuth app)
        token_path = Path(__file__).parent.parent / "infrastructure" / "mcp-servers" / "google-tasks-mcp-server" / "token.json"
        credentials_path = Path(__file__).parent.parent / "infrastructure" / "mcp-servers" / "google-tasks-mcp-server" / "credentials.json"

        creds = None

        # Load existing token if available - don't enforce specific scopes
        # Token may have calendar.readonly or calendar (full), either works for reading
        if token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(token_path))
            except Exception as e:
                # Token file exists but is invalid - will re-authenticate
                print(f"Warning: Could not load existing token: {e}")
                creds = None

        # Refresh token if expired
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    # Try to refresh the token
                    creds.refresh(Request())
                    # Save refreshed token immediately
                    with open(token_path, "w") as token_file:
                        token_file.write(creds.to_json())
                except Exception as e:
                    # Refresh failed - need to re-authenticate
                    raise ValueError(
                        f"OAuth credentials not valid. Token refresh failed: {e}\n"
                        f"Token path: {token_path}\n"
                        f"Calendar API requires the same OAuth setup as Tasks.\n"
                        f"Please run setup_oauth_with_calendar.py to re-authenticate."
                    )
            else:
                raise ValueError(
                    f"OAuth credentials not valid. Calendar API requires the same OAuth setup as Tasks.\n"
                    f"Token path: {token_path}"
                )

        return build("calendar", "v3", credentials=creds)

    # Calendars to query for daily briefing
    CALENDARS = [
        ('c_03826f839a86edf1e8e9ac0f4e0719a1759f8b4589a3da52ea10f2be01b18482@group.calendar.google.com', 'Peter - Work'),
        ('g2vv8treq9lc0h9981m1a3tcuaun6hgk@import.calendar.google.com', 'Family'),
    ]

    def get_today_events(self):
        """
        Get today's calendar events from Peter - Work and Family calendars.

        Returns:
            list: List of event dictionaries with summary, start, end times, sorted by start time
        """
        try:
            # Get start and end of today
            now = datetime.now()
            today_start = datetime(now.year, now.month, now.day, 0, 0, 0).isoformat() + 'Z'
            today_end = datetime(now.year, now.month, now.day, 23, 59, 59).isoformat() + 'Z'

            all_events = []

            # Query each calendar
            for calendar_id, calendar_name in self.CALENDARS:
                try:
                    events_result = self.service.events().list(
                        calendarId=calendar_id,
                        timeMin=today_start,
                        timeMax=today_end,
                        singleEvents=True,
                        orderBy='startTime'
                    ).execute()

                    events = events_result.get('items', [])

                    # Format events
                    for event in events:
                        start = event['start'].get('dateTime', event['start'].get('date'))
                        end = event['end'].get('dateTime', event['end'].get('date'))

                        all_events.append({
                            'summary': event.get('summary', 'Untitled Event'),
                            'start': start,
                            'end': end,
                            'description': event.get('description', ''),
                            'location': event.get('location', ''),
                            'calendar': calendar_name
                        })
                except Exception as e:
                    print(f"Error fetching from {calendar_name}: {e}")

            # Sort all events by start time
            all_events.sort(key=lambda x: x['start'])

            return all_events

        except Exception as e:
            print(f"Error fetching calendar events: {e}")
            return []


def get_today_events():
    """Standalone function to get today's events - for use by other scripts"""
    client = GoogleCalendarClient()
    return client.get_today_events()


# Quick test function
if __name__ == "__main__":
    print("Testing Google Calendar Client...")

    client = GoogleCalendarClient()

    # Test: Get today's events
    events = client.get_today_events()

    if events:
        print(f"\\n📅 Found {len(events)} event(s) for today:\\n")
        for event in events:
            start_time = event['start']
            if 'T' in start_time:
                # Parse datetime
                dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                time_str = dt.strftime('%I:%M %p')
            else:
                time_str = "All day"

            print(f"   {time_str} - {event['summary']}")
    else:
        print("\\n📅 No events found for today")
