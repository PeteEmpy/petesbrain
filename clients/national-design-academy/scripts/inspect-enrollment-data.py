#!/usr/bin/env python3
"""
Diagnostic script to inspect enrollment data structure
"""

import openpyxl
from datetime import datetime

# Read UK enrollments
print("📊 UK ENROLLMENTS FILE STRUCTURE:")
print("=" * 60)
uk_wb = openpyxl.load_workbook('../enrolments/NDA-UK-Enrolments-ACTIVE.xlsx')
uk_ws = uk_wb.active
uk_rows = list(uk_ws.rows)

print(f"Total rows: {len(uk_rows)}")
print(f"\nHeader row:")
header = [cell.value for cell in uk_rows[0]]
print(f"  {header}")

print(f"\nFirst 5 data rows:")
for i, row in enumerate(uk_rows[1:6], 1):
    values = [cell.value for cell in row[:5]]  # First 5 columns
    print(f"  Row {i}: {values}")
    if row[0].value:
        print(f"         Date type: {type(row[0].value)}, Value: {row[0].value}")

print(f"\n" + "=" * 60)
print("🌍 INTERNATIONAL ENROLLMENTS FILE STRUCTURE:")
print("=" * 60)
intl_wb = openpyxl.load_workbook('../enrolments/NDA-International-Enrolments-ACTIVE.xlsx')
intl_ws = intl_wb.active
intl_rows = list(intl_ws.rows)

print(f"Total rows: {len(intl_rows)}")
print(f"\nHeader row:")
header = [cell.value for cell in intl_rows[0]]
print(f"  {header}")

print(f"\nFirst 5 data rows:")
for i, row in enumerate(intl_rows[1:6], 1):
    values = [cell.value for cell in row[:5]]  # First 5 columns
    print(f"  Row {i}: {values}")
    if row[0].value:
        print(f"         Date type: {type(row[0].value)}, Value: {row[0].value}")

# Count rows by month
print(f"\n" + "=" * 60)
print("📅 ENROLLMENT COUNTS BY MONTH (2025):")
print("=" * 60)

from collections import defaultdict
uk_by_month = defaultdict(int)
intl_by_month = defaultdict(int)

for row in uk_rows[1:]:
    if row[0].value:
        date_val = row[0].value
        if isinstance(date_val, datetime):
            if date_val.year == 2025:
                uk_by_month[date_val.month] += 1

for row in intl_rows[1:]:
    if row[0].value:
        date_val = row[0].value
        if isinstance(date_val, datetime):
            if date_val.year == 2025:
                intl_by_month[date_val.month] += 1

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
print(f"\n{'Month':<10} {'UK':>6} {'Intl':>6} {'Total':>6}")
print("-" * 32)
for month_num in range(1, 13):
    uk_count = uk_by_month[month_num]
    intl_count = intl_by_month[month_num]
    print(f"{months[month_num-1]:<10} {uk_count:>6} {intl_count:>6} {uk_count+intl_count:>6}")

total_uk = sum(uk_by_month.values())
total_intl = sum(intl_by_month.values())
print("-" * 32)
print(f"{'TOTAL 2025':<10} {total_uk:>6} {total_intl:>6} {total_uk+total_intl:>6}")
