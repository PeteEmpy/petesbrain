#!/usr/bin/env python3
"""
Analyse 60-day Uno Lighting search term data using three-tier statistical criteria.
Period: 18th October - 17th December 2025
Customer ID: 6413338364

NO PRODUCT ASSUMPTIONS - purely statistical analysis based on:
- Click volume (statistical significance threshold)
- Conversion performance
- Spend levels
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for MCP imports
sys.path.insert(0, str(Path('/Users/administrator/Documents/PetesBrain.nosync')))

def classify_search_term(clicks, conversions, spend_gbp):
    """
    Classify a single search term into one of four categories.

    Returns: ('tier1' | 'tier2' | 'tier3' | 'converting')
    """
    # If has meaningful conversions (>=0.1), it's a converting term
    if conversions >= 0.1:
        return 'converting'

    # Zero or near-zero conversion terms
    if clicks >= 30 and spend_gbp >= 20:
        return 'tier1'  # Strong negative candidate
    elif clicks >= 10:
        return 'tier2'  # Monitor closely
    else:
        return 'tier3'  # Insufficient data


def analyse_search_terms():
    """
    Pull 60-day search term data and classify into three tiers.
    """
    print("🔄 Analysing 60-day search term data for Uno Lighting...")
    print(f"Period: 18th October - 17th December 2025 (60 days)")
    print(f"Customer ID: 6413338364")
    print()

    # Import MCP tool
    try:
        # In Claude Code context, mcp tools are available globally
        # This script is designed to be run within Claude Code execution
        print("⚠️  This script requires Claude Code MCP context")
        print("    Please run via Claude Code, not standalone Python")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def format_currency(micros):
    """Convert micros to GBP formatted string."""
    return f"£{micros / 1_000_000:.2f}"


def format_percentage(value):
    """Format as percentage."""
    return f"{value:.0f}%"


def calculate_roas(revenue_micros, spend_micros):
    """Calculate ROAS as percentage."""
    if spend_micros == 0:
        return 0
    return (revenue_micros / spend_micros) * 100


if __name__ == "__main__":
    print("=" * 80)
    print("UNO LIGHTING: 60-DAY SEARCH TERM CLASSIFICATION ANALYSIS")
    print("=" * 80)
    print()
    print("This script processes search term data using statistical criteria:")
    print()
    print("Tier 1 (Strong Negative Candidates):")
    print("  - 30+ clicks in 60 days")
    print("  - 0 conversions (or <0.1)")
    print("  - £20+ spend")
    print()
    print("Tier 2 (Monitor Closely):")
    print("  - 10-29 clicks in 60 days")
    print("  - 0 conversions (or <0.1)")
    print()
    print("Tier 3 (Insufficient Data):")
    print("  - <10 clicks in 60 days")
    print()
    print("=" * 80)
    print()

    result = analyse_search_terms()

    if result is None:
        print()
        print("⚠️  Run this analysis through Claude Code for MCP tool access")
