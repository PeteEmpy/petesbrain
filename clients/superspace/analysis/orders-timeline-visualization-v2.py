#!/usr/bin/env python3
"""
Superspace Orders Timeline Visualization V2
Shows daily orders from Oct 1 - Nov 24, 2025 with key Google Ads changes marked
Fixed: Labels positioned at alternating heights to avoid overlap
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
plt.figure(figsize=(18, 10))
ax = plt.gca()

# Plot the orders line
plt.plot(df['Day'], df['Orders'], linewidth=2.5, color='#2E86AB', marker='o', markersize=4, label='Daily Orders')

# Add key Google Ads changes as vertical lines
# Format: (date, short_label, color, position: 'top'/'upper'/'mid'/'lower'/'bottom')
changes = [
    ('2025-11-06', 'Budget scaling\n£5k→£12k/day', '#28a745', 'lower'),
    ('2025-11-13', 'Peak: £12k/day\n+140% budget', '#ffc107', 'top'),
    ('2025-11-17', 'Stock crisis\nROAS 550%→600%', '#dc3545', 'top'),
    ('2025-11-20', 'Phase 1: -20%\n£11.6k/day', '#dc3545', 'mid'),
    ('2025-11-21', 'Phase 2: -10%\n£10.4k/day', '#dc3545', 'bottom'),
    ('2025-11-24', 'Phase 3: -10%\n£9.4k/day', '#dc3545', 'lower'),
]

# Define Y positions (as fraction of max)
max_orders = df['Orders'].max()
positions = {
    'top': 0.95,
    'upper': 0.75,
    'mid': 0.50,
    'lower': 0.30,
    'bottom': 0.10
}

for date_str, label, color, position in changes:
    date = pd.to_datetime(date_str)
    plt.axvline(x=date, color=color, linestyle='--', linewidth=2, alpha=0.7, zorder=1)

    # Position labels at specified heights
    y_pos = max_orders * positions[position]

    # Add text label with smaller font and tighter box
    plt.text(date, y_pos, label,
             rotation=0, verticalalignment='center', horizontalalignment='center',
             fontsize=7, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.4', facecolor=color, alpha=0.4, edgecolor=color),
             zorder=3)

# Formatting
plt.xlabel('Date', fontsize=13, fontweight='bold')
plt.ylabel('Daily Orders', fontsize=13, fontweight='bold')
plt.title('Superspace US Orders Timeline: Oct 1 - Nov 24, 2025\nGoogle Ads Budget Changes Impact',
          fontsize=15, fontweight='bold', pad=20)

# Format x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.xticks(rotation=45, ha='right', fontsize=10)

# Add grid
plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.5, zorder=0)

# Add legend
plt.legend(loc='upper left', fontsize=11)

# Adjust layout
plt.tight_layout()

# Save the figure
output_path = '/Users/administrator/Documents/PetesBrain/clients/superspace/analysis/orders-timeline-oct-nov-2025.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Chart saved to: {output_path}")

# Show the plot
plt.show()
