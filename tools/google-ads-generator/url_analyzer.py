#!/usr/bin/env python3
"""
URL Content Analyzer
Extracts and analyzes website content for ad copy generation.
"""

import re
import json
from urllib.parse import urlparse


def analyze_url_content(url: str, page_content: str) -> dict:
    """
    Analyze URL and page content to extract key information for ad generation.

    Args:
        url: The target URL
        page_content: The fetched page content (HTML or markdown)

    Returns:
        dict with analyzed content including:
        - product_name
        - brand
        - key_features
        - benefits
        - technical_specs
        - unique_selling_points
    """

    analysis = {
        "url": url,
        "domain": urlparse(url).netloc,
        "product_name": "",
        "brand": "",
        "key_features": [],
        "benefits": [],
        "technical_specs": [],
        "unique_selling_points": [],
        "raw_content": page_content[:1000]  # First 1000 chars for reference
    }

    # Extract domain as potential brand name
    domain_parts = urlparse(url).netloc.split('.')
    if len(domain_parts) >= 2:
        analysis["brand"] = domain_parts[-2].title()

    # Basic content analysis (to be enhanced with AI)
    content_lower = page_content.lower()

    # Look for common product/feature indicators
    if "feature" in content_lower:
        analysis["key_features"].append("Features mentioned on page")

    if "benefit" in content_lower:
        analysis["benefits"].append("Benefits highlighted")

    # Look for technical terms
    tech_keywords = ["technology", "advanced", "innovative", "premium", "professional",
                     "patent", "certified", "award", "rated"]
    for keyword in tech_keywords:
        if keyword in content_lower:
            analysis["technical_specs"].append(f"Mentions {keyword}")

    return analysis


def extract_meta_info(html_content: str) -> dict:
    """Extract meta tags and structured data from HTML."""

    meta_info = {
        "title": "",
        "description": "",
        "keywords": []
    }

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if title_match:
        meta_info["title"] = title_match.group(1).strip()

    # Extract meta description
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']',
                           html_content, re.IGNORECASE)
    if desc_match:
        meta_info["description"] = desc_match.group(1).strip()

    # Extract meta keywords
    keywords_match = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']*)["\']',
                               html_content, re.IGNORECASE)
    if keywords_match:
        meta_info["keywords"] = [k.strip() for k in keywords_match.group(1).split(',')]

    return meta_info


def prepare_prompt_for_ai(url: str, content: str, ad_type: str = "rsa") -> str:
    """
    Prepare a detailed prompt for AI to generate ad copy based on URL content.

    Args:
        url: The target URL
        content: The page content
        ad_type: "rsa" for Responsive Search Ads or "asset_group" for Performance Max

    Returns:
        Formatted prompt string
    """

    meta_info = extract_meta_info(content)

    if ad_type == "rsa":
        prompt = f"""Based on the following website content, generate Google Ads RSA (Responsive Search Ads) text assets.

URL: {url}
Page Title: {meta_info.get('title', 'N/A')}
Meta Description: {meta_info.get('description', 'N/A')}

Content Summary:
{content[:2000]}

Please generate:

1. 50 HEADLINES (30 character maximum each) organized into 5 sections of 10 each:
   - Section 1 (Benefits): Explain why customers can't live without this product/service
   - Section 2 (Technical): Highlight technical advantages and features
   - Section 3 (Quirky): Creative, humorous descriptions with personality
   - Section 4 (Call to Action): Persuasive CTAs encouraging immediate purchase (not aggressive)
   - Section 5 (Brand/Category): Product/category descriptions highlighting the brand

2. 50 DESCRIPTIONS (90 character maximum each) following the same 5 sections as above

Requirements:
- Headlines must be 30 characters or less
- Descriptions must be 90 characters or less
- Maximize character usage while staying within limits
- Use a mix of informative, strong CTAs, features, benefits, and creative copy
- Be specific to this business and its products/services
- No Dynamic Keyword Insertion or customizers
- Include character counts for each

Format your response as a JSON object with this structure:
{{
    "headlines": {{
        "benefits": ["headline 1", "headline 2", ...],
        "technical": ["headline 1", "headline 2", ...],
        "quirky": ["headline 1", "headline 2", ...],
        "cta": ["headline 1", "headline 2", ...],
        "brand": ["headline 1", "headline 2", ...]
    }},
    "descriptions": {{
        "benefits": ["description 1", "description 2", ...],
        "technical": ["description 1", "description 2", ...],
        "quirky": ["description 1", "description 2", ...],
        "cta": ["description 1", "description 2", ...],
        "brand": ["description 1", "description 2", ...]
    }}
}}
"""
    else:  # asset_group
        prompt = f"""Based on the following website content, generate Google Ads Performance Max Asset Group text assets.

URL: {url}
Page Title: {meta_info.get('title', 'N/A')}
Meta Description: {meta_info.get('description', 'N/A')}

Content Summary:
{content[:2000]}

Please generate:

1. 50 SEARCH THEMES - All the different ways visitors might search for these products/services
2. 50 HEADLINES (30 character maximum) in 5 sections
3. 50 DESCRIPTIONS (90 character maximum) in 5 sections
4. 5 SITELINK suggestions with headlines (25 chars), two descriptions (35 chars each), and suggested URL paths
5. 5 CALLOUT EXTENSIONS (25 characters each)

Format your response as a JSON object with the complete asset group structure.
"""

    return prompt


if __name__ == "__main__":
    # Test with example
    test_url = "https://www.example.com/running-shoes"
    test_content = "<title>Premium Running Shoes | Example</title><meta name='description' content='High-performance running shoes for athletes'>"

    analysis = analyze_url_content(test_url, test_content)
    print(json.dumps(analysis, indent=2))

    prompt = prepare_prompt_for_ai(test_url, test_content, "rsa")
    print("\n" + "="*80)
    print("Generated Prompt:")
    print("="*80)
    print(prompt[:500] + "...")
