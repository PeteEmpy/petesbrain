#!/usr/bin/env python3
"""
Google Ads Text Generator - Web Application
Flask app for generating and managing Google Ads text assets.
"""

from flask import Flask, render_template, request, jsonify, send_file, session
import sys
import importlib
import io
import csv
import secrets
import json

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Import and reload the modules to ensure we get the latest code
import website_analyzer
import professional_ad_writer
importlib.reload(website_analyzer)
importlib.reload(professional_ad_writer)
from website_analyzer import WebsiteAnalyzer
from professional_ad_writer import ProfessionalAdWriter

app = Flask(__name__)

# Generate new secret key on every app start - invalidates all old sessions
app.secret_key = secrets.token_hex(16)

# Disable session permanence - sessions only last while browser is open
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 0


@app.after_request
def add_header(response):
    """Add headers to prevent caching."""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/')
def index():
    """Landing page with URL input."""
    # Clear any previous session data for fresh start
    session.clear()

    response = render_template('index.html')
    return response


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze URL and redirect to appropriate editor."""
    # Clear old session data before analyzing new URL
    session.clear()

    data = request.get_json()
    url = data.get('url', '').strip()
    ad_type = data.get('ad_type', 'rsa')

    print(f"\n{'='*80}", flush=True)
    print(f"ANALYZE REQUEST RECEIVED", flush=True)
    print(f"URL: {url}", flush=True)
    print(f"Ad Type: {ad_type}", flush=True)
    print(f"{'='*80}\n", flush=True)

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Analyze website deeply
    print("Creating WebsiteAnalyzer...", flush=True)
    try:
        analyzer = WebsiteAnalyzer(url)

        print("Analyzing website (crawling multiple pages)...", flush=True)
        analyzer.analyze_site()

        print("Extracting insights...", flush=True)
        insights = analyzer.get_insights_summary()

        print("Generating professional ad copy...", flush=True)
        writer = ProfessionalAdWriter(insights)
        ads = writer.generate_complete_rsa()

        print(f"Generation complete!", flush=True)

        # Format result for the RSA editor template
        result = {
            'headlines': ads['headlines'],
            'descriptions': ads['descriptions'],
            'page_info': {
                'brand': insights.get('brand_name', ''),
                'product': ', '.join(insights.get('main_products', [])[:3]),
                'category': insights.get('product_category', '')
            }
        }

        # Add debug info
        debug_info = {
            "product_name": ', '.join(insights.get('main_products', [])[:3]),
            "category": insights.get('product_category', ''),
            "brand": insights.get('brand_name', ''),
            "pages_analyzed": len(analyzer.visited_pages),
            "benefits_found": len(insights.get('key_benefits', [])),
            "features_found": len(insights.get('technical_features', []))
        }
        result['debug_info'] = debug_info

        print(f"\n{'='*80}", flush=True)
        print(f"ANALYZED URL: {url}", flush=True)
        print(f"Brand: {debug_info['brand']}", flush=True)
        print(f"Product: {debug_info['product_name']}", flush=True)
        print(f"Pages analyzed: {debug_info['pages_analyzed']}", flush=True)
        print(f"Benefits found: {debug_info['benefits_found']}", flush=True)
        print(f"Features found: {debug_info['features_found']}", flush=True)
        print(f"{'='*80}\n", flush=True)

    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        return jsonify({"error": f"Failed to analyze URL: {str(e)}"}), 400

    # Store in session
    session['rsa_data'] = result
    session['url'] = url
    session['ad_type'] = ad_type

    # Add timestamp to force fresh page load (cache busting)
    import time
    timestamp = int(time.time() * 1000)

    return jsonify({
        "success": True,
        "ad_type": ad_type,
        "redirect": f"/{ad_type}_editor?t={timestamp}",
        "debug": debug_info
    })


@app.route('/rsa_editor')
def rsa_editor():
    """RSA editor with selection interface."""
    from flask import redirect, url_for

    rsa_data = session.get('rsa_data')
    url = session.get('url')

    if not rsa_data:
        # No data - redirect to home page
        print("No rsa_data in session, redirecting to home", flush=True)
        return redirect(url_for('index'))

    # Debug: print what we're rendering
    print(f"\n{'='*80}", flush=True)
    print(f"RSA EDITOR - Rendering page with data:", flush=True)
    print(f"URL: {url}", flush=True)
    print(f"Brand: {rsa_data.get('page_info', {}).get('brand', 'N/A')}", flush=True)
    print(f"First headline: {list(rsa_data.get('headlines', {}).values())[0][0] if rsa_data.get('headlines') else 'N/A'}", flush=True)
    print(f"{'='*80}\n", flush=True)

    return render_template('rsa_editor.html',
                          url=url,
                          headlines=rsa_data['headlines'],
                          descriptions=rsa_data['descriptions'],
                          page_info=rsa_data['page_info'])


@app.route('/asset_group_editor')
def asset_group_editor():
    """Asset group editor (placeholder for future implementation)."""
    return render_template('asset_group_editor.html',
                          message="Asset Group editor coming soon!")


@app.route('/export_rsa_csv', methods=['POST'])
def export_rsa_csv():
    """Export selected RSA assets to CSV for Google Ads Editor."""
    data = request.get_json()
    selected_headlines = data.get('headlines', [])
    selected_descriptions = data.get('descriptions', [])
    url = data.get('url', '')

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Google Ads Editor CSV format for RSA
    # Header row
    writer.writerow(['Ad type', 'Text', 'Final URL'])

    # Headlines
    for headline in selected_headlines:
        writer.writerow(['Responsive search ad headline', headline, url])

    # Descriptions
    for description in selected_descriptions:
        writer.writerow(['Responsive search ad description', description, url])

    # Convert to bytes for download
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
    """Get formatted text for clipboard copy."""
    data = request.get_json()
    selected_headlines = data.get('headlines', [])
    selected_descriptions = data.get('descriptions', [])
    url = data.get('url', '')

    # Format for copying
    lines = []
    lines.append("=" * 80)
    lines.append("GOOGLE ADS RSA TEXT ASSETS")
    lines.append("=" * 80)
    lines.append(f"Final URL: {url}")
    lines.append("")

    lines.append("HEADLINES (30 char max)")
    lines.append("-" * 80)
    for i, headline in enumerate(selected_headlines, 1):
        lines.append(f"{i:2d}. {headline:<30} [{len(headline):2d} chars]")

    lines.append("")
    lines.append("DESCRIPTIONS (90 char max)")
    lines.append("-" * 80)
    for i, description in enumerate(selected_descriptions, 1):
        lines.append(f"{i:2d}. {description:<90} [{len(description):2d} chars]")

    lines.append("")
    lines.append("=" * 80)

    return jsonify({"text": "\n".join(lines)})


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("GOOGLE ADS TEXT GENERATOR")
    print("=" * 80)
    print("\nStarting web application...")
    print("Open your browser and navigate to: http://localhost:5001")
    print("\nPress Ctrl+C to stop the server.")
    print("=" * 80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5001)
