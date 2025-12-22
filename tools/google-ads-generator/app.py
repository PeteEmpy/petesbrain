#!/usr/bin/env python3
"""
Google Ads Text Generator - Web Application (Simplified - No Session)
Flask app that passes data directly without using sessions.
"""

from flask import Flask, render_template, request, jsonify, send_file
import sys
import importlib
import io
import csv
import json

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Import and reload the modules
import claude_copywriter
importlib.reload(claude_copywriter)
from claude_copywriter import ClaudeCopywriter

app = Flask(__name__)

# Store latest result in memory (simple, no sessions)
latest_result = None


@app.route('/')
def index():
    """Landing page with URL input."""
    global latest_result
    latest_result = None  # Clear on home page visit
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze URL and return data directly."""
    global latest_result

    # Reload the module on each request to pick up any code changes
    import importlib
    import claude_copywriter
    importlib.reload(claude_copywriter)
    from claude_copywriter import ClaudeCopywriter

    data = request.get_json()
    url = data.get('url', '').strip()
    context = data.get('context', '').strip()
    main_keyword = data.get('main_keyword', '').strip()
    review1 = data.get('review1', '').strip()
    review2 = data.get('review2', '').strip()
    ad_type = data.get('ad_type', 'rsa')

    # Build reviews list if provided
    social_proof_reviews = []
    if review1:
        social_proof_reviews.append(review1)
    if review2:
        social_proof_reviews.append(review2)

    print(f"\n{'='*80}", flush=True)
    print(f"ANALYZE REQUEST RECEIVED", flush=True)
    print(f"URL: {url}", flush=True)
    if context:
        print(f"Additional Context: {context}", flush=True)
    if main_keyword:
        print(f"Main Keyword: {main_keyword}", flush=True)
    if social_proof_reviews:
        print(f"Social Proof Reviews: {len(social_proof_reviews)} provided", flush=True)
    print(f"{'='*80}\n", flush=True)

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Use Claude API for professional copywriting
        copywriter = ClaudeCopywriter(url)

        print(f"Using Claude AI to generate {ad_type} assets...", flush=True)

        if ad_type == 'asset_group':
            result = copywriter.generate_asset_group(additional_context=context)
        else:
            result = copywriter.generate_ad_copy(
                additional_context=context,
                main_keyword=main_keyword,
                social_proof_reviews=social_proof_reviews if social_proof_reviews else None
            )

        # Store globally
        latest_result = result

        print(f"\nGenerated professional ad copy for: {url}", flush=True)
        print(f"Brand: {result['page_info']['brand']}", flush=True)
        print(f"Product: {result['page_info']['product']}", flush=True)
        # Handle both RSA (headlines) and asset groups (short_headlines)
        headlines_key = 'short_headlines' if ad_type == 'asset_group' else 'headlines'
        print(f"First headline: {result[headlines_key]['benefits'][0] if result[headlines_key]['benefits'] else 'N/A'}", flush=True)

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        return jsonify({"error": f"Failed to analyze URL: {str(e)}"}), 400


@app.route('/get_latest_data')
def get_latest_data():
    """API endpoint to get the latest analysis data."""
    global latest_result

    if not latest_result:
        return jsonify({"error": "No data available"}), 404

    print(f"Serving data for: {latest_result['url']}", flush=True)
    return jsonify(latest_result)


@app.route('/rsa_editor')
def rsa_editor():
    """RSA editor - loads data via JavaScript."""
    return render_template('rsa_editor_dynamic.html')


@app.route('/asset_group_editor')
def asset_group_editor():
    """Asset group editor - loads data via JavaScript."""
    return render_template('asset_group_editor_dynamic.html')


@app.route('/export_rsa_csv', methods=['POST'])
def export_rsa_csv():
    """Export selected RSA assets to CSV in Google Ads Editor format."""
    data = request.get_json()
    selected_items = data.get('selected_items', {})
    url = data.get('url', '')

    output = io.StringIO()
    writer = csv.writer(output)

    # Collect all headlines and descriptions (flatten from sections)
    all_headlines = []
    for section, headlines in selected_items.get('headlines', {}).items():
        all_headlines.extend(headlines)

    all_descriptions = []
    for section, descriptions in selected_items.get('descriptions', {}).items():
        all_descriptions.extend(descriptions)

    # Limit to max 15 headlines and 4 descriptions per Google Ads RSA spec
    all_headlines = all_headlines[:15]
    all_descriptions = all_descriptions[:4]

    # Google Ads Editor RSA CSV format
    # Ad type,Final URL,Path 1,Path 2,Headline 1-15,Description 1-4
    header = ['Ad type', 'Final URL', 'Path 1', 'Path 2']

    # Add headline columns (up to 15)
    for i in range(1, 16):
        header.append(f'Headline {i}')

    # Add description columns (up to 4)
    for i in range(1, 5):
        header.append(f'Description {i}')

    writer.writerow(header)

    # Write data row
    row = [
        'Responsive search ad',  # Ad type
        url,  # Final URL
        '',  # Path 1 (optional)
        ''   # Path 2 (optional)
    ]

    # Add headlines (pad with empty strings if less than 15)
    for i in range(15):
        if i < len(all_headlines):
            row.append(all_headlines[i])
        else:
            row.append('')

    # Add descriptions (pad with empty strings if less than 4)
    for i in range(4):
        if i < len(all_descriptions):
            row.append(all_descriptions[i])
        else:
            row.append('')

    writer.writerow(row)

    output.seek(0)
    csv_bytes = io.BytesIO(output.getvalue().encode('utf-8'))
    csv_bytes.seek(0)

    return send_file(
        csv_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name='google_ads_rsa_assets.csv'
    )


@app.route('/get_copy_text', methods=['POST'])
def get_copy_text():
    """Get formatted text for clipboard - matches CSV format for easy paste."""
    data = request.get_json()
    selected_items = data.get('selected_items', {})
    url = data.get('url', '')

    # Collect all headlines and descriptions (flatten from sections)
    all_headlines = []
    for section, headlines in selected_items.get('headlines', {}).items():
        all_headlines.extend(headlines)

    all_descriptions = []
    for section, descriptions in selected_items.get('descriptions', {}).items():
        all_descriptions.extend(descriptions)

    # Limit to max 15 headlines and 4 descriptions
    all_headlines = all_headlines[:15]
    all_descriptions = all_descriptions[:4]

    # Build tab-separated text (matches CSV structure)
    lines = []

    # Header row
    header_parts = ['Ad type', 'Final URL', 'Path 1', 'Path 2']
    for i in range(1, 16):
        header_parts.append(f'Headline {i}')
    for i in range(1, 5):
        header_parts.append(f'Description {i}')
    lines.append('\t'.join(header_parts))

    # Data row
    row_parts = ['Responsive search ad', url, '', '']

    # Add headlines (pad with empty strings if less than 15)
    for i in range(15):
        if i < len(all_headlines):
            row_parts.append(all_headlines[i])
        else:
            row_parts.append('')

    # Add descriptions (pad with empty strings if less than 4)
    for i in range(4):
        if i < len(all_descriptions):
            row_parts.append(all_descriptions[i])
        else:
            row_parts.append('')

    lines.append('\t'.join(row_parts))

    return jsonify({"text": "\n".join(lines)})


@app.route('/export_asset_group_headlines_desc', methods=['POST'])
def export_asset_group_headlines_desc():
    """Export selected headlines, long headlines, and descriptions for asset group to CSV.

    Performance Max Asset Group Specs:
    - Headlines: 30 chars max, 3-15 count
    - Long Headlines: 90 chars max, 1-5 count
    - Descriptions: 90 chars max, 3-5 count
    """
    data = request.get_json()
    headlines = data.get('headlines', [])
    long_headlines = data.get('long_headlines', [])
    descriptions = data.get('descriptions', [])
    url = data.get('url', '')
    asset_group_name = data.get('asset_group_name', '')

    output = io.StringIO()
    writer = csv.writer(output)

    # Google Ads Editor format for Performance Max Asset Groups (Section 8)
    # Single row with all assets as columns
    header = [
        'Campaign', 'Asset group', 'Asset group status', 'Final URL', 'Path 1', 'Path 2',
        'Headline 1', 'Headline 2', 'Headline 3', 'Headline 4', 'Headline 5',
        'Headline 6', 'Headline 7', 'Headline 8', 'Headline 9', 'Headline 10',
        'Headline 11', 'Headline 12', 'Headline 13', 'Headline 14', 'Headline 15',
        'Long headline 1', 'Long headline 2', 'Long headline 3', 'Long headline 4', 'Long headline 5',
        'Description 1', 'Description 2', 'Description 3', 'Description 4', 'Description 5',
        'Business name', 'Call to action text',
        'Image asset', 'Logo asset', 'Square image asset', 'Landscape logo asset', 'YouTube video asset'
    ]
    writer.writerow(header)

    # Prepare data row
    row = [
        '',  # Campaign (user fills in)
        asset_group_name,  # Asset group
        'Enabled',  # Asset group status
        url,  # Final URL
        '',  # Path 1
        ''   # Path 2
    ]

    # Add up to 15 regular headlines (30 char max each)
    for i in range(15):
        if i < len(headlines):
            row.append(headlines[i])
        else:
            row.append('')

    # Add up to 5 long headlines (90 char max each)
    for i in range(5):
        if i < len(long_headlines):
            row.append(long_headlines[i])
        else:
            row.append('')

    # Add up to 5 descriptions (90 char max each)
    for i in range(5):
        if i < len(descriptions):
            row.append(descriptions[i])
        else:
            row.append('')

    # Add remaining fields (empty for user to fill)
    row.extend(['', '', '', '', '', '', ''])  # Business name, CTA, Image, Logo, Square image, Landscape logo, Video

    writer.writerow(row)

    output.seek(0)
    csv_bytes = io.BytesIO(output.getvalue().encode('utf-8'))
    csv_bytes.seek(0)

    return send_file(
        csv_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name='asset_group.csv'
    )


@app.route('/export_sitelinks_csv', methods=['POST'])
def export_sitelinks_csv():
    """Export selected sitelinks to CSV in Google Ads Editor format."""
    data = request.get_json()
    sitelinks = data.get('sitelinks', [])

    output = io.StringIO()
    writer = csv.writer(output)

    # Sitelink Extensions CSV format
    writer.writerow(['Sitelink text', 'Description line 1',
                     'Description line 2', 'Final URL', 'Device preference',
                     'Start date', 'End date', 'Schedule'])

    # Write sitelinks
    for sitelink in sitelinks:
        writer.writerow([
            sitelink.get('headline', ''),
            sitelink.get('description_1', ''),
            sitelink.get('description_2', ''),
            sitelink.get('url', ''),
            '',  # Device preference
            '',  # Start date
            '',  # End date
            ''   # Schedule
        ])

    output.seek(0)
    csv_bytes = io.BytesIO(output.getvalue().encode('utf-8'))
    csv_bytes.seek(0)

    return send_file(
        csv_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name='sitelinks.csv'
    )


@app.route('/export_snippets_csv', methods=['POST'])
def export_snippets_csv():
    """Export selected structured snippets to CSV in Google Ads Editor format."""
    data = request.get_json()
    snippets = data.get('snippets', [])

    output = io.StringIO()
    writer = csv.writer(output)

    # Structured Snippets CSV format
    writer.writerow(['Header', 'Values', 'Device preference',
                     'Start date', 'End date', 'Schedule'])

    # Write snippets
    for snippet in snippets:
        writer.writerow([
            snippet.get('header', ''),
            ', '.join(snippet.get('values', [])),  # Values as comma-separated
            '',  # Device preference
            '',  # Start date
            '',  # End date
            ''   # Schedule
        ])

    output.seek(0)
    csv_bytes = io.BytesIO(output.getvalue().encode('utf-8'))
    csv_bytes.seek(0)

    return send_file(
        csv_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name='structured_snippets.csv'
    )


@app.route('/export_callouts_csv', methods=['POST'])
def export_callouts_csv():
    """Export selected callouts to CSV in Google Ads Editor format."""
    data = request.get_json()
    callouts = data.get('callouts', [])

    output = io.StringIO()
    writer = csv.writer(output)

    # Callout Extensions CSV format
    writer.writerow(['Callout text', 'Device preference',
                     'Start date', 'End date', 'Schedule'])

    # Write callouts
    for callout in callouts:
        writer.writerow([
            callout,
            '',  # Device preference
            '',  # Start date
            '',  # End date
            ''   # Schedule
        ])

    output.seek(0)
    csv_bytes = io.BytesIO(output.getvalue().encode('utf-8'))
    csv_bytes.seek(0)

    return send_file(
        csv_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name='callouts.csv'
    )


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("GOOGLE ADS TEXT GENERATOR (Session-Free Version)")
    print("=" * 80)
    print("\nStarting web application...")
    print("Open your browser and navigate to: http://localhost:5001")
    print("\nPress Ctrl+C to stop the server.")
    print("=" * 80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5001)
