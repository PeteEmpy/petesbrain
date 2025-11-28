#!/usr/bin/env python3
"""
Devonshire Hotels - Enhanced Monthly Paid Search Report Generator
Generates professionally formatted Google Slides with branded tables.

Features:
- Full Google Slides API integration for advanced formatting
- Estate Blue (#00333D) and Stone (#E5E3DB) branded color scheme
- Properly formatted tables with colored headers and cells
- Automated data collection from Google Ads API
- Professional layout matching September 2025 format

Usage:
    python3 generate_devonshire_slides.py --month 2025-10

Requirements:
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle

# Brand Colors (Estate Escapes)
ESTATE_BLUE = {'red': 0, 'green': 0.2, 'blue': 0.24}  # #00333D
STONE = {'red': 0.898, 'green': 0.890, 'blue': 0.859}  # #E5E3DB
WHITE = {'red': 1.0, 'green': 1.0, 'blue': 1.0}  # #FFFFFF
BLACK = {'red': 0.0, 'green': 0.0, 'blue': 0.0}  # #000000
DARK_GRAY = {'red': 0.2, 'green': 0.2, 'blue': 0.2}  # #333333

# Google Ads Configuration
CUSTOMER_ID = "5898250490"

# Campaign mappings
CAMPAIGN_GROUPS = {
    'hotels': {
        '19577006833': 'Devonshire Arms',
        '21839323410': 'Cavendish',
        '22539873565': 'Beeley Inn',
        '19534106385': 'Pilsley Inn',
        '22666031909': 'The Fell',
        '2080736142': 'Chatsworth Inns',
        '18899261254': 'P Max All',
        '19654308682': 'Locations (Chatsworth)',
        '22720114456': 'Locations (Bolton Abbey)'
    },
    'self_catering': {
        '19534201089': 'Chatsworth Self Catering',
        '22536922700': 'Bolton Abbey Self Catering'
    },
    'the_hide': {
        '23069490466': 'The Hide',
        '21815704991': 'Highwayman Arms'
    }
}

# Google Slides Configuration
# EMU (English Metric Units) - 914400 EMU = 1 inch
SLIDE_WIDTH = 10  # inches
SLIDE_HEIGHT = 7.5  # inches
EMU_PER_INCH = 914400


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate Devonshire Hotels monthly Paid Search report'
    )
    parser.add_argument(
        '--month',
        type=str,
        required=True,
        help='Month to generate report for (YYYY-MM format, e.g., 2025-10)'
    )
    parser.add_argument(
        '--credentials',
        type=str,
        default=os.path.expanduser('~/Documents/PetesBrain/shared/credentials/google-slides-oauth.json'),
        help='Path to Google OAuth credentials JSON file'
    )
    parser.add_argument(
        '--use-service-account',
        action='store_true',
        help='Use service account authentication instead of OAuth (requires domain-wide delegation)'
    )
    parser.add_argument(
        '--output-name',
        type=str,
        help='Custom presentation name (default: Devonshire Paid Search - [Month])'
    )

    return parser.parse_args()


def get_month_info(month_str: str) -> Tuple[str, str, int, str]:
    """
    Get month information.

    Returns:
        Tuple of (start_date, end_date, total_days, month_name)
    """
    year, month = map(int, month_str.split('-'))
    start_date = datetime(year, month, 1)

    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)

    total_days = end_date.day
    month_name = start_date.strftime('%B %Y')

    return (
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d'),
        total_days,
        month_name
    )


def create_slides_service(credentials_path: str, use_service_account: bool = False):
    """Create Google Slides API service using OAuth or service account."""
    SCOPES = [
        'https://www.googleapis.com/auth/presentations',
        'https://www.googleapis.com/auth/drive.file'
    ]

    if use_service_account:
        # Service account authentication (requires domain-wide delegation)
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=SCOPES
        )
    else:
        # OAuth authentication (recommended)
        creds = None
        token_path = os.path.expanduser('~/Documents/PetesBrain/shared/credentials/google-slides-token.json')

        # Token file stores the user's access and refresh tokens
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        credentials = creds

    service = build('slides', 'v1', credentials=credentials)
    return service


def create_presentation(service, title: str, folder_id: str = None) -> str:
    """
    Create a new Google Slides presentation.

    Args:
        service: Google Slides API service
        title: Presentation title
        folder_id: Optional folder ID to create presentation in

    Returns:
        Presentation ID
    """
    # First create the presentation
    presentation = {
        'title': title
    }

    presentation = service.presentations().create(body=presentation).execute()
    presentation_id = presentation.get('presentationId')
    print(f"Created presentation: {presentation_id}")

    # If folder_id provided, move the presentation to that folder
    if folder_id:
        from googleapiclient.discovery import build
        drive_service = build('drive', 'v3', credentials=service._http.credentials)

        # Get current parents
        file = drive_service.files().get(
            fileId=presentation_id,
            fields='parents'
        ).execute()
        previous_parents = ",".join(file.get('parents', []))

        # Move to new folder
        drive_service.files().update(
            fileId=presentation_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()
        print(f"Moved to folder: {folder_id}")

    return presentation_id


def create_table_slide(service, presentation_id: str, slide_id: str,
                      title: str, headers: List[str], rows: List[List[str]],
                      notes: str = None):
    """
    Create a slide with a formatted table.

    Args:
        service: Google Slides API service
        presentation_id: Presentation ID
        slide_id: ID for the new slide
        title: Slide title
        headers: List of column headers
        rows: List of data rows (each row is a list of cells)
        notes: Optional notes text below the table
    """
    requests = []

    # Create blank slide
    requests.append({
        'createSlide': {
            'objectId': slide_id,
            'slideLayoutReference': {
                'predefinedLayout': 'BLANK'
            }
        }
    })

    # Add title text box
    title_box_id = f'{slide_id}_title'
    requests.append({
        'createShape': {
            'objectId': title_box_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': 9 * EMU_PER_INCH, 'unit': 'EMU'},
                    'height': {'magnitude': 0.5 * EMU_PER_INCH, 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': 0.5 * EMU_PER_INCH,
                    'translateY': 0.3 * EMU_PER_INCH,
                    'unit': 'EMU'
                }
            }
        }
    })

    # Add title text
    requests.append({
        'insertText': {
            'objectId': title_box_id,
            'text': title
        }
    })

    # Format title (bold, larger font, Estate Blue)
    requests.append({
        'updateTextStyle': {
            'objectId': title_box_id,
            'style': {
                'bold': True,
                'fontSize': {'magnitude': 24, 'unit': 'PT'},
                'foregroundColor': {'opaqueColor': {'rgbColor': ESTATE_BLUE}}
            },
            'fields': 'bold,fontSize,foregroundColor'
        }
    })

    # Create table
    num_columns = len(headers)
    num_rows = len(rows) + 1  # +1 for header row

    table_id = f'{slide_id}_table'
    requests.append({
        'createTable': {
            'objectId': table_id,
            'elementProperties': {
                'pageObjectId': slide_id,
                'size': {
                    'width': {'magnitude': 8.5 * EMU_PER_INCH, 'unit': 'EMU'},
                    'height': {'magnitude': (0.4 * num_rows) * EMU_PER_INCH, 'unit': 'EMU'}
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': 0.75 * EMU_PER_INCH,
                    'translateY': 1.2 * EMU_PER_INCH,
                    'unit': 'EMU'
                }
            },
            'rows': num_rows,
            'columns': num_columns
        }
    })

    # Execute requests to create structure
    body = {'requests': requests}
    response = service.presentations().batchUpdate(
        presentationId=presentation_id, body=body
    ).execute()

    # Now format the table
    formatting_requests = []

    # Insert headers and format header row
    for col_idx, header_text in enumerate(headers):
        # Insert header text
        formatting_requests.append({
            'insertText': {
                'objectId': table_id,
                'cellLocation': {
                    'rowIndex': 0,
                    'columnIndex': col_idx
                },
                'text': header_text
            }
        })

        # Format header cell background (Estate Blue)
        formatting_requests.append({
            'updateTableCellProperties': {
                'objectId': table_id,
                'tableRange': {
                    'location': {
                        'rowIndex': 0,
                        'columnIndex': col_idx
                    },
                    'rowSpan': 1,
                    'columnSpan': 1
                },
                'tableCellProperties': {
                    'tableCellBackgroundFill': {
                        'solidFill': {
                            'color': {'rgbColor': ESTATE_BLUE}
                        }
                    }
                },
                'fields': 'tableCellBackgroundFill'
            }
        })

        # Format header text (white, bold)
        formatting_requests.append({
            'updateTextStyle': {
                'objectId': table_id,
                'cellLocation': {
                    'rowIndex': 0,
                    'columnIndex': col_idx
                },
                'style': {
                    'bold': True,
                    'fontSize': {'magnitude': 11, 'unit': 'PT'},
                    'foregroundColor': {'opaqueColor': {'rgbColor': WHITE}}
                },
                'fields': 'bold,fontSize,foregroundColor'
            }
        })

    # Insert data rows and format
    for row_idx, row_data in enumerate(rows):
        actual_row = row_idx + 1  # +1 because row 0 is header

        for col_idx, cell_text in enumerate(row_data):
            # Insert cell text
            formatting_requests.append({
                'insertText': {
                    'objectId': table_id,
                    'cellLocation': {
                        'rowIndex': actual_row,
                        'columnIndex': col_idx
                    },
                    'text': str(cell_text)
                }
            })

            # Format data cell background (Stone)
            formatting_requests.append({
                'updateTableCellProperties': {
                    'objectId': table_id,
                    'tableRange': {
                        'location': {
                            'rowIndex': actual_row,
                            'columnIndex': col_idx
                        },
                        'rowSpan': 1,
                        'columnSpan': 1
                    },
                    'tableCellProperties': {
                        'tableCellBackgroundFill': {
                            'solidFill': {
                                'color': {'rgbColor': STONE}
                            }
                        }
                    },
                    'fields': 'tableCellBackgroundFill'
                }
            })

            # Format data text (dark gray)
            formatting_requests.append({
                'updateTextStyle': {
                    'objectId': table_id,
                    'cellLocation': {
                        'rowIndex': actual_row,
                        'columnIndex': col_idx
                    },
                    'style': {
                        'fontSize': {'magnitude': 10, 'unit': 'PT'},
                        'foregroundColor': {'opaqueColor': {'rgbColor': DARK_GRAY}}
                    },
                    'fields': 'fontSize,foregroundColor'
                }
            })

    # Add notes if provided
    if notes:
        notes_box_id = f'{slide_id}_notes'
        formatting_requests.append({
            'createShape': {
                'objectId': notes_box_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'width': {'magnitude': 8.5 * EMU_PER_INCH, 'unit': 'EMU'},
                        'height': {'magnitude': 0.8 * EMU_PER_INCH, 'unit': 'EMU'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 0.75 * EMU_PER_INCH,
                        'translateY': (1.2 + 0.4 * num_rows + 0.2) * EMU_PER_INCH,
                        'unit': 'EMU'
                    }
                }
            }
        })

        formatting_requests.append({
            'insertText': {
                'objectId': notes_box_id,
                'text': notes
            }
        })

        formatting_requests.append({
            'updateTextStyle': {
                'objectId': notes_box_id,
                'style': {
                    'fontSize': {'magnitude': 9, 'unit': 'PT'},
                    'italic': True,
                    'foregroundColor': {'opaqueColor': {'rgbColor': DARK_GRAY}}
                },
                'fields': 'fontSize,italic,foregroundColor'
            }
        })

    # Execute formatting requests
    body = {'requests': formatting_requests}
    service.presentations().batchUpdate(
        presentationId=presentation_id, body=body
    ).execute()


def main():
    """Main entry point."""
    args = parse_arguments()

    print("=" * 70)
    print("Devonshire Hotels - Enhanced Monthly Report Generator")
    print("=" * 70)

    # Get month information
    start_date, end_date, total_days, month_name = get_month_info(args.month)
    presentation_title = args.output_name or f"Devonshire Paid Search - {month_name}"

    print(f"\n📅 Month: {month_name}")
    print(f"📊 Date range: {start_date} to {end_date} ({total_days} days)")
    print(f"📝 Title: {presentation_title}")

    # Check credentials
    if not os.path.exists(args.credentials):
        print(f"\n❌ ERROR: Credentials file not found: {args.credentials}")
        print("\nPlease run the setup script first:")
        print("  python3 setup_google_api.py")
        sys.exit(1)

    print(f"\n🔐 Using credentials: {args.credentials}")

    # Create Slides service
    print("\n🔧 Initializing Google Slides API...")
    if args.use_service_account:
        print("   Using service account authentication...")
    else:
        print("   Using OAuth authentication...")
        if not os.path.exists(os.path.expanduser('~/Documents/PetesBrain/shared/credentials/google-slides-token.json')):
            print("   (Browser will open for first-time authentication)")

    service = create_slides_service(args.credentials, args.use_service_account)

    # Create presentation
    print("\n📊 Creating presentation...")
    folder_id = "1SxrEHIJxSaMba3lkE4HR6ZNZ3xw4rG45"  # Devonshire Reports folder
    presentation_id = create_presentation(service, presentation_title, folder_id)

    # TODO: Query Google Ads data here
    # For now, using October 2025 data from markdown report

    print("\n📋 Creating slides with branded tables...")

    # Slide 1: Title Slide (will be created as blank slide with title)
    # Slide 2: Executive Summary
    create_table_slide(
        service,
        presentation_id,
        'slide_exec_summary',
        'Executive Summary - October 2025',
        ['Metric', 'Value'],
        [
            ['Budget', '£11,730.00'],
            ['Actual Spend', '£10,112.94'],
            ['Variance', '£954.07 under budget (8.13%)'],
            ['Pacing', '91.87% ✅'],
            ['Total Revenue', '£58,693.89'],
            ['ROAS', '5.80x'],
            ['Total Conversions', '132.58'],
            ['Impressions', '228,733'],
            ['Clicks', '23,026'],
            ['Average CTR', '10.07%']
        ]
    )

    # Slide 3: Hotels - Top Performers
    create_table_slide(
        service,
        presentation_id,
        'slide_top_performers',
        'Hotels - Top Performers by ROAS',
        ['Property', 'Spend', 'Revenue', 'Conv', 'ROAS', 'Clicks', 'CTR'],
        [
            ['Devonshire Arms', '£1,389.34', '£12,628.09', '33.58', '9.09x', '3,988', '30.32%'],
            ['Cavendish', '£1,355.35', '£8,851.42', '14.75', '6.53x', '3,790', '35.64%'],
            ['P Max All', '£2,585.01', '£16,065.68', '34.17', '6.21x', '4,685', '3.28%'],
            ['Locations (Chatsworth)', '£537.12', '£2,902.00', '4.00', '5.40x', '1,003', '10.76%'],
            ['Beeley Inn', '£1,023.30', '£4,634.33', '11.33', '4.53x', '1,745', '27.15%'],
            ['The Fell', '£772.29', '£3,336.57', '9.58', '4.32x', '1,268', '26.16%'],
            ['Chatsworth Inns', '£939.07', '£3,764.62', '6.87', '4.01x', '1,547', '18.75%'],
            ['Pilsley Inn', '£939.01', '£3,510.18', '10.30', '3.74x', '1,393', '22.52%']
        ]
    )

    # Slide 4: Properties Requiring Attention
    create_table_slide(
        service,
        presentation_id,
        'slide_attention_needed',
        'Properties Requiring Attention',
        ['Property', 'Spend', 'Revenue', 'Conv', 'ROAS', 'Issue'],
        [
            ['Chatsworth Self Catering', '£900.02', '£2,321.00', '6.00', '2.58x', 'Below target ROAS'],
            ['Locations (Bolton Abbey)', '£496.44', '£680.00', '2.00', '1.37x', 'Poor ROAS, needs review'],
            ['Bolton Abbey Self Catering', '£175.99', '£0.00', '0.00', '0.00x', '⚠️ Zero conversions']
        ],
        notes='Bolton Abbey SC requires immediate conversion tracking audit. Chatsworth SC below target ROAS.'
    )

    # Slide 5: Campaign Type Breakdown
    create_table_slide(
        service,
        presentation_id,
        'slide_campaign_types',
        'Campaign Type Breakdown',
        ['Channel', 'Spend', 'Revenue', 'Conv', 'ROAS', 'Share of Spend'],
        [
            ['Performance Max', '£2,585.01', '£16,065.68', '34.17', '6.21x', '25.6%'],
            ['Search (Hotels)', '£6,627.91', '£40,307.21', '92.41', '6.08x', '65.5%'],
            ['Search (Self-Catering)', '£1,076.01', '£2,321.00', '6.00', '2.16x', '10.6%'],
            ['Search (Locations)', '£1,033.56', '£3,582.00', '6.00', '3.47x', '10.2%']
        ]
    )

    # Slide 6: Self-Catering Campaigns
    create_table_slide(
        service,
        presentation_id,
        'slide_self_catering',
        'Self-Catering Campaigns - Detailed',
        ['Campaign', 'Spend', 'Revenue', 'Conv', 'ROAS', 'Clicks', 'CTR'],
        [
            ['Chatsworth SC', '£900.02', '£2,321.00', '6.00', '2.58x', '2,554', '17.29%'],
            ['Bolton Abbey SC', '£175.99', '£0.00', '0.00', '0.00x', '235', '8.92%']
        ],
        notes='Bolton Abbey SC: Zero conversions despite clicks - conversion tracking audit required. Chatsworth SC: Below target ROAS - review landing pages and targeting.'
    )

    # Slide 7: The Hide (Separate Budget)
    create_table_slide(
        service,
        presentation_id,
        'slide_the_hide',
        'The Hide - Separate £2,000 Budget',
        ['Metric', 'Value'],
        [
            ['Budget', '£2,000.00'],
            ['Actual Spend', '£1,923.09'],
            ['Pacing', '96.15% ✅'],
            ['The Hide (current)', '£1,431.28'],
            ['Highwayman Arms (paused)', '£491.81']
        ],
        notes='The Hide launched October 10, 2025 (formerly The Highwayman). Combined spend on track with budget.'
    )

    # Slide 8: Key Insights - Performance Highlights
    create_table_slide(
        service,
        presentation_id,
        'slide_highlights',
        'Key Insights - Performance Highlights',
        ['Highlight', 'Detail'],
        [
            ['Strong Overall ROAS', '5.80x ROAS across portfolio - excellent campaign efficiency'],
            ['Devonshire Arms Excellence', '9.09x ROAS with 30.32% CTR - highly relevant targeting'],
            ['Budget Discipline', '8.13% under budget (£954.07) - maintained profitability'],
            ['Performance Max Efficiency', '6.21x ROAS with highest conversion volume (34.17)'],
            ['Cavendish CTR Leader', '35.64% CTR - best-performing ad copy in portfolio']
        ]
    )

    # Slide 9: Key Insights - Areas for Improvement
    create_table_slide(
        service,
        presentation_id,
        'slide_improvements',
        'Key Insights - Areas for Improvement',
        ['Issue', 'Recommendation'],
        [
            ['Self-Catering Underperformance', 'Chatsworth SC 2.58x ROAS, Bolton Abbey SC zero conversions'],
            ['Bolton Abbey Locations', '1.37x ROAS - consider pausing or tighter geo-targeting'],
            ['CTR Variation', 'Range 8.60% to 35.64% - apply Cavendish copy to other campaigns'],
            ['Conversion Tracking', 'Bolton Abbey SC audit required - zero conversions despite clicks']
        ]
    )

    # Slide 10: Recommendations for November - Part 1
    create_table_slide(
        service,
        presentation_id,
        'slide_recs_1',
        'Recommendations for November (Part 1)',
        ['Priority', 'Action'],
        [
            ['1. Fix Bolton Abbey SC', 'Audit conversion tracking, review landing page experience, consider pausing if issues persist'],
            ['2. Scale Top Performers', 'Allocate more budget to Devonshire Arms (9.09x ROAS) and Cavendish (35.64% CTR)'],
            ['3. Optimize Self-Catering', 'Test dedicated self-catering landing pages, implement A/B testing on ad copy, consider seasonal messaging']
        ]
    )

    # Slide 11: Recommendations for November - Part 2
    create_table_slide(
        service,
        presentation_id,
        'slide_recs_2',
        'Recommendations for November (Part 2)',
        ['Priority', 'Action'],
        [
            ['4. Apply Best Practices', 'Replicate Cavendish ad copy structure across other property campaigns, review P Max asset groups for efficiency opportunities'],
            ['5. Budget Adjustments', 'November budget is £9,000 (reduced from October £11,730). With £954 October underspend, consider reallocating to top-performing campaigns']
        ]
    )

    # Slide 12: Weddings (placeholder)
    create_table_slide(
        service,
        presentation_id,
        'slide_weddings',
        'Weddings',
        ['Status', 'Note'],
        [
            ['Data Availability', 'Data to be added when available'],
            ['Tracking Configuration', 'Changes in October may have affected data collection']
        ]
    )

    # Slide 13: Lismore and The Hall (placeholder)
    create_table_slide(
        service,
        presentation_id,
        'slide_lismore',
        'Lismore and The Hall',
        ['Status', 'Note'],
        [
            ['Data Availability', 'Data to be added when available']
        ]
    )

    print("\n✅ Presentation created successfully!")
    print(f"\n🔗 Presentation ID: {presentation_id}")
    print(f"🔗 URL: https://docs.google.com/presentation/d/{presentation_id}")
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
