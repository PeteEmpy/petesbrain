#!/usr/bin/env python3
"""
Generate NDA PMax headline alternatives using Claude AI
Uses the same technique as the Google Ads Text Generator
"""

import os
import json
import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic

# NDA URL
URL = "https://www.nda.ac.uk/"

# The 7 unique asset texts we need alternatives for
ASSET_TEXTS = {
    "6501874539": "Study Interior Design",
    "6542848540": "Interior Design Diploma",
    "8680183789": "Interior Design Courses",
    "8680134790": "Online Interior Design Degrees",
    "6503351051": "Interior Design Degree",
    "10422358209": "Price-Match Guarantee",
    "182887527317": "Intensive Fast-Track Diplomas"
}

def fetch_website_content(url: str) -> str:
    """Fetch and extract clean text content from NDA website."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove scripts, styles, navigation
    for tag in soup(['script', 'style', 'nav', 'footer']):
        tag.decompose()

    title = soup.find('title')
    title_text = title.get_text() if title else ""

    meta_desc = soup.find('meta', attrs={'name': 'description'}) or \
               soup.find('meta', attrs={'property': 'og:description'})
    meta_text = meta_desc.get('content', '') if meta_desc else ""

    h1_tags = [h1.get_text().strip() for h1 in soup.find_all('h1')[:8]]
    h2_tags = [h2.get_text().strip() for h2 in soup.find_all('h2')[:20]]
    h3_tags = [h3.get_text().strip() for h3 in soup.find_all('h3')[:15]]
    paragraphs = [p.get_text().strip() for p in soup.find_all('p')[:35] if len(p.get_text().strip()) > 30]
    list_items = [li.get_text().strip() for li in soup.find_all('li')[:40] if len(li.get_text().strip()) > 15]
    buttons = [btn.get_text().strip() for btn in soup.find_all(['button', 'a']) if btn.get_text().strip() and len(btn.get_text().strip()) < 50]
    buttons = list(set(buttons))[:10]

    content = f"""
URL: {url}

TITLE: {title_text}

META DESCRIPTION: {meta_text}

MAIN HEADINGS (H1):
{chr(10).join('- ' + h for h in h1_tags if h)}

SECTION HEADINGS (H2):
{chr(10).join('- ' + h for h in h2_tags if h)}

SUB-HEADINGS (H3):
{chr(10).join('- ' + h for h in h3_tags if h)}

BUTTONS/CALLS TO ACTION:
{chr(10).join('- ' + btn for btn in buttons if btn)}

KEY POINTS/FEATURES:
{chr(10).join('- ' + item for item in list_items[:20] if item)}

MAIN BODY CONTENT:
{chr(10).join(paragraphs[:15])}
"""
    return content.strip()


def generate_headlines_for_assets(website_content: str) -> dict:
    """Use Claude to generate headline alternatives for each asset text."""

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = Anthropic(api_key=api_key)

    # Build the list of assets we need alternatives for
    assets_list = "\n".join([f"- {text}" for text in ASSET_TEXTS.values()])

    prompt = f"""You are an ELITE copywriter with 20+ years experience writing Google Ads copy.

Your task: Create EXCEPTIONAL Performance Max asset alternatives for each of the 7 underperforming PMax headlines below. These headlines are currently underperforming (low CTR, 0 conversions) and need fresh alternatives.

CURRENT UNDERPERFORMING HEADLINES (need alternatives for each):
{assets_list}

WEBSITE CONTENT FOR CONTEXT:
{website_content}

═══════════════════════════════════════════════════════════════════
NDA KEY USPs (USE THESE IN YOUR COPY):
═══════════════════════════════════════════════════════════════════
- 35+ years teaching interior design (established 1991)
- 35,000+ graduates worldwide
- UK accredited (AIM Awards, Ofqual regulated)
- 100% online, flexible study
- From short courses to BA (Hons) degrees
- Study from anywhere in the world
- University partner for degree programmes
- Career-focused, practical training
- Personal tutor support
- Payment plans and 0% finance available

═══════════════════════════════════════════════════════════════════
GENERATE THREE ASSET TYPES FOR EACH - STRICT REQUIREMENTS:
═══════════════════════════════════════════════════════════════════

For EACH of the 7 asset texts, you MUST generate ALL of the following:

1. SHORT HEADLINES (EXACTLY 15 total - EXACTLY 3 per section, NO EXCEPTIONS)
   ⚠️ MAXIMUM: 30 characters (Google's hard limit)
   ⚠️ TARGET: 27-30 characters (REQUIRED!)
   ⚠️ MINIMUM: 25 characters
   🚨 YOU MUST PROVIDE EXACTLY 3 HEADLINES FOR EACH OF THE 5 SECTIONS = 15 TOTAL

2. LONG HEADLINES (EXACTLY 10 total - EXACTLY 2 per section, NO EXCEPTIONS)
   ⚠️ MAXIMUM: 90 characters (Google's hard limit)
   ⚠️ TARGET: 80-90 characters (REQUIRED!)
   ⚠️ MINIMUM: 75 characters
   - ONE complete, flowing sentence
   - Expand on the short headline concept
   🚨 YOU MUST PROVIDE EXACTLY 2 LONG HEADLINES FOR EACH OF THE 5 SECTIONS = 10 TOTAL

3. DESCRIPTIONS (EXACTLY 10 total - EXACTLY 2 per section, NO EXCEPTIONS)
   ⚠️ MAXIMUM: 90 characters (Google's hard limit)
   ⚠️ TARGET: 80-90 characters (REQUIRED!)
   ⚠️ MINIMUM: 75 characters
   - ONE complete, flowing sentence
   - Persuasive, benefit-focused
   🚨 YOU MUST PROVIDE EXACTLY 2 DESCRIPTIONS FOR EACH OF THE 5 SECTIONS = 10 TOTAL

SECTIONS (ALL 5 REQUIRED for EVERY asset type):
- Benefits: Customer-focused value propositions (3 short, 2 long, 2 desc)
- Technical: Accreditations, qualifications, specifics (3 short, 2 long, 2 desc)
- Quirky: Creative, attention-grabbing, memorable (3 short, 2 long, 2 desc)
- CTA: Action-oriented, compelling next steps (3 short, 2 long, 2 desc)
- Brand: Heritage, trust, positioning (3 short, 2 long, 2 desc)

🚨 CRITICAL: Every section MUST have the exact count specified. Do NOT skip any section. Do NOT provide fewer items than required. If you struggle with a section, be more creative - there are ALWAYS 3 ways to say something.

CAPITALIZATION: SENTENCE CASE ONLY
✓ "Earn your BA degree online" (correct)
✗ "Earn Your BA Degree Online" (wrong - title case)

QUALITY STANDARDS:
✓ Use NDA's actual USPs (35 years, 35,000 graduates, UK accredited, etc.)
✓ Sentence case only
✓ Specific to interior design education
✓ Match professional yet approachable tone
✓ No generic phrases - be specific to NDA
✓ MAXIMIZE character usage in every asset

Return ONLY valid JSON with EXACTLY these asset IDs:
{{
  "6501874539": {{
    "current": "Study Interior Design",
    "section_breakdown": {{
      "Benefits": ["short 1", "short 2", "short 3"],
      "Technical": ["short 1", "short 2", "short 3"],
      "Quirky": ["short 1", "short 2", "short 3"],
      "CTA": ["short 1", "short 2", "short 3"],
      "Brand": ["short 1", "short 2", "short 3"]
    }},
    "long_headlines": {{
      "Benefits": ["long 1", "long 2"],
      "Technical": ["long 1", "long 2"],
      "Quirky": ["long 1", "long 2"],
      "CTA": ["long 1", "long 2"],
      "Brand": ["long 1", "long 2"]
    }},
    "descriptions": {{
      "Benefits": ["desc 1", "desc 2"],
      "Technical": ["desc 1", "desc 2"],
      "Quirky": ["desc 1", "desc 2"],
      "CTA": ["desc 1", "desc 2"],
      "Brand": ["desc 1", "desc 2"]
    }}
  }},
  "6542848540": {{
    "current": "Interior Design Diploma",
    ... same structure ...
  }},
  "8680183789": {{
    "current": "Interior Design Courses",
    ... same structure ...
  }},
  "8680134790": {{
    "current": "Online Interior Design Degrees",
    ... same structure ...
  }},
  "6503351051": {{
    "current": "Interior Design Degree",
    ... same structure ...
  }},
  "10422358209": {{
    "current": "Price-Match Guarantee",
    ... same structure ...
  }},
  "182887527317": {{
    "current": "Intensive Fast-Track Diplomas",
    ... same structure ...
  }}
}}

CRITICAL: Use EXACTLY these 7 asset IDs: 6501874539, 6542848540, 8680183789, 8680134790, 6503351051, 10422358209, 182887527317

Return ONLY the JSON, no other text."""

    print("Sending to Claude AI...", flush=True)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        temperature=0.7,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    response_text = message.content[0].text

    # Extract JSON
    import re
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        response_text = json_match.group(0)

    result = json.loads(response_text)

    # Validate character limits and counts
    print("\nValidating character limits and counts...", flush=True)
    sections = ["Benefits", "Technical", "Quirky", "CTA", "Brand"]

    shortfall_errors = []

    for asset_id, asset_data in result.items():
        asset_name = asset_data.get('current', asset_id)

        # Validate short headlines (25-30 chars) - need exactly 3 per section
        for section in sections:
            if section in asset_data.get("section_breakdown", {}):
                valid_headlines = []
                for headline in asset_data["section_breakdown"][section]:
                    char_count = len(headline)
                    if char_count > 30:
                        print(f"  ✗ Short headline removed (>{30} chars): {headline}", flush=True)
                    elif char_count < 20:
                        print(f"  ✗ Short headline removed (<20 chars): {headline}", flush=True)
                    else:
                        valid_headlines.append(headline)
                asset_data["section_breakdown"][section] = valid_headlines

                # Check count
                if len(valid_headlines) < 3:
                    shortfall_errors.append(f"{asset_name} - section_breakdown.{section}: got {len(valid_headlines)}, need 3")
            else:
                shortfall_errors.append(f"{asset_name} - section_breakdown.{section}: MISSING")

        # Validate long headlines (75-90 chars) - need exactly 2 per section
        for section in sections:
            if section in asset_data.get("long_headlines", {}):
                valid_long = []
                for headline in asset_data["long_headlines"][section]:
                    char_count = len(headline)
                    if char_count > 90:
                        print(f"  ✗ Long headline removed (>{90} chars): {headline[:50]}...", flush=True)
                    elif char_count < 60:
                        print(f"  ✗ Long headline removed (<60 chars): {headline}", flush=True)
                    else:
                        valid_long.append(headline)
                asset_data["long_headlines"][section] = valid_long

                # Check count
                if len(valid_long) < 2:
                    shortfall_errors.append(f"{asset_name} - long_headlines.{section}: got {len(valid_long)}, need 2")
            else:
                shortfall_errors.append(f"{asset_name} - long_headlines.{section}: MISSING")

        # Validate descriptions (75-90 chars) - need exactly 2 per section
        for section in sections:
            if section in asset_data.get("descriptions", {}):
                valid_desc = []
                for desc in asset_data["descriptions"][section]:
                    char_count = len(desc)
                    if char_count > 90:
                        print(f"  ✗ Description removed (>{90} chars): {desc[:50]}...", flush=True)
                    elif char_count < 60:
                        print(f"  ✗ Description removed (<60 chars): {desc}", flush=True)
                    else:
                        valid_desc.append(desc)
                asset_data["descriptions"][section] = valid_desc

                # Check count
                if len(valid_desc) < 2:
                    shortfall_errors.append(f"{asset_name} - descriptions.{section}: got {len(valid_desc)}, need 2")
            else:
                shortfall_errors.append(f"{asset_name} - descriptions.{section}: MISSING")

    # Report shortfalls
    if shortfall_errors:
        print("\n" + "="*70)
        print("⚠️  SHORTFALL WARNINGS - Some sections have fewer items than required:")
        print("="*70)
        for error in shortfall_errors:
            print(f"  • {error}")
        print(f"\nTotal shortfalls: {len(shortfall_errors)}")
    else:
        print("\n✅ All sections have required counts")

    return result


def main():
    print("="*70)
    print("NDA PMAX HEADLINE ALTERNATIVES - CLAUDE AI GENERATION")
    print("="*70)

    print("\nFetching NDA website content...", flush=True)
    website_content = fetch_website_content(URL)
    print(f"✅ Fetched {len(website_content)} characters of content", flush=True)

    print("\nGenerating headline alternatives via Claude...", flush=True)
    result = generate_headlines_for_assets(website_content)

    # Save to file
    output_file = '/Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/final-alternatives-for-dropdowns.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Saved to {output_file}")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    total_short = 0
    total_long = 0
    total_desc = 0

    for asset_id, asset_data in result.items():
        short_count = sum(len(v) for v in asset_data.get("section_breakdown", {}).values())
        long_count = sum(len(v) for v in asset_data.get("long_headlines", {}).values())
        desc_count = sum(len(v) for v in asset_data.get("descriptions", {}).values())

        total_short += short_count
        total_long += long_count
        total_desc += desc_count

        print(f"\n{asset_data.get('current', asset_id)}:")
        print(f"  Short headlines: {short_count}")
        print(f"  Long headlines: {long_count}")
        print(f"  Descriptions: {desc_count}")

        # Show examples
        for section in ["Benefits", "Technical"]:
            if section in asset_data.get("section_breakdown", {}) and asset_data["section_breakdown"][section]:
                print(f"  Example short ({section}): {asset_data['section_breakdown'][section][0]} [{len(asset_data['section_breakdown'][section][0])} chars]")
                break

        for section in ["Benefits", "Technical"]:
            if section in asset_data.get("long_headlines", {}) and asset_data["long_headlines"][section]:
                print(f"  Example long ({section}): {asset_data['long_headlines'][section][0][:50]}... [{len(asset_data['long_headlines'][section][0])} chars]")
                break

        for section in ["Benefits", "Technical"]:
            if section in asset_data.get("descriptions", {}) and asset_data["descriptions"][section]:
                print(f"  Example desc ({section}): {asset_data['descriptions'][section][0][:50]}... [{len(asset_data['descriptions'][section][0])} chars]")
                break

    print(f"\n" + "="*70)
    print(f"TOTALS:")
    print(f"  Short headlines (30 chars): {total_short}")
    print(f"  Long headlines (90 chars): {total_long}")
    print(f"  Descriptions (90 chars): {total_desc}")
    print(f"  TOTAL ASSETS: {total_short + total_long + total_desc}")


if __name__ == "__main__":
    main()
