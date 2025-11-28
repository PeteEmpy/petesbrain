#!/usr/bin/env python3
"""
Organize search terms data by country from Google Sheets data.
Reads the two batches of data saved earlier and organizes them by country.
"""

def get_country(campaign_name):
    """Extract country code from campaign name."""
    if "SUP | US |" in campaign_name:
        return "US"
    elif "SUP | UK |" in campaign_name:
        return "UK"
    elif "SUP | AU |" in campaign_name:
        return "AUS"
    return None

def get_campaign_type(match_type, campaign_name):
    """Determine campaign type from match type and campaign name."""
    if match_type == "Performance Max":
        return "Performance Max"
    elif "Shopping" in campaign_name:
        return "Shopping"
    elif "P Max" in campaign_name:
        return "Performance Max"
    elif "Search" in campaign_name:
        return "Search"
    return "Unknown"

def is_data_row(row):
    """Check if row is actual data (not header or total)."""
    if len(row) < 4:
        return False
    search_term = row[0]
    # Skip header rows and total rows
    if search_term in ["Search term", "Total: Filtered search terms", "Total: Account",
                       "Total: Search", "Total: Demand Gen", "Total: Shopping",
                       "Total: Performance Max", "Search terms report - Superspace", ""]:
        return False
    if search_term.startswith("Total:") or search_term.startswith("1 January"):
        return False
    return True

# This will be run after saving batch data
# For now, just export the logic so we can use it in the next step
print("Helper functions defined.")
print("get_country: Extract 'US', 'UK', or 'AUS' from campaign name")
print("get_campaign_type: Determine 'Search', 'Shopping', or 'Performance Max'")
print("is_data_row: Filter out header/total rows")
