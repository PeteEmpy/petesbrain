#!/usr/bin/env python3
"""
Generate 15 alternative headline options for each HIGH priority NDA PMax asset
Uses Claude API following ROK text generation framework
"""

import os
import json
import subprocess
from anthropic import Anthropic

client = Anthropic()

# HIGH priority assets that need alternatives
HIGH_PRIORITY_ASSETS = [
    {
        "asset_id": "6501874539",
        "current_text": "Study Interior Design",
        "asset_type": "HEADLINE",
        "field_type": "HEADLINE",
        "char_limit": 30,
        "context": "Interior design diploma courses, UK-based, professional accreditation, flexible delivery"
    },
    {
        "asset_id": "6542848540",
        "current_text": "Interior Design Diploma",
        "asset_type": "HEADLINE",
        "field_type": "HEADLINE",
        "char_limit": 30,
        "context": "Professional interior design diploma, accredited, international recognition, KHDA approved"
    },
    {
        "asset_id": "8680183789",
        "current_text": "Interior Design Courses",
        "asset_type": "HEADLINE",
        "field_type": "HEADLINE",
        "char_limit": 30,
        "context": "Flexible, part-time and full-time interior design courses, professional certification"
    }
]

def generate_alternatives(asset):
    """Generate 15 alternative headline options for an asset"""

    prompt = f"""You are a Google Ads copywriter specializing in educational courses. Generate exactly 15 alternative headlines for this interior design diploma course.

CURRENT HEADLINE: "{asset['current_text']}"
CHARACTER LIMIT: {asset['char_limit']} characters (strict)
ASSET TYPE: {asset['field_type']}
CONTEXT: {asset['context']}

REQUIREMENTS:
1. Each headline must be EXACTLY under {asset['char_limit']} characters
2. Follow ROK 5-section framework:
   - 3 Benefits-focused (value, outcomes, transformation)
   - 3 Technical-focused (credentials, accreditation, features)
   - 3 Quirky-focused (creative, attention-grabbing, memorable)
   - 3 CTA-focused (action-oriented, urgency, invitation)
   - 3 Brand-focused (authority, trust, credibility)
3. Use sentence case (capitalize first word and proper nouns only)
4. Avoid superlatives (best, greatest, amazing)
5. Be specific about interior design (not generic "courses")
6. Consider the underperformance of the current headline (CTR is low - need to boost engagement)

OUTPUT FORMAT:
Return ONLY a JSON array with exactly 15 headline options:
[
  "headline 1 (XX chars)",
  "headline 2 (XX chars)",
  ...
]

Do not include explanations or numbering - just the JSON array."""

    response = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    try:
        # Extract JSON from response
        response_text = response.content[0].text.strip()
        alternatives = json.loads(response_text)

        # Validate character limits
        valid_alternatives = []
        for alt in alternatives:
            if len(alt) <= asset['char_limit']:
                valid_alternatives.append(alt)

        if len(valid_alternatives) < 15:
            print(f"  ⚠️  Only {len(valid_alternatives)}/15 alternatives passed character limit validation")

        return valid_alternatives[:15]

    except json.JSONDecodeError:
        print(f"  ❌ Failed to parse JSON response")
        return []

def main():
    print("=" * 80)
    print("NATIONAL DESIGN ACADEMY - PMax HEADLINE GENERATION")
    print("=" * 80)
    print()

    all_alternatives = {}

    for asset in HIGH_PRIORITY_ASSETS:
        print(f"Generating alternatives for: {asset['current_text']}")
        alternatives = generate_alternatives(asset)

        if alternatives:
            all_alternatives[asset['asset_id']] = {
                "current": asset['current_text'],
                "alternatives": alternatives
            }
            print(f"  ✅ Generated {len(alternatives)} alternatives")
            for i, alt in enumerate(alternatives[:5], 1):
                print(f"     {i}. {alt}")
            if len(alternatives) > 5:
                print(f"     ... and {len(alternatives) - 5} more")
        else:
            print(f"  ❌ Failed to generate alternatives")
        print()

    # Save to file
    output_path = '/Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/generated-alternatives.json'
    with open(output_path, 'w') as f:
        json.dump(all_alternatives, f, indent=2)

    print("=" * 80)
    print(f"✅ COMPLETE - {len(all_alternatives)} assets processed")
    print(f"   Alternatives saved to: {output_path}")
    print()
    print("NEXT STEPS:")
    print("1. Review alternatives above")
    print("2. Update Google Sheet with dropdown options")
    print("3. Select top alternatives for implementation")
    print("4. Use implement-asset-changes.py to deploy")
    print("=" * 80)

if __name__ == '__main__':
    main()
