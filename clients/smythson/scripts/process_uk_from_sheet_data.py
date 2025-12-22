#!/usr/bin/env python3
"""
Process UK spreadsheet data and create update JSON.
This script correctly separates headlines (columns 5-19) from descriptions (columns 20-23).
"""

import json
from pathlib import Path

# UK spreadsheet data (27 rows fetched from MCP)
UK_SHEET_DATA = [
    ["13811031042", "SMY | UK | Search | Brand Exact", "128117925481", "UK - Brand", "784157361259", "Smythson of Bond Street™", "British heritage since 1887", "Over 135 years of expertise", "Shop luxury leather pieces", "Free delivery on orders £300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Shop luxury stocking fillers", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Luxury personalised gifts", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/"],
    ["13811031042", "SMY | UK | Search | Brand Exact", "187903967924", "UK - Brand - Sale", "784408654524", "Smythson of Bond Street™", "British heritage since 1887", "Shop luxury leather pieces", "Free delivery on orders £300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Over 135 years of expertise", "", "Timeless leather craftsmanship", "Personalise your order today", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "137137030701", "UK - semi-brand - home - desk accessories - blotters", "784228048462", "Smythson of Bond Street™", "Luxury leather blotters", "Discover gifts for him & her", "Shop luxury leather blotters", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "", "", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1888", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/home/accessories/desk-accessories"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "137137030981", "UK - semi-brand - home - games", "784228048447", "Smythson of Bond Street™", "Luxury games & playing cards", "Discover gifts for him & her", "Shop games & playing cards", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "Shop luxury game sets", "Handcrafted card & table games", "Shop exquisite luxury games", "", "", "", "Discover classic artisan poker and backgammon sets, each crafted with exceptional detail", "Ensure every event is memorable with our luxurious entertainment collection", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/home/accessories/games"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "141157046398", "UK - semi-brand - home - gifts", "784228048453", "Smythson of Bond Street™", "Luxury gifts", "Discover gifts for him & her", "Shop luxury gifts", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "Shop luxury leather gifts", "Luxury gifts for her", "Luxury gifts for him", "Explore luxury Christmas gifts", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "Make this festive season truly special with Smythson's curated collection of luxury gifts.", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/gifts/christmas-gifts"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "137137030741", "UK - semi-brand - home - jewellery boxes", "784228048465", "Smythson of Bond Street™", "Luxury leather jewellery boxes", "Discover gifts for him & her", "Shop luxury jewellery boxes", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "Shop leather jewellery boxes", "", "", "", "", "", "Keep your treasures & keepsakes beautifully organized with our leather jewellery boxes", "Make this festive season truly special with Smythson's curated collection of luxury gifts.", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/home/accessories/jewellery-boxes-rolls"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "137137030781", "UK - semi-brand - home - jewellery boxes - trinket cases", "784228048444", "Smythson of Bond Street™", "Luxury leather trinket cases", "Discover gifts for him & her", "Shop luxury trinket cases", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "Shop leather trinket cases", "", "", "", "", "", "Keep your dressing table or desk in order with our luxury trinket trays and cases.", "Make this festive season truly special with Smythson's curated collection of luxury gifts.", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/home/accessories/trinket-trays"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "137137030941", "UK - semi-brand - home - jewellery boxes - trinket trays", "784228048456", "Smythson of Bond Street™", "Luxury leather trinket trays", "Discover gifts for him & her", "Shop luxury trinket trays", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "Shop leather trinket trays", "", "", "", "", "", "Keep your dressing table or desk in order with our luxury trinket trays and cases.", "Make this festive season truly special with Smythson's curated collection of luxury gifts.", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/home/accessories/trinket-trays"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "121861436342", "UK - semi-brand - home - photo albums - albums", "784228048459", "Smythson of Bond Street™", "Luxury leather photo albums", "Discover gifts for him & her", "Shop luxury photo albums", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "", "", "", "", "", "", "", "Make this festive season truly special with Smythson's curated collection of luxury gifts.", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/home/accessories/frames-albums"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "137137031021", "UK - semi-brand - home - photo frames - frames", "784228048468", "Smythson of Bond Street™", "Luxury leather photo frames", "Discover gifts for him & her", "Shop luxury photo frames", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "", "", "", "", "", "", "", "Make this festive season truly special with Smythson's curated collection of luxury gifts.", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/home/accessories/frames-albums"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "137137031181", "UK - semi-brand - home - watch boxes", "784228048450", "Smythson of Bond Street™", "Leather watch boxes", "Discover gifts for him & her", "Shop leather watch boxes", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "", "", "", "", "", "", "", "Make this festive season truly special with Smythson's curated collection of luxury gifts.", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/home/accessories/watch-cufflink-boxes"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "183725950777", "UK - semi-brand - stationery - notebooks", "784197388692", "Smythson of Bond Street™", "Luxury leather notebooks", "Shop Smythson notebooks", "Shop leather notebooks", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "Handcrafted leather notebooks", "Timeless leather pieces", "fom", "", "", "", "Each of our notebooks is hand-bound and packed full of our signature Featherweight paper.", "Make this festive season truly special with Smythson's curated collection of luxury gifts.", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/diaries-and-books/notebooks/all-notebooks"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "145878157888", "UK - semi-brand - stationary - Birthday Cards", "780966363483", "Smythson of Bond Street™", "Luxury birthday cards", "Over 135 years of expertise", "Luxury paper craftsmanship", "Free delivery on orders £300+", "Discover new arrivals", "Enjoy complimentary returns", "Personalise your order today", "Discover gifts for him & her", "Exclusive luxury gift wrapping", "Uncover our latest collection", "Discover timeless collections", "Crafted for modern life", "", "", "Discover our selection of hand-engraved birthday cards.", "Design your own suite of stationery & personalise your order with our gold stamp service.", "Discover new arrivals from luxury leather stationery, accessories, bags, notebooks & more.", "Explore our bespoke stationery services for a suite that's uniquely yours.", "https://www.smythson.com/uk/stationery/cards/birthday-cards"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "145878157808", "UK - semi-brand - stationary - Notelets", "780374687964", "Luxury notelets by Smythson", "Notelets with tissue envelopes", "Heritage notelets since 1887", "Notelets for every occasion", "Notelets for refined tastes", "Discover Smythson notelets", "Luxury notelet collection", "Smythson signature notelets", "Shop notelets collection today", "Luxury paper notelets", "", "", "", "", "", "Browse Smythson's distinguished range of notelets for every correspondence occasion.", "Shop notelets that arrive beautifully packaged in Smythson's signature presentation.", "Premium British notelets featuring hand-engraved designs and tissue-lined envelopes.", "Luxury notelets that make every thank you, acceptance, or greeting truly memorable.", "https://www.smythson.com/uk/stationery/cards"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "145878157328", "UK - semi-brand - stationery - Personalised Stationery - Generic", "780374687982", "Smythson of Bond Street™", "Luxury personalised stationery", "Exquisite engraving available", "Order custom stationery today", "Luxury custom stationery", "135 years of personal service", "British bespoke stationery", "Add your personal touch today", "Choose your perfect design", "Choose border & layout styles", "Designed by you crafted by us", "Shop exquisite stationery", "Create your perfect letterhead", "", "", "Smythson personalisation service brings bespoke luxury to your correspondence.", "Create bespoke stationery that perfectly represents your individual style.", "Distinguished personalisation options for business cards and correspondence alike.", "Exclusive personalisation service for those who appreciate bespoke quality.", "https://www.smythson.com/uk/stationery"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "145878157648", "UK - semi-brand - stationery - correspondence cards", "780374687985", "Smythson of Bond Street™", "Distinguished card range", "Smythson writing cards", "Luxury correspondence cards", "Make letters beautiful", "Luxury correspondence sets", "Find perfect writing cards", "Correspondence excellence", "Over 135 years of letter craft", "", "", "", "", "", "", "Make every letter beautiful with handcrafted correspondence cards from Smythson.", "The ultimate in British luxury correspondence cards for discerning letter writers.", "Over 135 years of expertise evident in every handcrafted correspondence card we produce.", "Hand-lined envelopes complement each card for a complete luxury writing experience.", "https://www.smythson.com/uk/stationery/cards/correspondence-cards"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "145878157368", "UK - semi-brand - stationery - invitations", "780374687991", "Smythson invitation cards", "Luxury invitation cards", "Hand-engraved invitations", "Make events truly special", "Matching envelope invites", "Exquisite invitation sets", "Distinguished invites range", "Shop invitation cards today", "Shop exquisite stationery", "", "", "", "", "", "", "Smythson invitations combine traditional craftsmanship with contemporary elegance.", "Find the ideal invitation cards from Britain's premier stationery house since 1887.", "Smythson creates invitations for hosts who value exceptional quality.", "Transform event planning with invitations that guests will admire and remember.", "https://www.smythson.com/uk/stationery/cards/invitations"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "145878157568", "UK - semi-brand - stationery - pencil cases", "780374687979", "Smythson leather pencil cases", "Luxury leather pencil cases", "Expertly crafted pencil cases", "Cases worth the investment", "Quality leather pen cases", "Luxury panama leather cases", "Over 135 years of expertise", "Explore leather case designs", "Browse luxury case collection", "British heritage leather cases", "Personalisation available", "Heritage pencil case craft", "", "", "", "Smythson creates pencil cases for those who value quality and organisation.", "Luxury British pencil cases featuring the finest Panama leather and expert construction.", "Discover pencil cases worthy of your finest pens and creative tools.", "Expertly crafted from durable Panama leather for stationery storage that lasts a lifetime.", "https://www.smythson.com/uk/leather-goods/accessories/pencil-cases"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "145878157408", "UK - semi-brand - stationery - pencils", "780374687976", "Smythson pen craftsmanship", "Smythson writing excellence", "Over 135 years of expertise", "Luxury pens & pencils range", "Fountain pens from Smythson", "Luxury British pens & pencils", "Luxury writing essentials", "Find your writing style today", "Pens to inspire every word", "Luxury writing companions", "Complete writing solutions", "Smythson signature pencils", "Fountain & rollerball pens", "", "", "From fountain & rollerball pens to our signature gold gilded pencils, shop now.", "Smythson creates writing instruments for those who value excellence.", "Discover new arrivals from luxury leather stationery, accessories, bags, notebooks & more.", "Explore our bespoke stationery services for a suite that's uniquely yours.", "https://www.smythson.com/uk/stationery/pens-pencils"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "128117974201", "UK - semi-brand - stationery - plain stationery - envelopes", "780374687967", "Smythson quality envelopes", "Smythson envelope excellence", "Watermarked white laid style", "Distinguished envelope range", "Exquisite envelope quality", "King & A4 envelope sizes", "Handcrafted British envelopes", "British crafted excellence", "Shop exquisite stationery", "", "", "", "", "", "", "Smythson London creates envelopes for those who value quality in every detail.", "Lovingly handcrafted envelopes that transform ordinary letters into special deliveries.", "British made envelopes combining traditional craftsmanship with contemporary elegance.", "", "https://www.smythson.com/uk/stationery/plain-stationery/envelopes"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "128117974241", "UK - semi-brand - stationery - plain stationery paper", "780374687973", "Smythson luxury writing paper", "Discover writing excellence", "Luxury writing paper", "Plain stationery excellence", "Classic plain stationery range", "Writing paper & envelope sets", "Signature handcrafted luxury", "Smythson plain paper range", "Luxury plain writing paper", "Handcrafted writing excellence", "", "", "", "", "", "Smythson creates plain stationery for those who value quality correspondence.", "Find writing materials that inspire you to put pen to paper more often than ever before.", "Transform ordinary messages into extraordinary correspondence with luxury plain paper.", "Smythson plain stationery where simplicity meets luxury in perfect harmony.", "https://www.smythson.com/uk/stationery/plain-stationery"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "153607315370", "UK - semi-brand - stationery - stationery", "780374687970", "Smythson of Bond Street™", "Smythson writing excellence", "Luxury stationery selection", "Distinguished stationery range", "Express elegance in writing", "Find your writing style", "Browse full collections online", "Exclusive British stationery", "137 years stationery expertise", "Heritage writing collections", "Refined writing accessories", "", "", "", "", "Smythson stationery bringing timeless sophistication to modern communication.", "Distinguished collections encompassing every aspect of luxury writing.", "137 years creating stationery that elevates the art of handwritten communication.", "Browse our full range of writing accessories and fine stationery options online.", "https://www.smythson.com/uk/stationery"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "145878157848", "UK - semi-brand - stationery - thank you cards", "780374687988", "Smythson of Bond Street™", "Luxury thank you cards", "Cards for heartfelt thanks", "Luxury paper craftsmanship", "Express recognition in style", "Gratitude cards & notelets", "Thank you cards worth keeping", "Sophisticated thank you notes", "Find your thank you style", "", "", "", "", "", "", "Smythson gratitude cards combining traditional values with contemporary style.", "Tissue-lined elegance ensures your gratitude arrives in distinguished style.", "Premium materials show recipients their kindness deserves quality recognition.", "British craftsmanship brings elegance to every expression of heartfelt gratitude.", "https://www.smythson.com/uk/stationery/cards/thank-you-cards"],
    ["13813053110", "SMY | UK | Search | Brand Stationery", "153607315570", "UK - semi-brand - stationery - writing folder", "780374687994", "Smythson of Bond Street™", "Luxury leather writing folders", "Over 135 years Of expertise", "Stay effortlessly organised", "Classic black leather folders", "Luxury leather organisers", "Enjoy complimentary returns", "Polished professional finish", "A4 & A5 sizes available", "", "", "", "", "", "", "Smythson creates folders for those who demand excellence in every detail.", "Exclusive folder designs that transform organisation into luxury.", "Luxury British folders featuring finest leathers and expert construction.", "Streamlined style meets practical function in our premium leather folder collection.", "https://www.smythson.com/uk/diaries-books/writing-folders"],
    ["23215754148", "SMY | UK | Search | Competitor | Ai", "191738856607", "UK - Competitor", "784157389885", "Smythson of Bond Street™", "", "Shop luxury leather pieces", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Personalise your order today", "British luxury since 1887", "", "", "", "", "", "", "", "Discover luxury leather bags, notebooks, diaries, personalised stationery and accessories.", "Add initials, text or motifs gold-stamped by our artisans for a uniquely personal touch.", "Make this festive season truly special with Smythson's curated collection of luxury gifts.", "", "https://www.smythson.com/uk/stationery"],
    ["13810745002", "SMY | UK | Search | Semi Brand - Diaries", "185695100380", "UK - brand plus - stationery - diary", "773478848874", "Smythson of Bond Street™", "Luxury leather diaries", "Over 135 years of expertise", "Luxury leather craftsmanship", "Free delivery on orders £300+", "Discover our 2026 Diary", "Enjoy complimentary returns", "Personalise your order today", "Discover gifts for him & her", "Shop the 2026 diary collection", "Exclusive luxury gift wrapping", "Uncover our latest collection", "Smythson Portobello diary", "Handcrafted in England", "", "Start planning next year's adventures with our 2026 diaries.", "Crafted with featherweight paper and leather for effortless planning.", "Discover new arrivals from luxury leather diaries, bags, notebooks, stationery & more.", "Explore gold-stamped initials motifs & more to make your diary uniquely yours.", "https://www.smythson.com/uk/diaries-and-books/diaries/full-year-diaries"],
    ["13810745002", "SMY | UK | Search | Semi Brand - Diaries", "124001824749", "UK - diaries & organisers - diaries - collection - panama", "773478848871", "Smythson of Bond Street™", "Luxury leather diaries", "Over 135 years Of expertise", "Luxury leather craftsmanship", "Free delivery on orders £300+", "Discover our 2026 Diary", "Enjoy complimentary returns", "Personalise your order today", "Discover gifts for him & her", "Shop the 2026 diary collection", "Exclusive luxury gift wrapping", "Uncover our latest collection", "Smythson Panama diary", "Handcrafted in England", "", "Start planning next year's adventures with our 2026 diaries.", "Crafted with featherweight paper and leather for effortless planning.", "Discover new arrivals from luxury leather diaries, bags, notebooks, stationery & more.", "Explore gold-stamped initials motifs & more to make your diary uniquely yours.", "https://www.smythson.com/uk/diaries-and-books/diaries/full-year-diaries"]
]

def parse_row(row):
    """
    Parse spreadsheet row into ad data.

    Column structure:
    0: Campaign ID
    1: Campaign Name
    2: Ad Group ID
    3: Ad Group Name
    4: Ad ID
    5-19: Headlines 1-15 (15 columns)
    20-23: Descriptions 1-4 (4 columns)
    24: Final URL
    """
    if len(row) < 25:
        print(f"⚠️  Row has only {len(row)} columns, expected 25")
        return None

    # Extract headlines (indices 5-19 inclusive, which is 15 headlines)
    headlines = []
    for i in range(5, 20):
        if row[i] and row[i].strip():
            headlines.append(row[i].strip())

    # Extract descriptions (indices 20-23 inclusive, which is 4 descriptions)
    descriptions = []
    for i in range(20, 24):
        if row[i] and row[i].strip():
            descriptions.append(row[i].strip())

    return {
        'campaign_id': row[0],
        'campaign_name': row[1],
        'ad_group_id': row[2],
        'ad_group_name': row[3],
        'ad_id': row[4],
        'headlines': headlines,
        'descriptions': descriptions,
        'final_url': row[24] if len(row) > 24 else ""
    }

def main():
    # Load current state
    current_state_file = Path(__file__).parent.parent / 'data' / 'uk_rsa_current_state.json'

    print(f"Loading current state from {current_state_file}")
    with open(current_state_file, 'r') as f:
        current_state = json.load(f)

    # Create lookup by ad_id
    current_by_id = {ad['ad_id']: ad for ad in current_state}

    print(f"✓ Loaded {len(current_by_id)} current UK RSAs\n")

    # Parse spreadsheet data
    print("Parsing spreadsheet data...")
    spreadsheet_ads = {}
    for i, row in enumerate(UK_SHEET_DATA, 1):
        parsed = parse_row(row)
        if parsed:
            spreadsheet_ads[parsed['ad_id']] = parsed
            print(f"  Row {i}: Ad {parsed['ad_id']} - {len(parsed['headlines'])} headlines, {len(parsed['descriptions'])} descriptions")

    print(f"\n✓ Parsed {len(spreadsheet_ads)} ads from spreadsheet\n")

    # Build updates JSON
    updates = []
    changes_count = 0

    print("Comparing with current state...\n")

    for ad_id, sheet_ad in spreadsheet_ads.items():
        current_ad = current_by_id.get(ad_id)

        if not current_ad:
            print(f"⚠️  Ad {ad_id} in spreadsheet but not in current state - skipping")
            continue

        # Check for changes
        headlines_changed = sheet_ad['headlines'] != current_ad['current_headlines']
        descriptions_changed = sheet_ad['descriptions'] != current_ad['current_descriptions']
        url_changed = sheet_ad['final_url'] != current_ad['final_url']

        if headlines_changed or descriptions_changed or url_changed:
            changes_count += 1
            print(f"{'='*80}")
            print(f"✓ Changes for Ad {ad_id}")
            print(f"  Campaign: {current_ad['campaign_name']}")
            print(f"  Ad Group: {current_ad['ad_group_name']}")

            if headlines_changed:
                print(f"\n  Headlines changed:")
                print(f"    Current: {len(current_ad['current_headlines'])} headlines")
                print(f"    New: {len(sheet_ad['headlines'])} headlines")
                for i, (curr, new) in enumerate(zip(current_ad['current_headlines'], sheet_ad['headlines']), 1):
                    if curr != new:
                        print(f"    H{i}: '{curr[:50]}...' → '{new[:50]}...'")

            if descriptions_changed:
                print(f"\n  Descriptions changed:")
                print(f"    Current: {len(current_ad['current_descriptions'])} descriptions")
                print(f"    New: {len(sheet_ad['descriptions'])} descriptions")
                for i, (curr, new) in enumerate(zip(current_ad['current_descriptions'], sheet_ad['descriptions']), 1):
                    if curr != new:
                        print(f"    D{i}: '{curr[:50]}...' → '{new[:50]}...'")

            if url_changed:
                print(f"\n  URL changed:")
                print(f"    '{current_ad['final_url']}'")
                print(f"    → '{sheet_ad['final_url']}'")

        # Add to updates (all ads, whether changed or not)
        updates.append({
            'campaign_name': current_ad['campaign_name'],
            'ad_group_name': current_ad['ad_group_name'],
            'ad_id': ad_id,
            'status': current_ad['status'],
            'current_headlines': current_ad['current_headlines'],
            'new_headlines': sheet_ad['headlines'],
            'current_descriptions': current_ad['current_descriptions'],
            'new_descriptions': sheet_ad['descriptions'],
            'final_url': sheet_ad['final_url']
        })

    # Save updates JSON
    output_file = Path(__file__).parent.parent / 'data' / 'uk_rsa_updates_from_sheet.json'

    with open(output_file, 'w') as f:
        json.dump(updates, f, indent=2)

    print(f"\n{'='*80}")
    print(f"✓ UK processing complete")
    print(f"  Total ads: {len(updates)}")
    print(f"  Ads with changes: {changes_count}")
    print(f"  Output: {output_file}")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    main()
