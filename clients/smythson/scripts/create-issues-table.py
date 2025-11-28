#!/usr/bin/env python3
"""Create a simple HTML table of issues found"""

import json

# Load the issues
with open('/Users/administrator/Documents/PetesBrain/clients/smythson/documents/eur-row-issues-from-api.json', 'r') as f:
    issues = json.load(f)

# Create HTML
html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Smythson EUR/ROW - Issues from Google Ads</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; font-size: 12px; }
        h1 { font-size: 18px; }
        h2 { font-size: 14px; margin-top: 30px; }
        table { border-collapse: collapse; width: 100%; margin-top: 10px; }
        th, td { border: 1px solid #ccc; padding: 6px 8px; text-align: left; vertical-align: top; }
        th { background: #f0f0f0; }
        .currency { background: #fff3cd; }
        .arrivals { background: #f8d7da; }
        .ext-yes { font-weight: bold; }
    </style>
</head>
<body>
    <h1>Smythson EUR/ROW Ad Copy Issues</h1>
    <p>Pulled from Google Ads API - 21 Nov 2025</p>
    <p><strong>Total issues: """ + str(len(issues)) + """</strong></p>
"""

# Separate EUR and ROW, and by issue type
eur_currency = [i for i in issues if i['account'] == 'EUR' and 'CURRENCY' in i['issue']]
eur_arrivals = [i for i in issues if i['account'] == 'EUR' and 'NEW ARRIVALS' in i['issue']]
row_currency = [i for i in issues if i['account'] == 'ROW' and 'CURRENCY' in i['issue']]
row_arrivals = [i for i in issues if i['account'] == 'ROW' and 'NEW ARRIVALS' in i['issue']]

def make_table(items, title, css_class):
    if not items:
        return f"<h2>{title}</h2><p>None found</p>"

    # Deduplicate by campaign + ad group/asset group + text
    seen = set()
    unique_items = []
    for item in items:
        key = (item['campaign'], item['location'], item['text'])
        if key not in seen:
            seen.add(key)
            unique_items.append(item)

    html = f"<h2>{title} ({len(unique_items)} unique)</h2>"
    html += """<table>
        <tr>
            <th>Campaign</th>
            <th>Ad Group / Asset Group</th>
            <th>Type</th>
            <th>Extension?</th>
            <th>Text</th>
        </tr>"""

    for item in unique_items:
        ext_class = 'ext-yes' if item['is_extension'] == 'Yes' else ''
        html += f"""<tr class="{css_class}">
            <td>{item['campaign']}</td>
            <td>{item['location']}</td>
            <td>{item['type']}</td>
            <td class="{ext_class}">{item['is_extension']}</td>
            <td>{item['text'][:80]}{'...' if len(item['text']) > 80 else ''}</td>
        </tr>"""

    html += "</table>"
    return html

html += make_table(eur_currency, "EUR - Currency Issues (£300 should be €300)", "currency")
html += make_table(eur_arrivals, "EUR - New Arrivals (remove for winter sale)", "arrivals")
html += make_table(row_arrivals, "ROW - New Arrivals (remove for winter sale)", "arrivals")

# Note about ROW currency
html += """
<h2>ROW - Currency Issues</h2>
<p><em>ROW uses £300 which is correct - no changes needed for currency in ROW.</em></p>
"""

html += """
</body>
</html>
"""

# Save
output_path = '/Users/administrator/Documents/PetesBrain/clients/smythson/documents/eur-row-issues-simple-table.html'
with open(output_path, 'w') as f:
    f.write(html)

print(f"Table saved to: {output_path}")
print(f"\nSummary:")
print(f"  EUR Currency issues: {len(eur_currency)} ({len(set((i['campaign'], i['location'], i['text']) for i in eur_currency))} unique)")
print(f"  EUR New Arrivals: {len(eur_arrivals)} ({len(set((i['campaign'], i['location'], i['text']) for i in eur_arrivals))} unique)")
print(f"  ROW New Arrivals: {len(row_arrivals)} ({len(set((i['campaign'], i['location'], i['text']) for i in row_arrivals))} unique)")
