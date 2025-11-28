#!/usr/bin/env python3
"""
Create cost per enrollment charts for NDA - August-November 2025
Generates two bar charts: UK and ROW (Rest of World)
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

# Load enrollment data
with open('/tmp/nda_enrollments_aug_nov_2025.json', 'r') as f:
    enrollment_data = json.load(f)

# Load cost data
with open('/tmp/nda_costs_aug_nov_2025.json', 'r') as f:
    cost_data = json.load(f)

# Calculate cost per enrollment
months = ['2025-08', '2025-09', '2025-10', '2025-11']
month_labels = ['August', 'September', 'October', 'November']

uk_cpe = []
row_cpe = []

print("=== COST PER ENROLLMENT (Aug-Nov 2025) ===\n")
print(f"{'Month':<12} {'Region':<8} {'Cost':>12} {'Enrollments':>12} {'Cost/Enr':>12}")
print("-" * 65)

for month in months:
    # UK
    uk_cost = cost_data['uk'][month]
    uk_enr = enrollment_data['uk'].get(month, 0)
    uk_cpe_value = uk_cost / uk_enr if uk_enr > 0 else 0
    uk_cpe.append(uk_cpe_value)

    month_name = month_labels[months.index(month)]
    print(f"{month_name:<12} {'UK':<8} £{uk_cost:>10,.2f} {uk_enr:>12} £{uk_cpe_value:>10,.2f}")

    # ROW
    row_cost = cost_data['row'][month]
    row_enr = enrollment_data['row'].get(month, 0)
    row_cpe_value = row_cost / row_enr if row_enr > 0 else 0
    row_cpe.append(row_cpe_value)

    print(f"{'':<12} {'ROW':<8} £{row_cost:>10,.2f} {row_enr:>12} £{row_cpe_value:>10,.2f}")
    print()

# Calculate averages
uk_total_cost = sum(cost_data['uk'].values())
uk_total_enr = sum(enrollment_data['uk'].values())
uk_avg_cpe = uk_total_cost / uk_total_enr

row_total_cost = sum(cost_data['row'].values())
row_total_enr = sum(enrollment_data['row'].values())
row_avg_cpe = row_total_cost / row_total_enr

print("-" * 65)
print(f"{'AVERAGE':<12} {'UK':<8} £{uk_total_cost:>10,.2f} {uk_total_enr:>12} £{uk_avg_cpe:>10,.2f}")
print(f"{'':12} {'ROW':<8} £{row_total_cost:>10,.2f} {row_total_enr:>12} £{row_avg_cpe:>10,.2f}")

# Roksys brand colors
roksys_blue = '#2E5EAA'  # Primary blue
roksys_orange = '#FF6B35'  # Accent orange

# Create figure with two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Cost Per Enrollment - National Design Academy (Aug-Nov 2025)',
             fontsize=16, fontweight='bold', y=0.98)

# UK Chart
x_pos = range(len(months))
bars1 = ax1.bar(x_pos, uk_cpe, color=roksys_blue, edgecolor='black', linewidth=0.7)
ax1.set_xlabel('Month', fontsize=12, fontweight='bold')
ax1.set_ylabel('Cost Per Enrollment (£)', fontsize=12, fontweight='bold')
ax1.set_title('UK Cost Per Enrollment', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(month_labels, rotation=0)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_axisbelow(True)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars1, uk_cpe)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'£{value:,.0f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add average line
ax1.axhline(y=uk_avg_cpe, color='red', linestyle='--', linewidth=2, label=f'Average: £{uk_avg_cpe:,.0f}')
ax1.legend(loc='upper right', fontsize=10)

# ROW Chart
bars2 = ax2.bar(x_pos, row_cpe, color=roksys_orange, edgecolor='black', linewidth=0.7)
ax2.set_xlabel('Month', fontsize=12, fontweight='bold')
ax2.set_ylabel('Cost Per Enrollment (£)', fontsize=12, fontweight='bold')
ax2.set_title('ROW (Rest of World) Cost Per Enrollment', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(month_labels, rotation=0)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.set_axisbelow(True)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars2, row_cpe)):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'£{value:,.0f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add average line
ax2.axhline(y=row_avg_cpe, color='red', linestyle='--', linewidth=2, label=f'Average: £{row_avg_cpe:,.0f}')
ax2.legend(loc='upper right', fontsize=10)

# Add Roksys branding (small logo in corner)
fig.text(0.99, 0.01, 'roksys.co.uk', ha='right', va='bottom',
         fontsize=8, color='gray', style='italic')

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.96])

# Save chart
output_path = 'enrolments/cost-per-enrollment-aug-nov-2025.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"\n✅ Chart saved: {output_path}")

# Save data summary
summary = {
    'period': 'August-November 2025 (Academic Year 2025-26)',
    'uk': {
        'total_cost': uk_total_cost,
        'total_enrollments': uk_total_enr,
        'average_cost_per_enrollment': uk_avg_cpe,
        'monthly': [
            {
                'month': month_labels[i],
                'cost': cost_data['uk'][months[i]],
                'enrollments': enrollment_data['uk'].get(months[i], 0),
                'cost_per_enrollment': uk_cpe[i]
            }
            for i in range(len(months))
        ]
    },
    'row': {
        'total_cost': row_total_cost,
        'total_enrollments': row_total_enr,
        'average_cost_per_enrollment': row_avg_cpe,
        'monthly': [
            {
                'month': month_labels[i],
                'cost': cost_data['row'][months[i]],
                'enrollments': enrollment_data['row'].get(months[i], 0),
                'cost_per_enrollment': row_cpe[i]
            }
            for i in range(len(months))
        ]
    },
    'key_insights': [
        f"UK average: £{uk_avg_cpe:,.2f} per enrollment ({uk_total_enr} total enrollments)",
        f"ROW average: £{row_avg_cpe:,.2f} per enrollment ({row_total_enr} total enrollments)",
        f"ROW is {((row_avg_cpe/uk_avg_cpe - 1) * 100):+.1f}% vs UK" if uk_avg_cpe > 0 else "N/A"
    ]
}

with open('enrolments/cost-per-enrollment-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(f"✅ Summary saved: enrolments/cost-per-enrollment-summary.json")
print(f"\n📊 Analysis complete!")
