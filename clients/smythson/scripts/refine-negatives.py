#!/usr/bin/env python3
"""
Refine negative keyword recommendations - separate genuine negatives from brand terms with issues
"""

import json
from datetime import datetime

# Load candidates
with open('/Users/administrator/Documents/PetesBrain/clients/smythson/documents/eur-row-negative-candidates.json') as f:
    candidates = json.load(f)

# Brand terms - these should NOT be negatives, but flagged for investigation
brand_patterns = ['smythson', 'smython', 'smithson', 'smythsons']

# Genuine negative patterns
negative_patterns = [
    # Competitors
    'aspinal', 'mulberry', 'louis vuitton', 'gucci', 'prada', 'hermes',
    'montblanc', 'mont blanc', 'cross pen', 'parker pen', 'waterman',
    'filofax', 'moleskine', 'leuchtturm', 'rhodia', 'paperchase',
    'ettinger', 'globe trotter', 'anya hindmarch', 'loewe', 'bottega',
    # Cheap/discount seekers
    'cheap', 'cheapest', 'budget', 'affordable', 'discount', 'coupon',
    'promo code', 'voucher', 'sale', 'outlet', 'clearance',
    'second hand', 'used', 'pre owned', 'ebay', 'amazon', 'aliexpress',
    # DIY/How to
    'diy', 'how to make', 'tutorial', 'template', 'printable', 'free download',
    # Jobs
    'job', 'jobs', 'career', 'hiring', 'salary', 'glassdoor', 'indeed',
    # Info seekers
    'wiki', 'wikipedia', 'reddit', 'review', 'vs', 'versus', 'compare',
    'what is', 'meaning', 'pronounce', 'pronunciation',
    # Service/repair
    'repair', 'fix', 'broken', 'restore', 'refurbish',
    # Wrong product intent
    'app', 'software', 'download', 'login', 'sign in',
]

# Categorize
genuine_negatives = []
brand_issues = []
other_issues = []

for c in candidates:
    term_lower = c['search_term'].lower()

    # Check if it contains brand
    is_brand = any(bp in term_lower for bp in brand_patterns)

    # Check if it matches negative pattern
    matched_pattern = None
    for np in negative_patterns:
        if np in term_lower:
            matched_pattern = np
            break

    if matched_pattern and not is_brand:
        c['matched_pattern'] = matched_pattern
        genuine_negatives.append(c)
    elif is_brand:
        c['note'] = 'Brand term - investigate why not converting'
        brand_issues.append(c)
    else:
        other_issues.append(c)

# Sort by cost
genuine_negatives.sort(key=lambda x: x['cost'], reverse=True)
brand_issues.sort(key=lambda x: x['cost'], reverse=True)
other_issues.sort(key=lambda x: x['cost'], reverse=True)

# Calculate totals
genuine_total = sum(n['cost'] for n in genuine_negatives)
brand_total = sum(n['cost'] for n in brand_issues)

print("="*60)
print("REFINED NEGATIVE ANALYSIS")
print("="*60)
print(f"\nGenuine negatives (add these): {len(genuine_negatives)}")
print(f"  Total wasted spend: £{genuine_total:.2f}")
print(f"\nBrand terms not converting (DON'T negative - investigate): {len(brand_issues)}")
print(f"  Total spend: £{brand_total:.2f}")
print(f"\nOther non-converting terms: {len(other_issues)}")

# Create refined HTML report
html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Smythson EUR/ROW - Refined Negative Recommendations</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; font-size: 12px; }
        h1 { font-size: 18px; }
        h2 { font-size: 14px; margin-top: 30px; border-bottom: 2px solid #333; padding-bottom: 5px; }
        h3 { font-size: 13px; margin-top: 20px; color: #666; }
        table { border-collapse: collapse; width: 100%; margin-top: 10px; }
        th, td { border: 1px solid #ccc; padding: 6px 8px; text-align: left; }
        th { background: #f0f0f0; }
        .add-negative { background: #f8d7da; }
        .investigate { background: #fff3cd; }
        .summary { background: #e7f3ff; padding: 15px; margin: 20px 0; border-left: 4px solid #007bff; }
        .warning { background: #fff3cd; padding: 15px; margin: 20px 0; border-left: 4px solid #ffc107; }
        .action { font-weight: bold; color: #d63384; }
    </style>
</head>
<body>
    <h1>Smythson EUR/ROW - Negative Keyword Recommendations</h1>
    <p>Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M') + """ | Period: Last 30 days</p>

    <div class="summary">
        <strong>Summary:</strong><br><br>
        <span class="action">ADD AS NEGATIVES:</span> """ + str(len(genuine_negatives)) + """ terms (£""" + f"{genuine_total:.2f}" + """ wasted)<br>
        <span style="color: #856404;">INVESTIGATE (don't negative):</span> """ + str(len(brand_issues)) + """ brand terms not converting (£""" + f"{brand_total:.2f}" + """ spent)
    </div>

    <div class="warning">
        <strong>Important:</strong> The brand terms below (smythson + product) are getting clicks but not converting.
        This could indicate:<br>
        - Product out of stock<br>
        - Landing page issues<br>
        - Price perception problems<br>
        - Wrong landing page<br>
        <strong>Don't add these as negatives</strong> - investigate and fix the conversion issue instead.
    </div>
"""

# Section 1: Genuine Negatives
html += """
    <h2>1. ADD THESE AS NEGATIVES</h2>
    <p>These are competitor terms, discount seekers, and irrelevant searches. Add to negative keyword lists.</p>
"""

# Group by pattern type
competitor_negs = [n for n in genuine_negatives if n['matched_pattern'] in ['aspinal', 'mulberry', 'louis vuitton', 'gucci', 'prada', 'hermes', 'montblanc', 'mont blanc', 'ettinger', 'filofax', 'moleskine', 'leuchtturm', 'anya hindmarch', 'loewe', 'bottega']]
discount_negs = [n for n in genuine_negatives if n['matched_pattern'] in ['cheap', 'cheapest', 'discount', 'coupon', 'sale', 'outlet', 'second hand', 'used', 'ebay', 'amazon']]
info_negs = [n for n in genuine_negatives if n['matched_pattern'] in ['wiki', 'reddit', 'review', 'vs', 'versus', 'compare', 'pronounce', 'pronunciation', 'what is']]
other_negs = [n for n in genuine_negatives if n not in competitor_negs and n not in discount_negs and n not in info_negs]

def make_neg_table(items, title):
    if not items:
        return ""
    total = sum(i['cost'] for i in items)
    h = f"""
    <h3>{title} ({len(items)} terms, £{total:.2f} wasted)</h3>
    <table>
        <tr><th>Account</th><th>Search Term</th><th>Cost</th><th>Clicks</th><th>Pattern</th></tr>
"""
    for n in items[:30]:
        h += f"""        <tr class="add-negative">
            <td>{n['account']}</td>
            <td><strong>{n['search_term']}</strong></td>
            <td>£{n['cost']}</td>
            <td>{n['clicks']}</td>
            <td>{n['matched_pattern']}</td>
        </tr>
"""
    h += "    </table>"
    return h

html += make_neg_table(competitor_negs, "Competitor Terms")
html += make_neg_table(discount_negs, "Discount/Cheap Seekers")
html += make_neg_table(info_negs, "Information Seekers (not buyers)")
html += make_neg_table(other_negs, "Other Irrelevant")

# Section 2: Brand Issues
html += """
    <h2>2. INVESTIGATE - Brand Terms Not Converting</h2>
    <p><strong>Do NOT add these as negatives.</strong> These are brand searches that should convert but aren't. Find out why.</p>
    <table>
        <tr><th>Account</th><th>Search Term</th><th>Cost</th><th>Clicks</th><th>Imps</th><th>Action</th></tr>
"""
for n in brand_issues[:50]:
    ctr = (n['clicks'] / n['impressions'] * 100) if n['impressions'] > 0 else 0
    html += f"""        <tr class="investigate">
            <td>{n['account']}</td>
            <td><strong>{n['search_term']}</strong></td>
            <td>£{n['cost']}</td>
            <td>{n['clicks']}</td>
            <td>{n['impressions']}</td>
            <td>Check landing page & stock</td>
        </tr>
"""
html += "    </table>"

# Quick copy list for negatives
html += """
    <h2>3. Quick Copy - Negative Keywords to Add</h2>
    <p>Copy this list and add to your negative keyword lists:</p>
    <textarea style="width:100%; height:300px; font-family: monospace; font-size: 11px;">"""

# Dedupe and list
neg_terms = sorted(set(n['search_term'] for n in genuine_negatives))
html += "\n".join(neg_terms)
html += """</textarea>
</body>
</html>
"""

# Save
output_path = '/Users/administrator/Documents/PetesBrain/clients/smythson/documents/eur-row-negative-recommendations-refined.html'
with open(output_path, 'w') as f:
    f.write(html)

print(f"\nRefined report saved to: {output_path}")

# Print top genuine negatives
print("\nTop 15 GENUINE negatives (add these):")
for n in genuine_negatives[:15]:
    print(f"  £{n['cost']:>6.2f} | {n['account']} | {n['search_term'][:45]} | [{n['matched_pattern']}]")

print("\nTop 10 BRAND terms to investigate (don't negative):")
for n in brand_issues[:10]:
    print(f"  £{n['cost']:>6.2f} | {n['account']} | {n['search_term'][:45]}")
