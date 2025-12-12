#!/usr/bin/env python3
"""
Add data validation dropdowns to NDA PMax Asset Performance Analysis sheet
Run this script to add dropdown lists to column M (Alternative Options)
"""

from google.auth.oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1VlsVKPPydqh5w70l9QmV6oT8B7qlw6YKMDgrcp2Zpto'

ALTERNATIVES = {
    "M2": [  # Study Interior Design
        "Change careers with design",
        "Transform your creative",
        "Build a design career in weeks",
        "Accredited design diploma",
        "AIM & Ofqual recognised",
        "Flexible study around your",
        "Design spaces, inspire people",
        "Your design journey starts",
        "Learn design your own way",
        "Start your design career today",
        "Enrol in design diploma now",
        "Begin designing professionally",
        "35+ years design education",
        "Design academy trusted by 35K+",
        "Industry-led design education"
    ],
    "M3": [  # Interior Design Diploma
        "Turn design passion into",
        "Master interior design skills",
        "Get recognised design",
        "AIM-accredited diploma course",
        "Ofqual-recognised",
        "Professional interior design",
        "Design beautiful interior",
        "Create stunning room designs",
        "Master the art of interiors",
        "Get your design diploma today",
        "Qualify as interior designer",
        "Claim your design",
        "National Design Academy",
        "Award-winning design programme",
        "Globally recognised design"
    ],
    "M4": [  # Interior Design Courses
        "Learn design in your own way",
        "Design career courses that fit",
        "Study design around your",
        "Accredited interior design",
        "Nationally recognised design",
        "Industry-standard design",
        "Design courses that inspire",
        "Learn design from industry",
        "Where design passion comes",
        "Enrol in design courses today",
        "Start learning interior design",
        "Begin your design education",
        "35 years design education",
        "Design courses trusted",
        "Academy-led design training"
    ]
}

def get_service():
    """Authenticate and get Google Sheets service"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('sheets', 'v4', credentials=creds)

def add_data_validation(service, cell_range, items):
    """Add data validation dropdown to a cell"""
    requests = {
        "requests": [
            {
                "setDataValidation": {
                    "range": {
                        "sheetId": 0,  # First sheet
                        "ranges": [{"name": cell_range}]
                    },
                    "rule": {
                        "condition": {
                            "type": "ONE_OF_LIST",
                            "values": [{"userEnteredValue": item} for item in items]
                        },
                        "inputMessage": "Select an alternative headline",
                        "strict": True,
                        "showCustomUi": True
                    }
                }
            }
        ]
    }
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=requests
    ).execute()
    print(f"✅ Added dropdown to {cell_range}")

if __name__ == '__main__':
    print("Adding data validation dropdowns...")
    service = get_service()
    
    for cell_range, alternatives in ALTERNATIVES.items():
        add_data_validation(service, cell_range, alternatives)
    
    print("\n✅ All dropdowns added successfully!")
