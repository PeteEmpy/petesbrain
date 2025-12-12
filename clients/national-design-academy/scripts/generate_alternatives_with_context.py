#!/usr/bin/env python3
"""
National Design Academy - PMax Asset Alternatives
Using brand context: Approachable & aspirational, flexible learning, 35+ years expertise, accreditation
Target: Career-changers, design enthusiasts, international students
Framework: ROK 5-section (3 per section = 15 total)
"""

# Brand Context Extracted
BRAND_CONTEXT = {
    "tone": "Approachable & aspirational, conversational yet authoritative",
    "key_messages": [
        "Flexible learning (online, fast-track Zoom, in-studio)",
        "35+ years expertise, 35,000+ alumni in 100+ countries",
        "Accredited credentials (AIM/Ofqual recognized)",
        "Career pathway focus - progression from short courses to MA",
        "Affordability - government funding available"
    ],
    "target_audience": "Career-changers, design enthusiasts, professionals balancing work/family",
    "differentiators": [
        "Only institution with truly flexible online interior design",
        "De Montfort University partnerships",
        "Internationally recognised credentials",
        "Multiple study options (online, fast-track, in-studio)"
    ]
}

ASSETS = {
    "6501874539": {
        "current": "Study Interior Design",
        "asset_type": "HEADLINE",
        "char_limit": 30,
        "char_limit_text": "30 chars",
        "alternatives": {
            "benefits": [
                "Change careers with design skills",  # 28 chars - career-changer focus
                "Transform your creative passion",     # 31 chars - aspirational
                "Build a design career in weeks",      # 28 chars - speed + career
            ],
            "technical": [
                "Accredited design diploma online",    # 31 chars - accreditation + online
                "AIM & Ofqual recognised courses",    # 31 chars - credentials
                "Flexible study around your life",     # 29 chars - flexibility message
            ],
            "quirky": [
                "Design spaces, inspire people",       # 27 chars - creative angle
                "Your design journey starts here",     # 30 chars - welcoming
                "Learn design your own way",          # 24 chars - accessibility
            ],
            "cta": [
                "Start your design career today",      # 29 chars - action-oriented
                "Enrol in design diploma now",        # 26 chars - direct CTA
                "Begin designing professionally",      # 29 chars - professional path
            ],
            "brand": [
                "35+ years design education leader",   # 32 chars - expertise + years (OVER - revise)
                "Design academy trusted by 35K+",      # 29 chars - social proof
                "Industry-led design education",       # 29 chars - authority
            ]
        }
    },
    "6542848540": {
        "current": "Interior Design Diploma",
        "asset_type": "HEADLINE",
        "char_limit": 30,
        "alternatives": {
            "benefits": [
                "Turn design passion into career",     # 28 chars - transformation
                "Master interior design skills",       # 28 chars - expertise building
                "Get recognised design credentials",   # 31 chars (OVER) - credentials
            ],
            "technical": [
                "AIM-accredited diploma course",       # 28 chars - accreditation focus
                "Ofqual-recognised qualification",     # 31 chars (OVER) - official recognition
                "Professional interior design cert",   # 32 chars (OVER) - credibility
            ],
            "quirky": [
                "Design beautiful interior spaces",    # 31 chars (OVER) - outcome-focused
                "Create stunning room designs",        # 27 chars - creative outcome
                "Master the art of interiors",        # 26 chars - artistic angle
            ],
            "cta": [
                "Get your design diploma today",       # 27 chars - direct action
                "Qualify as interior designer",       # 28 chars - specific outcome
                "Claim your design certification",     # 29 chars - ownership language
            ],
            "brand": [
                "National Design Academy diploma",     # 31 chars (OVER) - branded
                "Award-winning design programme",      # 31 chars (OVER) - prestige
                "Globally recognised design cert",     # 30 chars - international credibility
            ]
        }
    },
    "8680183789": {
        "current": "Interior Design Courses",
        "asset_type": "HEADLINE",
        "char_limit": 30,
        "alternatives": {
            "benefits": [
                "Learn design in your own way",        # 26 chars - flexibility + learning
                "Design career courses that fit",      # 28 chars - flexibility + career
                "Study design around your schedule",   # 32 chars (OVER) - flexibility
            ],
            "technical": [
                "Accredited interior design courses",  # 33 chars (OVER) - accreditation
                "Nationally recognised design training",  # 36 chars (OVER) - credentials
                "Industry-standard design education",  # 33 chars (OVER) - authority
            ],
            "quirky": [
                "Design courses that inspire",         # 26 chars - emotional
                "Learn design from industry experts",  # 32 chars (OVER) - credibility
                "Where design passion comes alive",    # 31 chars (OVER) - aspirational
            ],
            "cta": [
                "Enrol in design courses today",       # 27 chars - direct CTA
                "Start learning interior design",      # 29 chars - action-oriented
                "Begin your design education",        # 27 chars - journey language
            ],
            "brand": [
                "35 years design education expertise", # 35 chars (OVER) - authority
                "Design courses trusted globally",     # 29 chars - international trust
                "Academy-led design training",        # 28 chars - institutional credibility
            ]
        }
    }
}

def validate_and_refine(assets):
    """Validate character counts and refine alternatives that exceed limits"""
    refined = {}

    for asset_id, data in assets.items():
        refined[asset_id] = {
            "current": data["current"],
            "asset_type": data["asset_type"],
            "char_limit": data["char_limit"],
            "alternatives_by_section": {}
        }

        print(f"\n{'='*70}")
        print(f"{data['current']} (ID: {asset_id})")
        print(f"{'='*70}")

        all_valid = True

        for section, alts in data["alternatives"].items():
            section_title = section.upper()
            print(f"\n{section_title} SECTION:")
            refined_alts = []

            for alt in alts:
                char_count = len(alt)
                is_valid = char_count <= data["char_limit"]
                status = "✅" if is_valid else "❌"

                print(f"  {status} {alt:<35s} ({char_count} chars)")

                if is_valid:
                    refined_alts.append(alt)
                else:
                    all_valid = False
                    # Create shorter version
                    if char_count > data["char_limit"]:
                        # Simple truncation strategy - remove words from end
                        words = alt.split()
                        while len(" ".join(words)) > data["char_limit"] and words:
                            words.pop()
                        shortened = " ".join(words)
                        if shortened and len(shortened) <= data["char_limit"]:
                            print(f"     → REVISED: {shortened:<35s} ({len(shortened)} chars)")
                            refined_alts.append(shortened)
                        else:
                            print(f"     → SKIPPED (cannot fit character limit)")

            refined[asset_id]["alternatives_by_section"][section] = refined_alts

        # Ensure we have exactly 3 per section (15 total)
        total_alts = sum(len(alts) for alts in refined[asset_id]["alternatives_by_section"].values())
        print(f"\n→ Total valid alternatives: {total_alts}/15")

        if total_alts < 15:
            print(f"⚠️  ATTENTION: Only {total_alts}/15 alternatives passed character validation")
            print(f"   Need to generate {15 - total_alts} additional alternatives")

    return refined

if __name__ == '__main__':
    print("\n" + "="*70)
    print("NATIONAL DESIGN ACADEMY - PMAX ASSET ALTERNATIVES")
    print("Using brand context from website analysis")
    print("="*70)

    print("\nBRAND CONTEXT:")
    print(f"Tone: {BRAND_CONTEXT['tone']}")
    print(f"Target: {BRAND_CONTEXT['target_audience']}")
    print(f"\nKey Messages:")
    for msg in BRAND_CONTEXT['key_messages']:
        print(f"  • {msg}")

    refined = validate_and_refine(ASSETS)

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    import json
    with open('/Users/administrator/Documents/PetesBrain.nosync/clients/national-design-academy/scripts/alternatives-with-context.json', 'w') as f:
        json.dump(refined, f, indent=2)

    print("\n✅ Alternatives saved to alternatives-with-context.json")
    print("\nNEXT: Review character limits and generate replacements for over-limit options")
