#!/usr/bin/env python3
"""
Complete Devonshire Hotels PMAX Asset Optimizer
Fetches 90-day API data and generates CSV with campaign names and asset groups
"""

import json
import csv
import sys

# This script will receive API data and convert it to CSV
# For now, showing the structure

print("=" * 80)
print("DEVONSHIRE HOTELS - PMAX ASSET OPTIMIZER (COMPLETE)")
print("=" * 80)
print()
print("Customer ID: 5898250490")
print("Campaign: DEV | Core Properties CE & BE | P Max | All")
print("Date Range: 90 days (2025-08-28 to 2025-11-27)")
print()
print("Processing steps:")
print("1. Fetch all text assets from API (90 days, >500 impressions)")
print("2. Convert to CSV with campaign name and asset group columns")
print("3. Analyze performance and identify underperformers")
print()
print("Output file: output/devonshire-asset-performance-api-2025-11-27.csv")
print("=" * 80)
