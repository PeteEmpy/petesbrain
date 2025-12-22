#!/usr/bin/env python3
"""Convert keyword audit markdown to styled HTML"""

import markdown

# Read markdown file
with open('../audits/keyword-audit-2025-12-17.md', 'r') as f:
    md_content = f.read()

# Convert to HTML with tables extension
html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# Create styled HTML with Roksys green headings
styled_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Clear Prospects - Keyword Audit (17th December 2025)</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
            line-height: 1.6;
        }}
        .container {{
            background: white;
            padding: 50px;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #10B981;
            border-bottom: 3px solid #10B981;
            padding-bottom: 15px;
            font-size: 2.5em;
            margin-top: 0;
        }}
        h2 {{
            color: #059669;
            border-bottom: 2px solid #D1FAE5;
            padding-bottom: 10px;
            margin-top: 50px;
            font-size: 1.8em;
        }}
        h3 {{
            color: #047857;
            margin-top: 35px;
            font-size: 1.4em;
        }}
        h4 {{
            color: #065F46;
            margin-top: 25px;
            font-size: 1.2em;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 25px 0;
            font-size: 0.95em;
        }}
        th {{
            background-color: #10B981;
            color: white;
            padding: 14px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #059669;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 12px;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #D1FAE5;
        }}
        strong {{
            color: #065F46;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
        }}
        hr {{
            border: none;
            border-top: 2px solid #D1FAE5;
            margin: 40px 0;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Courier New", monospace;
        }}
        .metric {{
            display: inline-block;
            background: #D1FAE5;
            padding: 3px 8px;
            border-radius: 4px;
            font-weight: 600;
            color: #065F46;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>"""

# Write HTML file
output_path = '../audits/keyword-audit-2025-12-17.html'
with open(output_path, 'w') as f:
    f.write(styled_html)

print(f"✅ HTML report generated: {output_path}")
