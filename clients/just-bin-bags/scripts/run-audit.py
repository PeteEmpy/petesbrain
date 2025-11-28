#!/usr/bin/env python3
"""
Execute Just Bin Bags Audit - Fetch live data and generate report
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Try to use MCP server's execute_gaql
try:
    sys.path.insert(0, str(PROJECT_ROOT / 'shared' / 'mcp-servers' / 'google-ads-mcp-server'))
    from oauth.google_auth import execute_gaql, format_customer_id
    GAQL_AVAILABLE = True
except ImportError:
    GAQL_AVAILABLE = False
    print("⚠️  Google Ads API not available - will generate template only")

CUSTOMER_ID = "9697059148"
CLIENT_NAME = "Just Bin Bags"

def format_micros(micros):
    """Convert micros to currency"""
    return micros / 1_000_000

def format_percent(value):
    """Format as percentage"""
    return f"{value * 100:.2f}%"

def calculate_roas(cost_micros, conv_value):
    """Calculate ROAS"""
    if cost_micros == 0:
        return 0.0
    return (conv_value / format_micros(cost_micros)) if format_micros(cost_micros) > 0 else 0.0

def fetch_campaign_data(days=7):
    """Fetch campaign-level performance data"""
    if not GAQL_AVAILABLE:
        return None
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    query = f"""
    SELECT
      campaign.id,
      campaign.name,
      campaign.status,
      campaign.advertising_channel_type,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value,
      metrics.ctr,
      metrics.average_cpc,
      metrics.cost_per_conversion
    FROM campaign
    WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
      AND campaign.status != 'REMOVED'
    ORDER BY metrics.cost_micros DESC
    """
    
    try:
        result = execute_gaql(CUSTOMER_ID, query)
        return result
    except Exception as e:
        print(f"Error fetching campaign data: {e}", file=sys.stderr)
        return None

def fetch_product_data(days=7):
    """Fetch product-level performance data"""
    if not GAQL_AVAILABLE:
        return None
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    query = f"""
    SELECT
      segments.product_item_id,
      segments.product_title,
      segments.product_brand,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value,
      metrics.ctr,
      metrics.average_cpc
    FROM shopping_performance_view
    WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY metrics.conversions_value DESC
    LIMIT 100
    """
    
    try:
        result = execute_gaql(CUSTOMER_ID, query)
        return result
    except Exception as e:
        print(f"Error fetching product data: {e}", file=sys.stderr)
        return None

def fetch_placement_data(days=7):
    """Fetch placement performance data"""
    if not GAQL_AVAILABLE:
        return None
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    query = f"""
    SELECT
      segments.placement,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value,
      metrics.ctr
    FROM placement_view
    WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY metrics.cost_micros DESC
    """
    
    try:
        result = execute_gaql(CUSTOMER_ID, query)
        return result
    except Exception as e:
        print(f"Error fetching placement data: {e}", file=sys.stderr)
        return None

def generate_audit_report(campaign_data, product_data, placement_data):
    """Generate comprehensive audit report"""
    
    report = []
    report.append("# Google Ads Audit: Just Bin Bags")
    report.append(f"**Date Range**: Last 7 days (Nov 2-9, 2025)")
    report.append(f"**Audit Date**: {datetime.now().strftime('%B %d, %Y')}")
    report.append(f"**Customer ID**: {CUSTOMER_ID}")
    report.append("")
    report.append("---")
    report.append("")
    
    # Executive Summary
    report.append("## Executive Summary")
    report.append("")
    
    if campaign_data and campaign_data.get('results'):
        total_spend = sum(format_micros(r.get('metrics', {}).get('costMicros', 0)) for r in campaign_data['results'])
        total_conv_value = sum(r.get('metrics', {}).get('conversionsValue', 0) for r in campaign_data['results'])
        total_conversions = sum(r.get('metrics', {}).get('conversions', 0) for r in campaign_data['results'])
        total_impressions = sum(r.get('metrics', {}).get('impressions', 0) for r in campaign_data['results'])
        total_clicks = sum(r.get('metrics', {}).get('clicks', 0) for r in campaign_data['results'])
        
        roas = calculate_roas(sum(r.get('metrics', {}).get('costMicros', 0) for r in campaign_data['results']), total_conv_value)
        ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
        
        report.append(f"**Overall Performance**:")
        report.append(f"- **Spend**: £{total_spend:,.2f}")
        report.append(f"- **Revenue**: £{total_conv_value:,.2f}")
        report.append(f"- **ROAS**: {roas:.2f}x ({roas*100:.0f}%)")
        report.append(f"- **Conversions**: {total_conversions:.0f}")
        report.append(f"- **CTR**: {ctr:.2f}%")
        report.append(f"- **CVR**: {cvr:.2f}%")
        report.append(f"- **CPA**: £{cpa:.2f}")
        report.append("")
        
        report.append(f"**Key Findings**:")
        if roas < 2.0:
            report.append(f"- ⚠️ ROAS below target (200% target indicated by campaign name)")
        if total_conversions == 0:
            report.append("- ⚠️ No conversions recorded in last 7 days")
        report.append("")
    else:
        report.append("*Live data fetch unavailable - see campaign analysis below*")
        report.append("")
    
    # Campaign Performance
    report.append("## Campaign Performance")
    report.append("")
    
    if campaign_data and campaign_data.get('results'):
        report.append("| Campaign | Type | Status | Spend | Revenue | ROAS | Conv. | CTR |")
        report.append("|----------|------|--------|-------|---------|------|-------|-----|")
        
        for row in campaign_data['results']:
            campaign_name = row.get('campaign', {}).get('name', 'N/A')
            campaign_type = row.get('campaign', {}).get('advertisingChannelType', 'N/A')
            status = row.get('campaign', {}).get('status', 'N/A')
            metrics = row.get('metrics', {})
            
            spend = format_micros(metrics.get('costMicros', 0))
            revenue = metrics.get('conversionsValue', 0)
            conversions = metrics.get('conversions', 0)
            roas = calculate_roas(metrics.get('costMicros', 0), revenue)
            ctr = metrics.get('ctr', 0) * 100 if metrics.get('ctr') else 0
            
            report.append(f"| {campaign_name} | {campaign_type} | {status} | £{spend:.2f} | £{revenue:.2f} | {roas:.2f}x | {conversions:.0f} | {ctr:.2f}% |")
        
        report.append("")
    else:
        report.append("*Campaign data unavailable - check MCP connection*")
        report.append("")
    
    # Product Performance
    report.append("## Product-Level Performance")
    report.append("")
    
    if product_data and product_data.get('results'):
        # Top 10 products
        report.append("### Top 10 Products by Revenue")
        report.append("")
        report.append("| Product | Impressions | Clicks | Spend | Revenue | ROAS | Conv. |")
        report.append("|---------|-------------|--------|-------|---------|------|-------|")
        
        sorted_products = sorted(product_data['results'], 
                                 key=lambda x: x.get('metrics', {}).get('conversionsValue', 0), 
                                 reverse=True)[:10]
        
        for row in sorted_products:
            product_title = row.get('segments', {}).get('productTitle', 'N/A')[:50]
            metrics = row.get('metrics', {})
            
            impressions = metrics.get('impressions', 0)
            clicks = metrics.get('clicks', 0)
            spend = format_micros(metrics.get('costMicros', 0))
            revenue = metrics.get('conversionsValue', 0)
            roas = calculate_roas(metrics.get('costMicros', 0), revenue)
            conversions = metrics.get('conversions', 0)
            
            report.append(f"| {product_title} | {impressions:,} | {clicks:,} | £{spend:.2f} | £{revenue:.2f} | {roas:.2f}x | {conversions:.0f} |")
        
        report.append("")
    else:
        report.append("*Product data unavailable - check MCP connection*")
        report.append("")
    
    # Placement Analysis
    report.append("## Placement Analysis")
    report.append("")
    
    if placement_data and placement_data.get('results'):
        report.append("| Placement | Impressions | Clicks | Spend | Revenue | ROAS | CTR |")
        report.append("|-----------|-------------|--------|-------|---------|------|-----|")
        
        for row in placement_data['results']:
            placement = row.get('segments', {}).get('placement', 'N/A')
            metrics = row.get('metrics', {})
            
            impressions = metrics.get('impressions', 0)
            clicks = metrics.get('clicks', 0)
            spend = format_micros(metrics.get('costMicros', 0))
            revenue = metrics.get('conversionsValue', 0)
            roas = calculate_roas(metrics.get('costMicros', 0), revenue)
            ctr = metrics.get('ctr', 0) * 100 if metrics.get('ctr') else 0
            
            report.append(f"| {placement} | {impressions:,} | {clicks:,} | £{spend:.2f} | £{revenue:.2f} | {roas:.2f}x | {ctr:.2f}% |")
        
        report.append("")
    else:
        report.append("*Placement data unavailable - check MCP connection*")
        report.append("")
    
    # Recommendations
    report.append("## Prioritized Recommendations")
    report.append("")
    report.append("1. **Review Campaign Performance** - Analyze both Performance Max campaigns")
    report.append("2. **Product Analysis** - Identify top performers and optimize budget allocation")
    report.append("3. **Placement Optimization** - Review placement performance and adjust as needed")
    report.append("4. **ROAS Target Review** - Campaign name suggests 200% ROAS target - verify performance")
    report.append("5. **JHD Brand Analysis** - Understand JHD sub-brand performance vs main brand")
    report.append("")
    
    # Next Steps
    report.append("## Next Steps")
    report.append("")
    report.append("- [ ] Review campaign structure and bidding strategy")
    report.append("- [ ] Analyze product-level performance in detail")
    report.append("- [ ] Check Product Impact Analyzer for feed changes")
    report.append("- [ ] Review conversion tracking setup")
    report.append("- [ ] Identify what JHD sub-brand represents")
    report.append("")
    
    return "\n".join(report)

def main():
    print("🔍 Fetching live data for Just Bin Bags audit...")
    print("")
    
    # Fetch data
    campaign_data = fetch_campaign_data(7)
    product_data = fetch_product_data(7)
    placement_data = fetch_placement_data(7)
    
    # Generate report
    report = generate_audit_report(campaign_data, product_data, placement_data)
    
    # Save to audit file
    audit_file = PROJECT_ROOT / 'clients' / 'just-bin-bags' / 'audits' / f"{datetime.now().strftime('%Y-%m-%d')}-weekly-audit.md"
    
    # Read existing template and replace results section
    template_file = PROJECT_ROOT / 'clients' / 'just-bin-bags' / 'audits' / '2025-11-09-weekly-audit-template.md'
    
    if template_file.exists():
        with open(template_file, 'r') as f:
            template = f.read()
        
        # Replace the results section
        if "## 📊 Audit Results" in template:
            parts = template.split("## 📊 Audit Results")
            new_template = parts[0] + "## 📊 Audit Results\n\n" + report + "\n\n---\n\n" + parts[1].split("---")[-1] if len(parts) > 1 else parts[0] + "## 📊 Audit Results\n\n" + report
        else:
            new_template = template + "\n\n---\n\n## 📊 Audit Results\n\n" + report
        
        with open(audit_file, 'w') as f:
            f.write(new_template)
        
        print(f"✅ Audit report saved to: {audit_file}")
    else:
        # Create new file
        with open(audit_file, 'w') as f:
            f.write(report)
        print(f"✅ Audit report saved to: {audit_file}")
    
    print("")
    print("📊 Audit Summary:")
    if campaign_data and campaign_data.get('results'):
        print(f"   - {len(campaign_data['results'])} campaign(s) analyzed")
    if product_data and product_data.get('results'):
        print(f"   - {len(product_data['results'])} product(s) analyzed")
    if placement_data and placement_data.get('results'):
        print(f"   - {len(placement_data['results'])} placement(s) analyzed")

if __name__ == "__main__":
    main()

