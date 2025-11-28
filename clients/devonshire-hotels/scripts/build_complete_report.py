#!/usr/bin/env python3
"""
Build complete Devonshire Hotels October 2025 report
Combines all individual slide HTML files and commentary into one navigable document
"""

import re
from pathlib import Path

# Define paths
BASE_DIR = Path("/Users/administrator/Documents/PetesBrain/clients/devonshire-hotels")
SLIDES_DIR = BASE_DIR / "Monthly Report Slides"
COMMENTARY_FILE = BASE_DIR / "documents/october-2025-slide-commentary.html"
OUTPUT_FILE = BASE_DIR / "reports/october-2025-complete-report.html"

# Slide configuration
SLIDES = [
    {"id": "slide-16", "file": "Slide 16 October 25.html", "title": "Overview", "nav": "Overview"},
    {"id": "slide-17", "file": "Slide 17 October 25 UPDATED.html", "title": "Year-over-Year", "nav": "YoY"},
    {"id": "slide-18", "file": "Slide 18 October 25.html", "title": "Monthly Trends", "nav": "Trends"},
    {"id": "slide-19", "file": "Slide 19 October 25.html", "title": "Search vs PMax", "nav": "Search vs PMax"},
    {"id": "slide-20", "file": "Slide 20 October 25.html", "title": "Profitability", "nav": "Profitability"},
    {"id": "slide-21", "file": "Slide 21 October 25.html", "title": "Locations", "nav": "Locations"},
    {"id": "slide-22", "file": "Slide 22 October 25.html", "title": "Self-Catering", "nav": "Self-Catering"},
    {"id": "slide-23", "file": "Slide 23 October 25.html", "title": "The Hide", "nav": "The Hide"},
    {"id": "slide-24", "file": "Slide 24 October 25.html", "title": "Weddings", "nav": "Weddings"},
    {"id": "slide-25", "file": "Slide 25 October 25.html", "title": "Hide Trend", "nav": "Hide Trend"},
    {"id": "slide-26", "file": "Slide 26 October 25.html", "title": "Exclusive Venues", "nav": "Venues"},
]

def extract_body_content(html_content):
    """Extract just the body content from HTML file"""
    # Find body content
    body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
    if body_match:
        body = body_match.group(1)

        # Remove script tags (they'll be added at the end)
        body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)

        # Remove container divs - handle nested structure
        # Remove opening container div
        body = re.sub(r'<div\s+class="container[^"]*"[^>]*>', '', body)
        body = re.sub(r'<div\s+class="slide-container[^"]*"[^>]*>', '', body)

        # Remove closing divs (from end, working backwards)
        # Count divs to remove the right number of closing tags
        opening_divs = len(re.findall(r'<div\s+class="(?:container|slide-container)', body))
        for _ in range(opening_divs):
            # Remove last </div>
            body = re.sub(r'</div>\s*$', '', body, count=1)

        return body.strip()
    return ""

def extract_scripts(html_content):
    """Extract all script tags from HTML"""
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html_content, re.DOTALL)
    return scripts

def build_combined_report():
    """Build the complete combined report"""

    print("Building complete Devonshire Hotels October 2025 report...")

    # Start building HTML
    html_parts = []

    # Add header with nav
    html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Devonshire Hotels - October 2025 Complete Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js"></script>
    <style>
        :root {
            --estate-blue: #00333D;
            --stone: #E5E3DB;
            --success-green: #2E7D32;
            --alert-red: #C62828;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, Helvetica, sans-serif;
            background: #f5f5f5;
            color: #333;
        }

        /* Navigation */
        nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: var(--estate-blue);
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }

        .nav-content {
            max-width: 1800px;
            margin: 0 auto;
            padding: 15px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }

        .nav-title {
            color: white;
            font-size: 22px;
            font-weight: bold;
            white-space: nowrap;
        }

        .nav-links {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
            justify-content: flex-end;
        }

        .nav-link {
            color: white;
            text-decoration: none;
            padding: 8px 14px;
            border-radius: 4px;
            font-size: 13px;
            transition: background 0.3s;
            white-space: nowrap;
        }

        .nav-link:hover {
            background: rgba(255,255,255,0.2);
        }

        .nav-link.active {
            background: rgba(255,255,255,0.3);
            font-weight: bold;
        }

        /* Main Content */
        .content-wrapper {
            margin-top: 80px;
            padding: 40px;
        }

        .slide-section {
            max-width: 1600px;
            margin: 0 auto 60px;
            background: white;
            border-radius: 8px;
            padding: 50px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            scroll-margin-top: 100px;
        }

        /* Universal styles for all slide content */
        h1 {
            color: var(--estate-blue);
            font-size: 42px;
            margin-bottom: 30px;
            font-weight: bold;
        }

        h2 {
            color: var(--estate-blue);
            font-size: 32px;
            margin: 40px 0 20px;
            font-weight: bold;
        }

        h3 {
            color: var(--estate-blue);
            font-size: 22px;
            margin: 25px 0 15px;
            font-weight: bold;
        }

        .subtitle {
            color: #666;
            font-size: 18px;
            margin-bottom: 30px;
            text-align: center;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }

        thead {
            background: var(--estate-blue);
            color: white;
        }

        th {
            padding: 15px;
            text-align: left;
            font-size: 16px;
            font-weight: bold;
            border: 1px solid var(--estate-blue);
        }

        th.rank { text-align: center; }
        th.number { text-align: right; }

        td {
            padding: 15px;
            font-size: 17px;
            border: 1px solid #ddd;
        }

        td.rank {
            text-align: center;
            font-weight: bold;
            color: var(--estate-blue);
            font-size: 20px;
        }

        td.hotel-name {
            font-weight: 600;
            color: var(--estate-blue);
            font-size: 18px;
        }

        td.number {
            text-align: right;
            font-weight: 500;
        }

        tbody tr:nth-child(even) {
            background: var(--stone);
        }

        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin: 40px 0;
        }

        .kpi-box {
            background: var(--stone);
            border: 2px solid var(--estate-blue);
            border-radius: 8px;
            padding: 30px;
            text-align: center;
            min-height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .kpi-title {
            color: var(--estate-blue);
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .kpi-value {
            color: var(--estate-blue);
            font-size: 56px;
            font-weight: bold;
            margin: 15px 0;
        }

        .kpi-change {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }

        .arrow {
            font-size: 48px;
            font-weight: bold;
        }

        .arrow-up { color: var(--success-green); }
        .arrow-down { color: var(--alert-red); }

        .change-percent {
            font-size: 32px;
            font-weight: bold;
        }

        .change-percent.positive { color: var(--success-green); }
        .change-percent.negative { color: var(--alert-red); }

        .change-description {
            font-size: 16px;
            color: #666;
        }

        .change-details {
            text-align: center;
        }

        .chart-container {
            background: var(--stone);
            padding: 30px;
            border-radius: 8px;
            border: 2px solid var(--estate-blue);
            margin: 30px 0;
            position: relative;
        }

        .chart-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin: 30px 0;
        }

        .chart-grid .chart-container {
            height: 280px;
        }

        .chart-title {
            color: var(--estate-blue);
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        }

        canvas {
            max-height: 500px;
        }

        .commentary-box {
            background: var(--stone);
            padding: 25px;
            border-radius: 8px;
            border-left: 6px solid var(--estate-blue);
            margin: 25px 0;
        }

        .commentary-box h3 {
            margin-top: 0;
        }

        .commentary-box p {
            margin: 12px 0;
            line-height: 1.6;
        }

        .commentary-box ul {
            margin: 15px 0;
            padding-left: 25px;
        }

        .commentary-box li {
            margin: 10px 0;
            line-height: 1.5;
        }

        .info-box {
            background: white;
            padding: 20px;
            border: 2px solid var(--estate-blue);
            border-radius: 6px;
            margin: 20px 0;
        }

        .highlight-box {
            background: white;
            padding: 20px;
            border: 2px solid var(--estate-blue);
            border-radius: 6px;
            margin: 20px 0;
        }

        .footer-note, .footer {
            margin-top: 40px;
            padding: 20px;
            background: var(--stone);
            border-left: 4px solid var(--estate-blue);
            font-size: 14px;
            color: #666;
            line-height: 1.6;
        }

        .section-divider {
            background: var(--estate-blue) !important;
            color: white !important;
            font-weight: bold;
        }

        .section-divider td {
            padding: 12px 15px;
            font-size: 18px;
            color: white !important;
        }

        .alert { color: var(--alert-red); font-weight: 600; }
        .success { color: var(--success-green); font-weight: 600; }
        .positive { color: var(--success-green); font-weight: 600; }
        .negative { color: var(--alert-red); font-weight: 600; }
        .neutral { color: #666; font-weight: 600; }

        strong {
            font-weight: 600;
            color: var(--estate-blue);
        }

        ul {
            margin: 15px 0;
            padding-left: 25px;
        }

        li {
            margin: 10px 0;
            line-height: 1.5;
        }

        .slide-ref {
            color: #999;
            font-size: 14px;
            font-style: italic;
            margin-bottom: 15px;
        }

        .section {
            margin-bottom: 50px;
        }
    </style>
</head>
<body>
    <nav>
        <div class="nav-content">
            <div class="nav-title">Devonshire Hotels - October 2025</div>
            <div class="nav-links">
''')

    # Add navigation links for all slides
    for slide in SLIDES:
        html_parts.append(f'                <a href="#{slide["id"]}" class="nav-link">{slide["nav"]}</a>\n')

    html_parts.append('                <a href="#commentary" class="nav-link">Commentary</a>\n')
    html_parts.append('''            </div>
        </div>
    </nav>

    <div class="content-wrapper">
''')

    # Process each slide
    all_scripts = []
    slide_counter = 0
    for slide in SLIDES:
        slide_file = SLIDES_DIR / slide["file"]
        print(f"  Processing {slide['file']}...")

        if slide_file.exists():
            content = slide_file.read_text()

            # Extract body content
            body_content = extract_body_content(content)

            # Find all canvas IDs and make them unique
            chart_ids = re.findall(r'id="([^"]*Chart)"', body_content)
            for chart_id in set(chart_ids):
                unique_id = f"{chart_id}_{slide_counter}"
                # Update canvas ID
                body_content = body_content.replace(f'id="{chart_id}"', f'id="{unique_id}"')
                # Update any inline script references in the body
                body_content = body_content.replace(f"'{chart_id}'", f"'{unique_id}'")
                body_content = body_content.replace(f'"{chart_id}"', f'"{unique_id}"')

            # Extract scripts and make chart IDs unique
            scripts = extract_scripts(content)
            for script in scripts:
                # Update all chart IDs found in body
                for chart_id in set(chart_ids):
                    unique_id = f"{chart_id}_{slide_counter}"
                    script = script.replace(f"'{chart_id}'", f"'{unique_id}'")
                    script = script.replace(f'"{chart_id}"', f'"{unique_id}"')

                # Make ctx variable names unique to avoid conflicts
                script = script.replace('const ctx = ', f'const ctx_{slide_counter} = ')
                script = script.replace('const chart = ', f'const chart_{slide_counter} = ')

                # Replace Chart constructor calls, but NOT inside functions that have ctx as parameter
                # Check if this script has functions with ctx parameter - if so, leave those alone
                if 'function createPctChart(ctx,' in script or 'function createAbsChart(ctx,' in script:
                    # This slide has helper functions - don't touch ctx inside them
                    # Only replace direct Chart calls (not inside functions)
                    pass
                else:
                    # No helper functions, safe to replace all ctx references
                    script = script.replace('new Chart(ctx,', f'new Chart(ctx_{slide_counter},')
                    script = script.replace('new Chart(ctx ', f'new Chart(ctx_{slide_counter} ')

                all_scripts.append(script)

            # Wrap in section
            html_parts.append(f'        <!-- {slide["title"].upper()} -->\n')
            html_parts.append(f'        <section id="{slide["id"]}" class="slide-section">\n')
            html_parts.append(f'            {body_content}\n')
            html_parts.append('        </section>\n\n')

            slide_counter += 1
        else:
            print(f"  WARNING: {slide_file} not found!")

    # Add commentary section
    print("  Processing commentary...")
    if COMMENTARY_FILE.exists():
        commentary_content = COMMENTARY_FILE.read_text()
        commentary_body = extract_body_content(commentary_content)

        html_parts.append('        <!-- COMMENTARY -->\n')
        html_parts.append('        <section id="commentary" class="slide-section">\n')
        html_parts.append(f'            {commentary_body}\n')
        html_parts.append('        </section>\n\n')

    # Close content wrapper
    html_parts.append('    </div>\n\n')

    # Add all scripts
    html_parts.append('    <script>\n')
    for script in all_scripts:
        html_parts.append(f'        {script}\n\n')

    # Add navigation JavaScript
    html_parts.append('''
        // Smooth scroll for navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });

                    // Update active state
                    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                    this.classList.add('active');
                }
            });
        });

        // Update active nav link on scroll
        const sections = document.querySelectorAll('.slide-section');
        const navLinks = document.querySelectorAll('.nav-link');

        window.addEventListener('scroll', () => {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (window.scrollY >= (sectionTop - 150)) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        });
    </script>
''')

    # Close HTML
    html_parts.append('</body>\n</html>')

    # Write output
    output_html = ''.join(html_parts)
    OUTPUT_FILE.write_text(output_html)

    print(f"\n✓ Complete report built: {OUTPUT_FILE}")
    print(f"  Total size: {len(output_html):,} characters")
    print(f"  Slides included: {len(SLIDES)}")
    print(f"  Commentary included: Yes")

if __name__ == "__main__":
    build_combined_report()
