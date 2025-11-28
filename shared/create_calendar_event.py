#!/usr/bin/env python3
"""
Create a calendar event in Google Calendar
"""
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json
import os
import sys

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_PATH = '/Users/administrator/Documents/PetesBrain/shared/calendar_token.json'
CREDS_PATH = '/Users/administrator/Documents/PetesBrain/infrastructure/mcp-servers/google-tasks-mcp-server/credentials.json'

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'r') as f:
            token_data = json.load(f)
        creds = Credentials(
            token=token_data.get('token'),
            refresh_token=token_data.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=token_data.get('client_id'),
            client_secret=token_data.get('client_secret'),
            scopes=SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        token_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
        with open(TOKEN_PATH, 'w') as f:
            json.dump(token_data, f)

    return creds

def create_event(summary, location, start_time, end_time, calendar_name='Peter - Work'):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    # Find the calendar
    calendars = service.calendarList().list().execute()
    calendar_id = None

    for calendar in calendars.get('items', []):
        if calendar_name in calendar.get('summary', ''):
            calendar_id = calendar['id']
            break

    if not calendar_id:
        print(f"ERROR: Could not find calendar '{calendar_name}'")
        return None

    event = {
        'summary': summary,
        'location': location,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Europe/London',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Europe/London',
        },
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return event

if __name__ == '__main__':
    # Get today's date at 2 PM
    today = datetime.now()
    start_time = today.replace(hour=14, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)

    event = create_event(
        summary="Haircut at Master Barber's",
        location="Master Barber's",
        start_time=start_time,
        end_time=end_time
    )

    if event:
        print(f"✓ Event created: {event.get('htmlLink')}")
        print(f"✓ Haircut scheduled for {start_time.strftime('%I:%M %p')} today")
