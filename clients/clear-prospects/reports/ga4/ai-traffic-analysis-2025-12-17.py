#!/usr/bin/env python3
"""
AI Traffic Analysis for Clear Prospects - 2025
Generates line graph showing monthly AI tool traffic and revenue trends
"""

import json
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# AI tool sources to track
AI_TOOLS = {
    'chatgpt.com': 'ChatGPT',
    'claude.ai': 'Claude',
    'perplexity.ai': 'Perplexity',
    'perplexity': 'Perplexity',
    'gemini.google.com': 'Gemini',
    'bard.google.com': 'Bard',
    'chat.mistral.ai': 'Mistral',
    'you.com': 'You.com',
    'poe.com': 'Poe',
    'character.ai': 'Character.AI',
    'bing.com/chat': 'Bing Chat',
    'pi.ai': 'Pi',
    'copilot.microsoft.com': 'Copilot',
    'copilot.com': 'Copilot',
    'openai': 'OpenAI',
}

# Raw data from GA4 API (filtered for AI tools only)
ai_traffic_data = {
    '202501': {'sessions': 5, 'revenue': 17.98},  # chatgpt.com (not set)
    '202502': {'sessions': 11+2, 'revenue': 0+0},  # chatgpt.com (not set) + referral
    '202503': {'sessions': 8+6, 'revenue': 0+0},  # chatgpt.com (not set) + referral
    '202504': {'sessions': 11+5, 'revenue': 0+0},  # chatgpt.com (not set) + referral
    '202505': {'sessions': 33+5+1, 'revenue': 62.36+0+0},  # chatgpt.com (not set) + referral + perplexity.ai
    '202506': {'sessions': 21+7, 'revenue': 23.98+0},  # chatgpt.com (not set) + referral
    '202507': {'sessions': 31+6+2+1, 'revenue': 522+0+0+0},  # chatgpt.com (not set) + referral + gemini + perplexity (not set)
    '202508': {'sessions': 24+2+2, 'revenue': 0+0+0},  # chatgpt.com (not set) + referral + perplexity (not set)
    '202509': {'sessions': 12+13+1, 'revenue': 18.97+17.98+0},  # chatgpt.com (not set) + referral + perplexity.ai
    '202510': {'sessions': 51+23+2, 'revenue': 25.2+39.95+0},  # chatgpt.com (not set) + referral + perplexity (not set)
    '202511': {'sessions': 61+18+3, 'revenue': 64.98+0+0},  # chatgpt.com (not set) + referral + perplexity (not set)
    '202512': {'sessions': 36+17+1+1, 'revenue': 154.85+0+0+0},  # chatgpt.com (not set) + referral + perplexity (not set) + copilot.com (not set)
}

# Convert yearMonth to datetime and sort
months = []
sessions_list = []
revenue_list = []

for yearmonth in sorted(ai_traffic_data.keys()):
    # Convert YYYYMM to datetime (first day of month)
    date_obj = datetime.strptime(yearmonth, '%Y%m')
    months.append(date_obj)
    sessions_list.append(ai_traffic_data[yearmonth]['sessions'])
    revenue_list.append(ai_traffic_data[yearmonth]['revenue'])

# Create figure with two y-axes and white background
fig, ax1 = plt.subplots(figsize=(15, 8), facecolor='white')
ax1.set_facecolor('#F9FAFB')  # Light grey background

# Plot sessions on left y-axis
color1 = '#2563EB'  # Blue for sessions
ax1.set_xlabel('Month', fontsize=13, fontweight='bold', color='#1F2937')
ax1.set_ylabel('Sessions from AI Tools', fontsize=13, fontweight='bold', color=color1)
line1 = ax1.plot(months, sessions_list, color=color1, marker='o', linewidth=3.5,
                 markersize=10, label='Sessions', zorder=3, markeredgewidth=2,
                 markeredgecolor='white', markerfacecolor=color1)
ax1.tick_params(axis='y', labelcolor=color1, labelsize=11)
ax1.tick_params(axis='x', labelsize=11)
ax1.grid(True, alpha=0.2, linestyle='-', linewidth=1, color='#9CA3AF')
ax1.set_ylim(0, max(sessions_list) * 1.15)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color(color1)
ax1.spines['left'].set_linewidth(2)

# Plot revenue on right y-axis
ax2 = ax1.twinx()
color2 = '#10B981'  # ROK Green for revenue
ax2.set_ylabel('Revenue from AI Tools (£)', fontsize=13, fontweight='bold', color=color2)
line2 = ax2.plot(months, revenue_list, color=color2, marker='s', linewidth=3.5,
                 markersize=10, label='Revenue', linestyle='--', zorder=3,
                 markeredgewidth=2, markeredgecolor='white', markerfacecolor=color2)
ax2.tick_params(axis='y', labelcolor=color2, labelsize=11)
ax2.set_ylim(0, max(revenue_list) * 1.15)
ax2.spines['right'].set_color(color2)
ax2.spines['right'].set_linewidth(2)
ax2.spines['top'].set_visible(False)

# Format x-axis to show month names
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
ax1.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=0, ha='center')

# Add title with subtitle
plt.title('AI Tool Traffic & Revenue Trends - 2025',
          fontsize=16, fontweight='bold', pad=15, color='#1F2937')
fig.text(0.5, 0.96, 'ChatGPT, Perplexity, Gemini & Copilot referrals',
         ha='center', fontsize=11, style='italic', color='#6B7280')

# Add combined legend
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', frameon=True, shadow=True)

# Add data labels for key points
for i, (month, sessions, revenue) in enumerate(zip(months, sessions_list, revenue_list)):
    # Label sessions at peaks
    if sessions == max(sessions_list) or i == len(sessions_list) - 1:
        ax1.annotate(f'{int(sessions)}',
                    xy=(month, sessions),
                    xytext=(0, 10),
                    textcoords='offset points',
                    ha='center',
                    fontsize=9,
                    fontweight='bold',
                    color=color1)

    # Label revenue at peaks and non-zero values
    if revenue > 100 or i == len(revenue_list) - 1:
        ax2.annotate(f'£{revenue:.0f}',
                    xy=(month, revenue),
                    xytext=(0, -15),
                    textcoords='offset points',
                    ha='center',
                    fontsize=9,
                    fontweight='bold',
                    color=color2)

# Tight layout
plt.tight_layout()

# Save figure
output_path = '/Users/administrator/Documents/PetesBrain.nosync/clients/clear-prospects/reports/ga4/ai-traffic-chart-2025-12-17.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Chart saved to: {output_path}")

# Also save as PDF for better quality
pdf_path = output_path.replace('.png', '.pdf')
plt.savefig(pdf_path, format='pdf', bbox_inches='tight', facecolor='white')
print(f"PDF saved to: {pdf_path}")

# Don't show plot (would block in headless mode)
# plt.show()

# Print summary statistics
print("\n" + "="*60)
print("AI TRAFFIC SUMMARY - CLEAR PROSPECTS (JAN-DEC 2025)")
print("="*60)
print(f"Total Sessions: {sum(sessions_list):,}")
print(f"Total Revenue: £{sum(revenue_list):.2f}")
print(f"Average Sessions/Month: {sum(sessions_list)/len(sessions_list):.1f}")
print(f"Average Revenue/Month: £{sum(revenue_list)/len(revenue_list):.2f}")
print(f"Peak Sessions: {max(sessions_list)} ({months[sessions_list.index(max(sessions_list))].strftime('%B')})")
print(f"Peak Revenue: £{max(revenue_list):.2f} ({months[revenue_list.index(max(revenue_list))].strftime('%B')})")
print(f"Growth (Jan vs Dec): Sessions {sessions_list[-1]/sessions_list[0]*100-100:+.1f}%, Revenue {revenue_list[-1]/revenue_list[0]*100-100:+.1f}%")
print("="*60)
