#!/usr/bin/env python3
"""
Superspace Orders Timeline Visualization
Shows daily orders from Oct 1 - Nov 24, 2025 with key Google Ads changes marked
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Load the data
df = pd.read_csv('/Users/administrator/Downloads/Orders over time - 2025-10-01 - 2025-11-24.csv')

# Clean and prepare data
df['Day'] = pd.to_datetime(df['Day'])
df = df[df['Orders'] > 0]  # Remove empty rows

# Create the figure
plt.figure(figsize=(16, 8))
ax = plt.gca()

# Plot the orders line
plt.plot(df['Day'], df['Orders'], linewidth=2, color='#2E86AB', marker='o', markersize=3, label='Daily Orders')

# Add key Google Ads changes as vertical lines
# Format: (date, label, color, y_offset_multiplier)
changes = [
    ('2025-11-06', 'Budget scaling begins\n(~£5k → £12k/day)', '#28a745', 0.35),
    ('2025-11-13', 'Peak scaling: £12,010/day\n+140% budget increase\nDemand Gen scaled to £600/day', '#ffc107', 0.75),
    ('2025-11-17', 'Stock crisis identified\nROAS 550% → 600%', '#dc3545', 0.95),
    ('2025-11-20', 'Phase 1: -20% budget\n£14,460 → £11,568/day\nDemand Gen PAUSED', '#dc3545', 0.55),
    ('2025-11-21', 'Phase 2: -10% budget\n£11,568 → £10,397/day', '#dc3545', 0.15),
    ('2025-11-24', 'Phase 3: -10% budget\n£10,397 → £9,357/day', '#dc3545', 0.25),
]

# Get max orders for positioning
max_orders = df['Orders'].max()

for date_str, label, color, y_multiplier in changes:
    date = pd.to_datetime(date_str)
    plt.axvline(x=date, color=color, linestyle='--', linewidth=2, alpha=0.7)

    # Position labels at different heights to avoid overlap
    y_pos = max_orders * y_multiplier

    # Add text label
    plt.text(date, y_pos, label,
             rotation=0, verticalalignment='bottom', horizontalalignment='center',
             fontsize=8, bbox=dict(boxstyle='round,pad=0.5', facecolor=color, alpha=0.3))

# Formatting
plt.xlabel('Date', fontsize=12, fontweight='bold')
plt.ylabel('Daily Orders', fontsize=12, fontweight='bold')
plt.title('Superspace US Orders Timeline: Oct 1 - Nov 24, 2025\nGoogle Ads Budget Changes Impact',
          fontsize=14, fontweight='bold', pad=20)

# Format x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.xticks(rotation=45, ha='right')

# Add grid
plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)

# Add legend
plt.legend(loc='upper left', fontsize=10)

# Annotate key periods
plt.text(pd.to_datetime('2025-10-15'), 900, 'Pre-scaling baseline\n~100-150 orders/day',
         fontsize=10, bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.3))

plt.text(pd.to_datetime('2025-11-14'), 1050, 'Peak performance\n600-1,000+ orders/day',
         fontsize=10, bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffc107', alpha=0.3))

# Adjust layout
plt.tight_layout()

# Save the figure
output_path = '/Users/administrator/Documents/PetesBrain/clients/superspace/analysis/orders-timeline-oct-nov-2025.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Chart saved to: {output_path}")

# Show the plot
plt.show()

# Print summary statistics
print("\n" + "="*60)
print("SUMMARY STATISTICS")
print("="*60)

periods = [
    ("Pre-scaling (Oct 1-6)", df[df['Day'] < '2025-11-06']),
    ("Scaling phase (Nov 6-13)", df[(df['Day'] >= '2025-11-06') & (df['Day'] < '2025-11-13')]),
    ("Peak (Nov 13-17)", df[(df['Day'] >= '2025-11-13') & (df['Day'] < '2025-11-17')]),
    ("Post-throttle (Nov 17-24)", df[df['Day'] >= '2025-11-17']),
]

for period_name, period_df in periods:
    if len(period_df) > 0:
        print(f"\n{period_name}:")
        print(f"  Average orders/day: {period_df['Orders'].mean():.0f}")
        print(f"  Peak orders: {period_df['Orders'].max():.0f}")
        print(f"  Total orders: {period_df['Orders'].sum():.0f}")
