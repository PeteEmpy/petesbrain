#!/usr/bin/env python3
"""
Google Ads Campaign Builder
Web interface for creating campaigns, ad groups, and asset groups using MCP tools.
"""

from flask import Flask, render_template, request, jsonify
import subprocess
import json
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from keyword_generator import KeywordGenerator
from claude_copywriter import ClaudeCopywriter

app = Flask(__name__)

# Global storage for latest result
latest_result = None


def call_mcp_tool(tool_name, params):
    """
    Call an MCP tool via Claude Code CLI (if available) or direct Python import.
    For now, we'll use subprocess to call the MCP server directly.
    """
    # TODO: Implement MCP tool calling mechanism
    # This will depend on how we can invoke MCP tools from Flask
    # Options:
    # 1. Direct import of MCP server modules
    # 2. HTTP requests to running MCP server
    # 3. Subprocess calls to Claude Code CLI
    pass


def get_client_customer_id(client_name):
    """Get Google Ads customer ID for a client using MCP tool."""
    # Use mcp__google-ads__get_client_platform_ids
    # For now, return mock data
    client_ids = {
        'smythson': '8573235780',
        'tree2mydoor': '4941701449',
        'superspace': '6821627350',
        'devonshire-hotels': '1234567890',
        # Add more clients as needed
    }
    return client_ids.get(client_name.lower().replace(' ', '-'))


def list_campaigns(customer_id, campaign_type):
    """
    List campaigns of specified type using GAQL query via MCP.

    Args:
        customer_id: Google Ads customer ID
        campaign_type: 'PERFORMANCE_MAX' or 'SEARCH'

    Returns:
        List of campaign objects with id and name
    """
    # GAQL query to get campaigns
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status
        FROM campaign
        WHERE campaign.advertising_channel_type = '{campaign_type}'
            AND campaign.status != 'REMOVED'
        ORDER BY campaign.name
    """

    # TODO: Call mcp__google-ads__run_gaql with query
    # For now, return mock data
    if campaign_type == 'PERFORMANCE_MAX':
        return [
            {'id': '23233714033', 'name': 'SMY | UK | P Max | Christmas Gifting'},
            {'id': '23194794411', 'name': 'SMY | UK | P Max | Diaries'},
        ]
    else:  # SEARCH
        return [
            {'id': '12345', 'name': 'Brand | UK | Search | Main'},
            {'id': '67890', 'name': 'Generic | UK | Search | Main'},
        ]


def create_campaign(customer_id, campaign_data):
    """Create new campaign using MCP tool."""
    # Use mcp__google-ads__create_campaign
    # Ensure status is ALWAYS PAUSED
    campaign_data['status'] = 'PAUSED'

    # TODO: Call MCP tool
    # mcp__google-ads__create_campaign(**campaign_data)

    return {
        'success': True,
        'campaign_id': '99999',
        'message': 'Campaign created in PAUSED state'
    }


def create_ad_group(customer_id, campaign_id, ad_group_data):
    """Create new ad group using MCP tool."""
    # Use mcp__google-ads__create_ad_group
    # Ensure status is PAUSED
    ad_group_data['status'] = 'PAUSED'

    # TODO: Call MCP tool
    # mcp__google-ads__create_ad_group(customer_id, campaign_id, **ad_group_data)

    return {
        'success': True,
        'ad_group_id': '88888',
        'message': 'Ad group created in PAUSED state'
    }


def create_asset_group(customer_id, campaign_id, asset_group_data):
    """Create new asset group for Performance Max using MCP tool."""
    # Use mcp__google-ads__create_asset_group
    # Ensure status is PAUSED
    asset_group_data['status'] = 'PAUSED'

    # TODO: Call MCP tool
    # mcp__google-ads__create_asset_group(customer_id, campaign_id, **asset_group_data)

    return {
        'success': True,
        'asset_group_id': '77777',
        'message': 'Asset group created in PAUSED state'
    }


@app.route('/')
def index():
    """Main page with campaign builder form."""
    # Get list of clients from client-platform-ids.json
    clients = [
        'Smythson',
        'Tree2mydoor',
        'Superspace',
        'Devonshire Hotels',
        'Clear Prospects',
        'Godshot',
        'Crowd Control',
        # Add more clients
    ]

    return render_template('index.html', clients=clients)


@app.route('/api/get_campaigns', methods=['POST'])
def get_campaigns():
    """Get list of campaigns for selected client and type."""
    data = request.json
    client_name = data.get('client')
    campaign_type = data.get('campaign_type')

    # Get customer ID for client
    customer_id = get_client_customer_id(client_name)

    if not customer_id:
        return jsonify({'error': 'Client not found'}), 404

    # Get campaigns of specified type
    campaigns = list_campaigns(customer_id, campaign_type)

    return jsonify({'campaigns': campaigns})


@app.route('/api/create', methods=['POST'])
def create():
    """Create campaign/ad group/asset group based on form data."""
    global latest_result

    data = request.json
    client_name = data.get('client')
    action = data.get('action')  # 'new_campaign', 'new_ad_group', 'new_asset_group'

    # Get customer ID
    customer_id = get_client_customer_id(client_name)

    if not customer_id:
        return jsonify({'error': 'Client not found'}), 400

    try:
        if action == 'new_campaign':
            result = create_campaign(customer_id, data.get('campaign_data'))
        elif action == 'new_ad_group':
            campaign_id = data.get('campaign_id')
            result = create_ad_group(customer_id, campaign_id, data.get('ad_group_data'))
        elif action == 'new_asset_group':
            campaign_id = data.get('campaign_id')
            result = create_asset_group(customer_id, campaign_id, data.get('asset_group_data'))
        else:
            return jsonify({'error': 'Invalid action'}), 400

        latest_result = result
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/latest_result')
def get_latest_result():
    """Get the most recent creation result."""
    global latest_result
    return jsonify(latest_result or {'message': 'No results yet'})


@app.route('/api/generate_keywords', methods=['POST'])
def generate_keywords():
    """Generate high-quality keywords using AI with deduplication."""
    data = request.json
    url = data.get('url')
    client_name = data.get('client')
    max_keywords = data.get('max_keywords', 25)
    model = data.get('model', 'claude-3-haiku-20240307')  # Default to Haiku

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    if not client_name:
        return jsonify({'error': 'Client is required'}), 400

    try:
        # Get customer ID for deduplication checks
        customer_id = get_client_customer_id(client_name)

        # Generate keywords
        generator = KeywordGenerator(url, client_name, model=model)
        result = generator.generate_and_deduplicate(
            customer_id=customer_id,
            max_keywords=max_keywords
        )

        return jsonify(result)

    except Exception as e:
        print(f"Error generating keywords: {e}", flush=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate_rsa', methods=['POST'])
def generate_rsa():
    """Generate RSA ad copy using ClaudeCopywriter."""
    data = request.json
    url = data.get('url')
    client_name = data.get('client')
    context = data.get('context', '')
    model = data.get('model', 'claude-3-haiku-20240307')  # Default to Haiku

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        copywriter = ClaudeCopywriter(url, model=model)
        result = copywriter.generate_ad_copy(additional_context=context)

        # Add cost tracking
        cost = copywriter.calculate_cost()
        result['stats'] = {
            'cost': cost,
            'model': model,
            'input_tokens': copywriter.total_input_tokens,
            'output_tokens': copywriter.total_output_tokens
        }

        # Return headlines, descriptions, and stats
        return jsonify({
            'headlines': result.get('headlines', {}),
            'descriptions': result.get('descriptions', {}),
            'stats': result.get('stats', {})
        })

    except Exception as e:
        print(f"Error generating RSA: {e}", flush=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate_asset_group', methods=['POST'])
def generate_asset_group():
    """Generate asset group text assets using ClaudeCopywriter."""
    data = request.json
    url = data.get('url')
    client_name = data.get('client')
    context = data.get('context', '')
    model = data.get('model', 'claude-3-haiku-20240307')  # Default to Haiku

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        copywriter = ClaudeCopywriter(url, model=model)
        result = copywriter.generate_asset_group(additional_context=context)

        # Add cost tracking
        cost = copywriter.calculate_cost()
        result['stats'] = {
            'cost': cost,
            'model': model,
            'input_tokens': copywriter.total_input_tokens,
            'output_tokens': copywriter.total_output_tokens
        }

        # Return asset group text assets and stats
        return jsonify({
            'short_headlines': result.get('short_headlines', {}),
            'long_headlines': result.get('long_headlines', {}),
            'descriptions': result.get('descriptions', {}),
            'stats': result.get('stats', {})
        })

    except Exception as e:
        print(f"Error generating asset group: {e}", flush=True)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Starting Google Ads Campaign Builder...")
    print("📍 Open http://127.0.0.1:5003 in your browser")
    app.run(debug=True, port=5003)
