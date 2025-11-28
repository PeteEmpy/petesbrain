import json

# October 2025 - International enrollments (from actual data)
oct_2025_intl_enrollments = 50

# October 2024 - International enrollments (estimate based on YTD proportion)
# YTD 2024-25: 43 international of 104 total = 41.3% international rate
# October 2024 total estimated: ~45 students
# October 2024 international estimated: 45 × 0.413 = ~19 students
oct_2024_intl_enrollments_estimate = 19

# Revenue calculations
# YTD 2025-26: Dubai Income = £404,160 (51% of total)
# YTD 2024-25: Dubai Income = £289,296 (39% of total)

# October 2025 revenue (from Paul's data)
oct_2025_total_revenue = 250572
oct_2025_intl_revenue = round(oct_2025_total_revenue * 0.51)  # 51% international

# October 2024 revenue (from Paul's data)
oct_2024_total_revenue = 305026
oct_2024_intl_revenue = round(oct_2024_total_revenue * 0.39)  # 39% international

# Revenue per enrollment
oct_2025_rev_per_enrolment = round(oct_2025_intl_revenue / oct_2025_intl_enrollments)
oct_2024_rev_per_enrolment = round(oct_2024_intl_revenue / oct_2024_intl_enrollments_estimate)

print("\n" + "="*60)
print("INTERNATIONAL STUDENTS - OCTOBER COMPARISON")
print("="*60)
print(f"\nOCTOBER 2024:")
print(f"  Enrollments: {oct_2024_intl_enrollments_estimate} (estimated)")
print(f"  Revenue: £{oct_2024_intl_revenue:,}")
print(f"  Revenue per enrollment: £{oct_2024_rev_per_enrolment:,}")

print(f"\nOCTOBER 2025:")
print(f"  Enrollments: {oct_2025_intl_enrollments} (actual)")
print(f"  Revenue: £{oct_2025_intl_revenue:,}")
print(f"  Revenue per enrollment: £{oct_2025_rev_per_enrolment:,}")

enrollment_change = oct_2025_intl_enrollments - oct_2024_intl_enrollments_estimate
enrollment_change_pct = round((enrollment_change / oct_2024_intl_enrollments_estimate) * 100, 1)

revenue_change = oct_2025_intl_revenue - oct_2024_intl_revenue
revenue_change_pct = round((revenue_change / oct_2024_intl_revenue) * 100, 1)

rev_per_enrol_change = oct_2025_rev_per_enrolment - oct_2024_rev_per_enrolment
rev_per_enrol_change_pct = round((rev_per_enrol_change / oct_2024_rev_per_enrolment) * 100, 1)

print(f"\nCHANGES (Oct 2024 → Oct 2025):")
print(f"  Enrollments: +{enrollment_change} (+{enrollment_change_pct}%)")
print(f"  Revenue: £{revenue_change:,} ({revenue_change_pct:+.1f}%)")
print(f"  Revenue per enrollment: £{rev_per_enrol_change:,} ({rev_per_enrol_change_pct:+.1f}%)")

print("\n" + "="*60)

# Now get Google Ads spend for international campaigns in October
print("\nNEXT: Calculating cost per enrollment...")
print("Need to query Google Ads for international campaign spend in October")
print("="*60 + "\n")

