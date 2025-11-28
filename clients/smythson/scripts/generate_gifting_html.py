#!/usr/bin/env python3
"""
Parse the Smythson gifting translation spreadsheet and create an HTML file
displaying headlines, long headlines, and descriptions grouped by asset group.
"""

import csv
import os

# Path to the CSV file
csv_path = '/Users/administrator/Documents/PetesBrain/clients/smythson/spreadsheets/SMY _ Gifting Black Friday and Diaries ads_final(Gifting).csv'
output_path = '/Users/administrator/Documents/PetesBrain/clients/smythson/documents/gifting-text-assets-copyable.html'

def parse_csv():
    """Parse the CSV file and extract data organized by language and asset group."""
    data = {}
    current_language = None
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    i = 0
    while i < len(rows):
        row = rows[i]
        
        # Check if this is a language header (which is also the first data row for that language)
        if len(row) > 0 and row[0] in ['UK/US/EUR/ROW', 'GERMAN', 'ITALIAN', 'FRENCH']:
            current_language = row[0]
            if current_language not in data:
                data[current_language] = {}
            # This row also contains data, so process it
            # Then skip the header row that follows
            if len(row) > 1 and row[1] and row[1].strip():
                asset_group = row[1].strip()
                if asset_group not in data[current_language]:
                    data[current_language][asset_group] = {
                        'headlines': [],
                        'long_headlines': [],
                        'descriptions': []
                    }
                
                # Extract headlines (indices 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31)
                for idx in range(3, 33, 2):
                    if idx < len(row) and row[idx] and row[idx].strip():
                        headline = row[idx].strip()
                        if headline:
                            data[current_language][asset_group]['headlines'].append(headline)
                
                # Extract long headlines (indices 34, 36, 38, 40, 42)
                for idx in range(34, 44, 2):
                    if idx < len(row) and row[idx] and row[idx].strip():
                        long_headline = row[idx].strip()
                        if long_headline:
                            data[current_language][asset_group]['long_headlines'].append(long_headline)
                
                # Extract descriptions (indices 44, 46, 48, 50, 52)
                for idx in range(44, 54, 2):
                    if idx < len(row) and row[idx] and row[idx].strip():
                        description = row[idx].strip()
                        if description:
                            data[current_language][asset_group]['descriptions'].append(description)
            
            # Skip the header row that follows
            i += 2
            continue
        
        # Skip header rows
        if row and len(row) > 0 and row[0] == 'campaign':
            i += 1
            continue
        
        # Check if this is a data row with an asset group
        # The asset group is in column 1, and column 0 might be empty or have campaign name
        if len(row) > 1 and row[1] and row[1].strip():  # Asset Group column
            asset_group = row[1].strip()
            
            # Only process if we have a current language set
            if current_language:
                if asset_group not in data[current_language]:
                    data[current_language][asset_group] = {
                        'headlines': [],
                        'long_headlines': [],
                        'descriptions': []
                    }
                
                # Extract headlines (indices 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31)
                for idx in range(3, 33, 2):
                    if idx < len(row) and row[idx] and row[idx].strip():
                        headline = row[idx].strip()
                        if headline:
                            data[current_language][asset_group]['headlines'].append(headline)
                
                # Extract long headlines (indices 34, 36, 38, 40, 42)
                for idx in range(34, 44, 2):
                    if idx < len(row) and row[idx] and row[idx].strip():
                        long_headline = row[idx].strip()
                        if long_headline:
                            data[current_language][asset_group]['long_headlines'].append(long_headline)
                
                # Extract descriptions (indices 44, 46, 48, 50, 52)
                for idx in range(44, 54, 2):
                    if idx < len(row) and row[idx] and row[idx].strip():
                        description = row[idx].strip()
                        if description:
                            data[current_language][asset_group]['descriptions'].append(description)
        
        i += 1
    
    return data

def generate_html(data):
    """Generate HTML file from parsed data."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smythson Gifting Text Assets - Copyable</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #333;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 40px;
            border-bottom: 2px solid #ccc;
            padding-bottom: 5px;
        }
        h3 {
            color: #777;
            margin-top: 30px;
            font-size: 1.2em;
        }
        .language-section {
            background-color: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .asset-group {
            margin: 30px 0;
            padding: 15px;
            background-color: #fafafa;
            border-left: 4px solid #333;
        }
        .section-label {
            font-weight: bold;
            color: #333;
            margin-top: 15px;
            margin-bottom: 5px;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .text-item {
            padding: 8px 12px;
            margin: 5px 0;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            cursor: text;
            user-select: all;
        }
        .text-item:hover {
            background-color: #f0f0f0;
            border-color: #999;
        }
        .empty {
            color: #999;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>Smythson Gifting Text Assets - Copyable</h1>
    <p>All text assets organized by language and asset group. Click to select and copy.</p>
"""
    
    # Language display names
    language_names = {
        'UK/US/EUR/ROW': 'English (UK/US/EUR/ROW)',
        'GERMAN': 'German',
        'ITALIAN': 'Italian',
        'FRENCH': 'French'
    }
    
    for language in ['UK/US/EUR/ROW', 'GERMAN', 'ITALIAN', 'FRENCH']:
        if language not in data or not data[language]:
            continue
        
        html += f'    <div class="language-section">\n'
        html += f'        <h2>{language_names.get(language, language)}</h2>\n'
        
        for asset_group in sorted(data[language].keys()):
            group_data = data[language][asset_group]
            html += f'        <div class="asset-group">\n'
            html += f'            <h3>{asset_group}</h3>\n'
            
            # Headlines
            html += '            <div class="section-label">Headlines</div>\n'
            if group_data['headlines']:
                for headline in group_data['headlines']:
                    html += f'            <div class="text-item">{headline}</div>\n'
            else:
                html += '            <div class="text-item empty">No headlines</div>\n'
            
            # Long Headlines
            html += '            <div class="section-label">Long Headlines</div>\n'
            if group_data['long_headlines']:
                for long_headline in group_data['long_headlines']:
                    html += f'            <div class="text-item">{long_headline}</div>\n'
            else:
                html += '            <div class="text-item empty">No long headlines</div>\n'
            
            # Descriptions
            html += '            <div class="section-label">Descriptions</div>\n'
            if group_data['descriptions']:
                for description in group_data['descriptions']:
                    html += f'            <div class="text-item">{description}</div>\n'
            else:
                html += '            <div class="text-item empty">No descriptions</div>\n'
            
            html += '        </div>\n'
        
        html += '    </div>\n'
    
    html += """</body>
</html>"""
    
    return html

def main():
    print("Parsing CSV file...")
    data = parse_csv()
    
    # Debug: print what we found
    print(f"Found {len(data)} languages")
    for lang, groups in data.items():
        print(f"  {lang}: {len(groups)} asset groups")
        for ag, content in groups.items():
            print(f"    {ag}: {len(content['headlines'])} headlines, {len(content['long_headlines'])} long headlines, {len(content['descriptions'])} descriptions")
    
    print("Generating HTML...")
    html = generate_html(data)
    
    print(f"Writing HTML to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Done! HTML file created at: {output_path}")
    print(f"Open it in your browser to view and copy the text assets.")

if __name__ == '__main__':
    main()

