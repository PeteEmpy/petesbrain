# October 2025 International Students - ACTUAL DATA

# From spreadsheet analysis above:
oct_2025_intl_enrollments = 50  # Actual count

# Course fees in USD (from spreadsheet):
fees_usd = [
    1250, 1850, 1850, 1250, 1250, 1250, 325, 1250, 3500, 3225,  # 10 students
    325, 1250, 1050, 1850, 2425, 3225, 3500, 2100, 1850, 3500,  # 10 students  
    1250, 325, 2425, 2675, 1850, 8250, 1250, 1250, 1250, 7650,  # 10 students
    3225, 325, 2425, 2100, 3500, 3225, 3225, 7650, 7650, 7950,  # 10 students
    8600, 1250, 1850, 3225, 7650, 7650, 1250, 1850, 2100, 2100  # 10 students
]

# USD to GBP conversion rate (approximate Oct 2025): 1 USD = 0.79 GBP
usd_to_gbp = 0.79

# Calculate total revenue - using FULL course fees
total_revenue_usd = sum(fees_usd)
total_revenue_gbp = total_revenue_usd * usd_to_gbp

# Google Ads spend
oct_2025_intl_spend = 22254.96

# Calculate metrics
revenue_per_enrol = total_revenue_gbp / oct_2025_intl_enrollments
cost_per_enrol = oct_2025_intl_spend / oct_2025_intl_enrollments
roas = (total_revenue_gbp / oct_2025_intl_spend) * 100

print("="*70)
print("OCTOBER 2025 INTERNATIONAL - ACTUAL SPREADSHEET DATA")
print("="*70)

print(f"\nENROLLMENTS: {oct_2025_intl_enrollments}")

print(f"\nREVENUE (Full Course Fees):")
print(f"  Total USD: ${total_revenue_usd:,}")
print(f"  Total GBP: £{total_revenue_gbp:,.2f} (@ 0.79 USD/GBP)")
print(f"  Revenue per Enrollment: £{revenue_per_enrol:,.2f}")

print(f"\nGOOGLE ADS:")
print(f"  Spend: £{oct_2025_intl_spend:,.2f}")
print(f"  Cost per Enrollment: £{cost_per_enrol:,.2f}")

print(f"\nROAS (based on full course fees): {roas:.0f}%")

print("\n" + "="*70)

# Payment method breakdown from the data
full_payment_count = 40  # Count of "Y" in Fee Paid in Full column
installment_count = 10  # Count of "N" in Fee Paid in Full column

print("\nPAYMENT METHOD BREAKDOWN:")
print(f"  Paid in Full: {full_payment_count} students ({full_payment_count/50*100:.0f}%)")
print(f"  Installments: {installment_count} students ({installment_count/50*100:.0f}%)")

print("\n" + "="*70)

# Course price analysis
from collections import Counter
fee_counts = Counter(fees_usd)

print("\nCOURSE PRICE DISTRIBUTION (October International):")
for price in sorted(fee_counts.keys()):
    count = fee_counts[price]
    gbp_price = price * usd_to_gbp
    print(f"  ${price:,} (£{gbp_price:,.0f}): {count} students ({count/50*100:.0f}%)")

print("\n" + "="*70)

avg_fee_usd = total_revenue_usd / oct_2025_intl_enrollments
avg_fee_gbp = total_revenue_gbp / oct_2025_intl_enrollments

print(f"\nAVERAGE COURSE FEE: ${avg_fee_usd:,.0f} (£{avg_fee_gbp:,.0f})")
print("="*70)

