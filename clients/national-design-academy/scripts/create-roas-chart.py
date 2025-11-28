#!/usr/bin/env python3
"""
Create ROAS visualization chart for country performance
"""

import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from PIL import Image

# File paths
INPUT_CSV = Path("/Users/administrator/Documents/PetesBrain/clients/national-design-academy/data/country-correlation-analysis.csv")
OUTPUT_CHART = Path("/Users/administrator/Documents/PetesBrain/clients/national-design-academy/documents/country-roas-performance.png")

# Professional styling
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
rcParams['font.size'] = 10

def load_data():
    """Load correlation data from CSV"""
    countries = []
    with open(INPUT_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include countries with actual enrollments and ad spend
            if float(row['actual_enrollments']) > 0 and float(row['spend_gbp']) > 0:
                countries.append({
                    'country': row['country'],
                    'roas': float(row['actual_roas_percent']),
                    'spend': float(row['spend_gbp']),
                    'enrollments': int(row['actual_enrollments']),
                    'cpa': float(row['cpa_actual_gbp'])
                })

    return countries

def create_roas_chart(data):
    """Create ROAS scatter plot with bubble sizes"""

    # Sort by ROAS descending
    data.sort(key=lambda x: x['roas'], reverse=True)

    # Take top 15 for readability
    data = data[:15]

    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10), dpi=120)
    fig.patch.set_facecolor('white')

    # === Chart 1: ROAS Bar Chart ===
    ax1.set_facecolor('white')

    countries = [d['country'] for d in data]
    roas_values = [d['roas'] for d in data]

    # Color code: >3000% green, 1000-3000% orange, <1000% red
    colors = []
    for roas in roas_values:
        if roas > 3000:
            colors.append('#2ECC71')  # Green
        elif roas > 1000:
            colors.append('#FF6B35')  # Orange
        else:
            colors.append('#E74C3C')  # Red

    # Horizontal bar chart
    y_pos = np.arange(len(countries))
    bars = ax1.barh(y_pos, roas_values, color=colors, alpha=0.85, edgecolor='#333333', linewidth=1.5)

    # Add value labels
    for i, (bar, roas) in enumerate(zip(bars, roas_values)):
        ax1.text(roas + 100, i, f'{roas:.0f}%',
                va='center', fontsize=11, fontweight='600', color='#333333')

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(countries, fontsize=12)
    ax1.invert_yaxis()  # Top to bottom (highest first)

    ax1.set_xlabel('ROAS %', fontsize=14, fontweight='600', labelpad=15, color='#333333')
    ax1.set_title('Top 15 Countries by ROAS\n(Actual Enrollment Revenue vs Google Ads Spend)',
                 fontsize=16, fontweight='700', pad=20, color='#333333')

    # Add threshold line at 500% (breakeven for most educational orgs)
    ax1.axvline(x=500, color='#999999', linestyle='--', linewidth=2, alpha=0.5, label='500% Target')
    ax1.legend(loc='lower right', fontsize=11)

    ax1.grid(True, alpha=0.2, linestyle='--', linewidth=0.8, color='#DDDDDD', axis='x')
    ax1.set_axisbelow(True)

    # Clean spines
    for spine in ['top', 'right']:
        ax1.spines[spine].set_visible(False)
    for spine in ['bottom', 'left']:
        ax1.spines[spine].set_color('#999999')
        ax1.spines[spine].set_linewidth(2)

    # === Chart 2: Spend vs Enrollments Scatter ===
    ax2.set_facecolor('white')

    spend_values = [d['spend'] for d in data]
    enrollment_values = [d['enrollments'] for d in data]
    bubble_sizes = [r * 2 for r in roas_values]  # Bubble size = ROAS

    # Scatter plot
    scatter = ax2.scatter(spend_values, enrollment_values,
                         s=bubble_sizes,
                         c=roas_values,
                         cmap='RdYlGn',
                         alpha=0.7,
                         edgecolors='#333333',
                         linewidth=2)

    # Add country labels
    for d in data:
        ax2.annotate(d['country'],
                    (d['spend'], d['enrollments']),
                    fontsize=9,
                    ha='center',
                    va='bottom',
                    xytext=(0, 5),
                    textcoords='offset points',
                    fontweight='500',
                    color='#333333')

    ax2.set_xlabel('Google Ads Spend (£)', fontsize=14, fontweight='600', labelpad=15, color='#333333')
    ax2.set_ylabel('Actual Enrollments', fontsize=14, fontweight='600', labelpad=15, color='#333333')
    ax2.set_title('Efficiency Analysis\n(Bubble Size = ROAS %)',
                 fontsize=16, fontweight='700', pad=20, color='#333333')

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax2, pad=0.02)
    cbar.set_label('ROAS %', fontsize=12, fontweight='600', color='#333333')

    ax2.grid(True, alpha=0.2, linestyle='--', linewidth=0.8, color='#DDDDDD')
    ax2.set_axisbelow(True)

    # Clean spines
    for spine in ['top', 'right']:
        ax2.spines[spine].set_visible(False)
    for spine in ['bottom', 'left']:
        ax2.spines[spine].set_color('#999999')
        ax2.spines[spine].set_linewidth(2)

    # Add Roksys logo (bottom-right)
    logo_path = Path('/Users/administrator/Documents/PetesBrain/shared/assets/branding/roksys-logo-200x50.png')
    if logo_path.exists():
        try:
            logo = Image.open(logo_path)
            new_width = int(logo.width * 0.35)
            new_height = int(logo.height * 0.35)
            logo_resized = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)

            fig.figimage(logo_resized,
                        xo=fig.bbox.xmax - new_width - 15,
                        yo=15,
                        alpha=0.7,
                        zorder=1)
        except Exception as e:
            print(f"Note: Could not add logo: {e}")

    # Tight layout
    plt.tight_layout(pad=2.0, rect=[0, 0.02, 1, 1])

    # Save
    plt.savefig(OUTPUT_CHART, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    print(f"\n✓ Chart saved: {OUTPUT_CHART}")

def main():
    print("="*70)
    print("CREATING ROAS PERFORMANCE CHART")
    print("="*70)

    if not INPUT_CSV.exists():
        print(f"ERROR: Correlation data not found: {INPUT_CSV}")
        return

    # Load data
    print(f"\nLoading data from: {INPUT_CSV}")
    data = load_data()
    print(f"✓ Loaded {len(data)} countries with actual enrollments\n")

    # Create chart
    create_roas_chart(data)

    print("\n✓ Chart generation complete!")

if __name__ == '__main__':
    main()
