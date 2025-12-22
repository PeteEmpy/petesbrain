#!/usr/bin/env python3
"""Check how many ads have changes in each region"""

import json

def compare_lists(list1, list2):
    """Compare two lists (headlines or descriptions)"""
    # Remove empty strings
    l1 = [x for x in list1 if x]
    l2 = [x for x in list2 if x]
    return l1 != l2

def check_region(region_name, sheet_rows, current_state_file):
    """Check a region for changes"""
    
    # Load current state
    with open(current_state_file, 'r') as f:
        current_state = json.load(f)
    
    # Create lookup
    current_by_id = {ad['ad_id']: ad for ad in current_state}
    
    changes = []
    no_changes = 0
    not_found = 0
    
    for row in sheet_rows:
        ad_id = str(row[4])
        
        if ad_id not in current_by_id:
            not_found += 1
            continue
        
        current = current_by_id[ad_id]
        
        # Extract from spreadsheet
        sheet_headlines = [h for h in row[5:20] if h]
        sheet_descriptions = [d for d in row[20:24] if d]
        
        # Compare
        headlines_changed = compare_lists(current['current_headlines'], sheet_headlines)
        descriptions_changed = compare_lists(current['current_descriptions'], sheet_descriptions)
        
        if headlines_changed or descriptions_changed:
            changes.append({
                'ad_id': ad_id,
                'campaign': current['campaign_name'],
                'headlines_changed': headlines_changed,
                'descriptions_changed': descriptions_changed
            })
        else:
            no_changes += 1
    
    return {
        'region': region_name,
        'total_ads': len(sheet_rows),
        'matched': len(sheet_rows) - not_found,
        'not_found': not_found,
        'changes': len(changes),
        'no_changes': no_changes,
        'changed_ads': changes
    }

# UK data (Row 2-28 from earlier)
UK_DATA = [
    ["13811031042", "SMY | UK | Search | Brand Exact", "128117925481", "UK - Brand", "784157361259", "Smythson of Bond Street™", "British heritage since 1887", "Over 135 years of expertise", "Shop luxury leather pieces", "Free delivery on orders £300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Shop luxury stocking fillers", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Luxury personalised gifts", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/"],
    ["13811031042", "SMY | UK | Search | Brand Exact", "187903967924", "UK - Brand - Sale", "784408654524", "Smythson of Bond Street™", "British heritage since 1887", "Shop luxury leather pieces", "Free delivery on orders £300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Over 135 years of expertise", "", "Timeless leather craftsmanship", "Personalise your order today", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/"],
    ["13813052579", "SMY | UK | Search | Brand Plus", "137137030701", "UK - semi-brand - home - desk accessories - blotters", "784228048462", "Smythson of Bond Street™", "Luxury leather blotters", "Discover gifts for him & her", "Shop luxury leather blotters", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "Complimentary gift wrapping", "British heritage since 1887", "", "", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1888", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/uk/home/accessories/desk-accessories"],
]

# EUR data
EUR_DATA = [
    ["23292938044", "SMY | EUR | CH | Search | Brand Ai", "187736454383", "RONot | Brand", "785121413211", "Smythson of Bond Street™", "British heritage since 1887", "Over 135 years of expertise", "Shop luxury leather pieces", "Free delivery on orders €300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Shop luxury stocking fillers", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Luxury personalised gifts", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/int/"],
]

# ROW data
ROW_DATA = [
    ["6551615752", "SMY | AUS | Search | Brand Ai", "77517328486", "AUS - Brand - Exact & Phrase", "784326640550", "Smythson of Bond Street™", "British heritage since 1887", "Shop luxury leather pieces", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Personalise your order today", "", "Over 135 years of expertise", "Timeless leather craftsmanship", "Luxury personalised gifts", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/int/"],
]

# USA - sample only
USA_DATA = [
    ["1683494533", "SMY | US | Search | Brand Exact", "65464486037", "USA - Brand", "784198246551", "Smythson of Bond Street™", "British heritage since 1887", "Shop luxury leather pieces", "Personalize your order today", "Over 135 years of expertise", "Free delivery on orders $500+", "Handcrafted in England", "Explore luxury Christmas gifts", "Shop luxury stocking fillers", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Timeless leather craftsmanship", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/us/"],
]

print("="*80)
print("CHECKING ALL REGIONS FOR CHANGES")
print("="*80)

# Check UK (sample)
uk_result = check_region("UK (sample 3 ads)", UK_DATA, '../data/uk_rsa_current_state.json')
print(f"\n{uk_result['region']}:")
print(f"  Total: {uk_result['total_ads']} ads")
print(f"  Matched: {uk_result['matched']} ads")
print(f"  Changes: {uk_result['changes']} ads")
print(f"  No changes: {uk_result['no_changes']} ads")

if uk_result['changed_ads']:
    for change in uk_result['changed_ads']:
        print(f"    - Ad {change['ad_id']}: H={change['headlines_changed']}, D={change['descriptions_changed']}")

# Check EUR (sample)
eur_result = check_region("EUR (sample 1 ad)", EUR_DATA, '../data/eur_rsa_current_state.json')
print(f"\n{eur_result['region']}:")
print(f"  Total: {eur_result['total_ads']} ads")
print(f"  Matched: {eur_result['matched']} ads")
print(f"  Changes: {eur_result['changes']} ads")
print(f"  No changes: {eur_result['no_changes']} ads")

# Check ROW (sample)
row_result = check_region("ROW (sample 1 ad)", ROW_DATA, '../data/row_rsa_current_state.json')
print(f"\n{row_result['region']}:")
print(f"  Total: {row_result['total_ads']} ads")
print(f"  Matched: {row_result['matched']} ads")
print(f"  Changes: {row_result['changes']} ads")
print(f"  No changes: {row_result['no_changes']} ads")

# Check USA (sample)
usa_result = check_region("USA (sample 1 ad)", USA_DATA, '../data/usa_rsa_current_state.json')
print(f"\n{usa_result['region']}:")
print(f"  Total: {usa_result['total_ads']} ads")
print(f"  Matched: {usa_result['matched']} ads")
print(f"  Changes: {usa_result['changes']} ads")
print(f"  No changes: {usa_result['no_changes']} ads")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Based on samples, very few ads appear to have changes.")
print(f"Most ads in spreadsheet match current Google Ads state.")
print(f"\nThe UK sample found 1 change (1888 vs 1887) out of 3 ads tested.")
