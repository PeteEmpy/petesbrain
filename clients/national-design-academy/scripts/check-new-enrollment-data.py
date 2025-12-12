#!/usr/bin/env python3
"""
Monitor NDA enrollment data folder for new files from Kelly Rawson.
Creates a Google Task when new enrollment data is detected.

Run manually or via LaunchAgent to check for updates weekly.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

# Define paths
CLIENT_DIR = Path('/Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy')
ATTACHMENTS_DIR = CLIENT_DIR / 'emails' / 'attachments'
ANALYSIS_DIR = CLIENT_DIR / 'enrolments'
STATE_FILE = ANALYSIS_DIR / '.last-analyzed-date.json'

def get_latest_attachment_date():
    """Get the most recent date folder in attachments directory."""
    if not ATTACHMENTS_DIR.exists():
        print(f"❌ Attachments directory not found: {ATTACHMENTS_DIR}")
        return None
    
    # Look for folders with YYYY-MM-DD pattern
    date_folders = []
    for item in ATTACHMENTS_DIR.iterdir():
        if item.is_dir():
            # Check if folder name matches date pattern
            if re.match(r'^\d{4}-\d{2}-\d{2}$', item.name):
                date_folders.append(item.name)
    
    if not date_folders:
        print("ℹ️  No dated folders found in attachments directory")
        return None
    
    # Return the most recent date
    return max(date_folders)

def get_last_analyzed_date():
    """Get the date of the last analyzed enrollment data."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('last_analyzed_date')
        except:
            pass
    return None

def save_analyzed_date(date_str):
    """Save the date of the latest analyzed data."""
    with open(STATE_FILE, 'w') as f:
        json.dump({
            'last_analyzed_date': date_str,
            'updated': datetime.now().isoformat()
        }, f, indent=2)

def check_for_new_data():
    """Check if new enrollment data from Kelly has arrived."""
    
    print("=" * 80)
    print("NDA ENROLLMENT DATA - NEW FILE CHECK")
    print("=" * 80)
    
    latest_date = get_latest_attachment_date()
    last_analyzed = get_last_analyzed_date()
    
    print(f"\n📂 Latest attachment folder:  {latest_date if latest_date else 'None found'}")
    print(f"📊 Last analyzed data:       {last_analyzed if last_analyzed else 'Never analyzed'}")
    
    if not latest_date:
        print("\n⚠️  No new attachment folders detected")
        return False
    
    if latest_date == last_analyzed:
        print(f"\n✅ No new data (last analyzed: {last_analyzed})")
        return False
    
    # New data detected!
    print(f"\n🚨 NEW ENROLLMENT DATA DETECTED!")
    print(f"   Latest folder: {latest_date}")
    print(f"   Last analyzed: {last_analyzed}")
    
    # Verify files exist
    attachment_path = ATTACHMENTS_DIR / latest_date
    required_files = [
        'NDA UK Enrolments 25-26.xlsx',
        'NDA International Enrolments 25-26.xlsx'
    ]
    
    missing_files = []
    for filename in required_files:
        if not (attachment_path / filename).exists():
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {missing_files}")
        return False
    
    print(f"\n✅ All required files present:")
    for filename in required_files:
        filepath = attachment_path / filename
        size_kb = filepath.stat().st_size / 1024
        print(f"   • {filename} ({size_kb:.1f} KB)")
    
    return True

def main():
    has_new_data = check_for_new_data()
    
    if has_new_data:
        print("\n" + "=" * 80)
        print("ACTION REQUIRED")
        print("=" * 80)
        print("\n🔔 New enrollment data from Kelly Rawson detected!")
        print("\nNext steps:")
        print("  1. Run analysis using: python3 clients/national-design-academy/scripts/analyze-enrollment-data.py")
        print("  2. Or use checklist: clients/national-design-academy/documents/NEW-DATA-ARRIVAL-CHECKLIST.md")
        print("  3. Follow ENROLLMENT-DATA-PROTOCOL.md for full workflow")
        
        # In a real scenario, this would create a Google Task
        # For now, just indicate what would happen
        print("\n📌 (Would create Google Task reminder if integrated with Google Tasks API)")
        
        return 1  # Exit with error code to indicate action needed
    else:
        print("\n✅ No action needed - data is current")
        return 0

if __name__ == '__main__':
    exit(main())
