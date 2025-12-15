#!/usr/bin/env python3
"""
Generate alternatives for the 32 asset texts that don't have them yet
"""

import os
import json
import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic

URL = "https://www.nda.ac.uk/"

# Asset texts that need alternatives (from the sheet analysis)
MISSING_ASSETS = {
    "HEADLINE": [
        "Become an Interior Designer",
        "Online Interior Design Courses",
        "National Design Academy"
    ],
    "LONG_HEADLINE": [
        "The Only Online Professional Interior Design Diploma for a Recognized Qualification",
        "Leading Provider of Fully Accredited Interior Design Courses. Come Join 35,000+ Graduates",
        "35,000+ Interior Design Graduates – Join India's Most Trusted Design Academy",
        "Start Your Own Business or Enter a New Career With Our Interior Design Diploma",
        "Study At Home Full/Part-Time. Flexible Affordable Online Qualifications. 30+ Years Success",
        "Worlds Leading Provider Fully Accredited Interior Design Courses - Join 35,000+ Graduates",
        "National Design Academy Is the Only Institution to Offer Truly Flexible Online Courses",
        "Leading Provider of Interior Design Degrees. Government Funding. Join 35,000+ Graduates",
        "Choose from 5 Different Interior Design Degrees. BA (Hons) & Master's Degrees.",
        "Enrol at Any Time & Choose Your Start Date. No Term Times or Semesters.",
        "No Exams — Tutor Assessment Of Design Projects & Moderation By de Montfort University",
        "Leading Provider of Interior Design Degrees. - Join 35,000+ Graduates",
        "Study Full/Part-Time - Flexible Affordable Qualifications - 35+ Years Success",
        "Professional Interior Design AIM awards and KHDA Approved",
        "Launch Your Interior Design Career or Start Your Own Studio With Our Diploma",
        "National Design Academy Offers Truly Flexible Fully Accredited Courses"
    ],
    "DESCRIPTION": [
        "Study At Home Full/Part-Time. Flexible Affordable Online Qualifications. 30+ Years Success",
        "Our Diploma Courses Awarded by AIM, an Ofqual Approved National Awarding Organisation",
        "Leading Provider of Fully Accredited Interior Design Courses. Come Join 35,000+ Graduates",
        "Study Full/Part-Time. Flexible Affordable Qualifications. 35+ Years Success",
        "Complete a Professional Diploma in Interior Design – Career Ready in 3-12 Months",
        "Worlds Leading Provider of Accredited Interior Design Courses. Join 35,000+ Graduates NOW",
        "Leading Provider of Fully Accredited Interior Design Degrees. Come Join 35,000+ Graduates",
        "You Will Study Eight Dedicated Units During This Professional Diploma. Top Qualification",
        "Interior Design Diploma In-Studio Courses",
        "Interior Design Diploma Online & In-Studio Courses",
        "Become A Proffesional Interior Designer in as Little as Twelve Weeks!",
        "Study Full/Part-Time. Flexible Affordable Online Qualifications. 30+ Years Success",
        "Our Diploma Courses Awarded by AIM, KHDA and are Internationally Recognised"
    ]
}

def fetch_website_content(url: str) -> str:
    """Fetch and extract clean text content from NDA website."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    for tag in soup(['script', 'style', 'nav', 'footer']):
        tag.decompose()

    title = soup.find('title')
    title_text = title.get_text() if title else ""

    meta_desc = soup.find('meta', attrs={'name': 'description'}) or \
               soup.find('meta', attrs={'property': 'og:description'})
    meta_text = meta_desc.get('content', '') if meta_desc else ""

    h1_tags = [h1.get_text().strip() for h1 in soup.find_all('h1')[:8]]
    h2_tags = [h2.get_text().strip() for h2 in soup.find_all('h2')[:20]]
    paragraphs = [p.get_text().strip() for p in soup.find_all('p')[:35] if len(p.get_text().strip()) > 30]
    
    content = f"""
URL: {url}
TITLE: {title_text}
META DESCRIPTION: {meta_text}
MAIN HEADINGS (H1): {', '.join(h1_tags[:5])}
SECTION HEADINGS (H2): {', '.join(h2_tags[:10])}
KEY CONTENT: {' '.join(paragraphs[:10])}
"""
    return content.strip()


def generate_alternatives_batch(website_content: str, asset_texts: list, asset_type: str) -> dict:
    """Generate alternatives for a batch of asset texts using Claude."""
    
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    client = Anthropic(api_key=api_key)
    
    # Determine what to generate based on asset type
    if asset_type == "HEADLINE":
        instructions = """
For EACH asset text, generate EXACTLY 15 short headlines (30 chars max) organized into 5 sections:
- Benefits (3 headlines)
- Technical (3 headlines)
- Quirky (3 headlines)
- CTA (3 headlines)
- Brand (3 headlines)

Character requirements:
- MAXIMUM: 30 characters
- TARGET: 25-30 characters
- Use sentence case only

Return JSON format:
{
  "Asset Text 1": {
    "current": "Asset Text 1",
    "section_breakdown": {
      "Benefits": ["headline1", "headline2", "headline3"],
      "Technical": ["headline1", "headline2", "headline3"],
      "Quirky": ["headline1", "headline2", "headline3"],
      "CTA": ["headline1", "headline2", "headline3"],
      "Brand": ["headline1", "headline2", "headline3"]
    }
  },
  ...
}
"""
    elif asset_type == "LONG_HEADLINE":
        instructions = """
For EACH asset text, generate EXACTLY 10 long headlines (90 chars max) organized into 5 sections:
- Benefits (2 long headlines)
- Technical (2 long headlines)
- Quirky (2 long headlines)
- CTA (2 long headlines)
- Brand (2 long headlines)

Character requirements:
- MAXIMUM: 90 characters
- TARGET: 75-90 characters
- ONE complete, flowing sentence
- Use sentence case only

Return JSON format:
{
  "Asset Text 1": {
    "current": "Asset Text 1",
    "long_headlines": {
      "Benefits": ["headline1", "headline2"],
      "Technical": ["headline1", "headline2"],
      "Quirky": ["headline1", "headline2"],
      "CTA": ["headline1", "headline2"],
      "Brand": ["headline1", "headline2"]
    }
  },
  ...
}
"""
    else:  # DESCRIPTION
        instructions = """
For EACH asset text, generate EXACTLY 10 descriptions (90 chars max) organized into 5 sections:
- Benefits (2 descriptions)
- Technical (2 descriptions)
- Quirky (2 descriptions)
- CTA (2 descriptions)
- Brand (2 descriptions)

Character requirements:
- MAXIMUM: 90 characters
- TARGET: 75-90 characters
- ONE complete, flowing sentence
- Persuasive, benefit-focused
- Use sentence case only

Return JSON format:
{
  "Asset Text 1": {
    "current": "Asset Text 1",
    "descriptions": {
      "Benefits": ["desc1", "desc2"],
      "Technical": ["desc1", "desc2"],
      "Quirky": ["desc1", "desc2"],
      "CTA": ["desc1", "desc2"],
      "Brand": ["desc1", "desc2"]
    }
  },
  ...
}
"""

    assets_list = "\n".join([f"{i+1}. {text}" for i, text in enumerate(asset_texts)])
    
    prompt = f"""You are an ELITE Google Ads copywriter creating Performance Max asset alternatives.

ASSET TEXTS TO REWRITE ({asset_type}):
{assets_list}

{instructions}

NDA KEY USPs (USE THESE):
- 35+ years teaching interior design (established 1991)
- 35,000+ graduates worldwide
- UK accredited (AIM Awards, Ofqual regulated)
- 100% online, flexible study
- From short courses to BA (Hons) degrees
- University partner for degree programmes
- Career-focused, practical training
- 0% finance available

WEBSITE CONTENT:
{website_content[:2000]}

CRITICAL REQUIREMENTS:
✓ EXACT character limits (30 for short, 90 for long/descriptions)
✓ EXACT counts per section (3 short OR 2 long/desc)
✓ Sentence case ONLY (not title case)
✓ Specific to NDA and interior design
✓ Use actual USPs from the list above

Return ONLY valid JSON, no other text."""

    print(f"\nGenerating alternatives for {len(asset_texts)} {asset_type} assets...", flush=True)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text
    
    # Extract JSON
    import re
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        response_text = json_match.group(0)

    return json.loads(response_text)


def main():
    print("="*70)
    print("GENERATE MISSING NDA PMAX ALTERNATIVES")
    print("="*70)
    
    # Fetch website content
    print("\nFetching NDA website content...")
    website_content = fetch_website_content(URL)
    print(f"✅ Fetched content ({len(website_content)} chars)")
    
    # Load existing alternatives
    existing_file = 'clients/national-design-academy/scripts/final-alternatives-for-dropdowns.json'
    with open(existing_file, 'r') as f:
        existing_alternatives = json.load(f)
    
    print(f"\n✅ Loaded {len(existing_alternatives)} existing alternatives")
    
    # Generate for each type
    all_new_alternatives = {}
    
    for asset_type, asset_texts in MISSING_ASSETS.items():
        if not asset_texts:
            continue
            
        print(f"\n{'='*70}")
        print(f"PROCESSING: {asset_type} ({len(asset_texts)} texts)")
        print(f"{'='*70}")
        
        # Process in smaller batches to avoid token limits
        batch_size = 5
        for i in range(0, len(asset_texts), batch_size):
            batch = asset_texts[i:i+batch_size]
            print(f"\nBatch {i//batch_size + 1}/{(len(asset_texts)-1)//batch_size + 1}")
            
            result = generate_alternatives_batch(website_content, batch, asset_type)
            all_new_alternatives.update(result)
            
            print(f"  ✅ Generated {len(result)} alternatives")
    
    # Merge with existing
    print(f"\n{'='*70}")
    print("MERGING WITH EXISTING ALTERNATIVES")
    print(f"{'='*70}")
    
    # Create merged structure
    merged = {}
    
    # Add existing (with all three types)
    for asset_id, data in existing_alternatives.items():
        merged[data['current']] = data
    
    # Add new alternatives
    for asset_text, data in all_new_alternatives.items():
        if asset_text in merged:
            # Merge into existing entry
            if 'section_breakdown' in data:
                merged[asset_text]['section_breakdown'] = data['section_breakdown']
            if 'long_headlines' in data:
                merged[asset_text]['long_headlines'] = data['long_headlines']
            if 'descriptions' in data:
                merged[asset_text]['descriptions'] = data['descriptions']
        else:
            # Create new entry
            merged[asset_text] = data
    
    # Convert back to asset ID keys (create IDs from hash of text)
    import hashlib
    final_output = {}
    for asset_text, data in merged.items():
        # Use existing asset ID if available, otherwise generate one
        existing_id = None
        for aid, adata in existing_alternatives.items():
            if adata.get('current') == asset_text:
                existing_id = aid
                break
        
        if existing_id:
            final_output[existing_id] = data
        else:
            # Generate synthetic ID
            asset_id = str(int(hashlib.md5(asset_text.encode()).hexdigest()[:10], 16))
            final_output[asset_id] = data
    
    # Save
    output_file = 'clients/national-design-academy/scripts/final-alternatives-for-dropdowns.json'
    with open(output_file, 'w') as f:
        json.dump(final_output, f, indent=2)
    
    print(f"\n✅ Saved {len(final_output)} total alternatives to {output_file}")
    print(f"  • Previously: {len(existing_alternatives)} asset texts")
    print(f"  • Generated: {len(all_new_alternatives)} new asset texts")
    print(f"  • Total: {len(final_output)} asset texts")


if __name__ == "__main__":
    main()
