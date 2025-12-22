#!/usr/bin/env python3
"""Build UK RSA updates from complete spreadsheet data"""

import json

# Complete UK spreadsheet data (all 27 ads)
# Parsed from MCP output earlier: Row format is [Campaign ID, Campaign Name, Ad Group ID, Ad Group Name, Ad ID, H1-H15 (indices 5-19), D1-D4 (indices 20-23), Final URL (index 24)]

UK_SHEET_DATA = """784157361259|Smythson of Bond Street™|British heritage since 1887|Over 135 years of expertise|Shop luxury leather pieces|Free delivery on orders £300+|Complimentary gift wrapping|Discover gifts for him & her|Explore luxury Christmas gifts|Shop luxury stocking fillers|Luxury gifts for him|Luxury gifts for her|Gifts for the Home|Luxury personalised gifts|||Make the ordinary extraordinary and the everyday timeless with Smythson|A distinctly unique, extraordinary brand catering to extraordinary people since 1887|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/
784408654524|Smythson of Bond Street™|British heritage since 1887|Shop luxury leather pieces|Free delivery on orders £300+|Complimentary gift wrapping|Discover gifts for him & her|Explore luxury Christmas gifts|Over 135 years of expertise||Timeless leather craftsmanship|Personalise your order today||||Make the ordinary extraordinary and the everyday timeless with Smythson|A distinctly unique, extraordinary brand catering to extraordinary people since 1887|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/
784228048462|Smythson of Bond Street™|Luxury leather blotters|Discover gifts for him & her|Shop luxury leather blotters|Over 135 years of expertise|Free delivery on orders £300+|Timeless leather craftsmanship|Complimentary gift wrapping|British heritage since 1887||||||Make the ordinary extraordinary and the everyday timeless with Smythson|A distinctly unique, extraordinary brand catering to extraordinary people since 1888|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/home/accessories/desk-accessories
784228048447|Smythson of Bond Street™|Luxury games & playing cards|Discover gifts for him & her|Shop games & playing cards|Over 135 years of expertise|Free delivery on orders £300+|Timeless leather craftsmanship|Complimentary gift wrapping|British heritage since 1887|Shop luxury game sets|Handcrafted card & table games|Shop exquisite luxury games|||Discover classic artisan poker and backgammon sets, each crafted with exceptional detail|Ensure every event is memorable with our luxurious entertainment collection|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/home/accessories/games
784228048453|Smythson of Bond Street™|Luxury gifts|Discover gifts for him & her|Shop luxury gifts|Over 135 years of expertise|Free delivery on orders £300+|Timeless leather craftsmanship|Complimentary gift wrapping|British heritage since 1887|Shop luxury leather gifts|Luxury gifts for her|Luxury gifts for him|Explore luxury Christmas gifts||Make the ordinary extraordinary and the everyday timeless with Smythson|Make this festive season truly special with Smythson's curated collection of luxury gifts.|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/gifts/christmas-gifts
784228048465|Smythson of Bond Street™|Luxury leather jewellery boxes|Discover gifts for him & her|Shop luxury jewellery boxes|Over 135 years of expertise|Free delivery on orders £300+|Timeless leather craftsmanship|Complimentary gift wrapping|British heritage since 1887|Shop leather jewellery boxes|||||Keep your treasures & keepsakes beautifully organized with our leather jewellery boxes|Make this festive season truly special with Smythson's curated collection of luxury gifts.|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/home/accessories/jewellery-boxes-rolls
784228048444|Smythson of Bond Street™|Luxury leather trinket cases|Discover gifts for him & her|Shop luxury trinket cases|Over 135 years of expertise|Free delivery on orders £300+|Timeless leather craftsmanship|Complimentary gift wrapping|British heritage since 1887|Shop leather trinket cases|||||Keep your dressing table or desk in order with our luxury trinket trays and cases.|Make this festive season truly special with Smythson's curated collection of luxury gifts.|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/home/accessories/trinket-trays
784228048456|Smythson of Bond Street™|Luxury leather trinket trays|Discover gifts for him & her|Shop luxury trinket trays|Over 135 years of expertise|Free delivery on orders £300+|Timeless leather craftsmanship|Complimentary gift wrapping|British heritage since 1887|Shop leather trinket trays|||||Keep your dressing table or desk in order with our luxury trinket trays and cases.|Make this festive season truly special with Smythson's curated collection of luxury gifts.|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/home/accessories/trinket-trays
784228048459|Smythson of Bond Street™|Luxury leather photo albums|Discover gifts for him & her|Shop luxury photo albums|Over 135 years of expertise|Free delivery on orders £300+|Timeless leather craftsmanship|Complimentary gift wrapping|British heritage since 1887|||||||Make this festive season truly special with Smythson's curated collection of luxury gifts.|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/home/accessories/frames-albums
784228048468|Smythson of Bond Street™|Luxury leather photo frames|Discover gifts for him & her|Shop luxury photo frames|Over 135 years of expertise|Free delivery on orders £300+|Timeless leather craftsmanship|Complimentary gift wrapping|British heritage since 1887|||||||Make this festive season truly special with Smythson's curated collection of luxury gifts.|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/home/accessories/frames-albums
784228048450|Smythson of Bond Street™|Leather watch boxes|Discover gifts for him & her|Shop leather watch boxes|Over 135 years of expertise|Free delivery on orders £300+|Timeless leather craftsmanship|Complimentary gift wrapping|British heritage since 1887|||||||Make this festive season truly special with Smythson's curated collection of luxury gifts.|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/home/accessories/watch-cufflink-boxes
784197388692|Smythson of Bond Street™|Luxury leather notebooks|Shop Smythson notebooks|Shop leather notebooks|Over 135 years of expertise|Free delivery on orders £300+|Timeless leather craftsmanship|Complimentary gift wrapping|British heritage since 1887|Handcrafted leather notebooks|Timeless leather pieces|fom|||Each of our notebooks is hand-bound and packed full of our signature Featherweight paper.|Make this festive season truly special with Smythson's curated collection of luxury gifts.|Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given|This Christmas, celebrate the art of thoughtful gifting with Smythson|https://www.smythson.com/uk/diaries-and-books/notebooks/all-notebooks
780966363483|Smythson of Bond Street™|Luxury birthday cards|Over 135 years of expertise|Luxury paper craftsmanship|Free delivery on orders £300+|Discover new arrivals|Enjoy complimentary returns|Personalise your order today|Discover gifts for him & her|Exclusive luxury gift wrapping|Uncover our latest collection|Discover timeless collections|Crafted for modern life||Discover our selection of hand-engraved birthday cards.|Design your own suite of stationery & personalise your order with our gold stamp service.|Discover new arrivals from luxury leather stationery, accessories, bags, notebooks & more.|Explore our bespoke stationery services for a suite that's uniquely yours.|https://www.smythson.com/uk/stationery/cards/birthday-cards
780374687964|Luxury notelets by Smythson|Notelets with tissue envelopes|Heritage notelets since 1887|Notelets for every occasion|Notelets for refined tastes|Discover Smythson notelets|Luxury notelet collection|Smythson signature notelets|Shop notelets collection today|Luxury paper notelets|||||Browse Smythson's distinguished range of notelets for every correspondence occasion.|Shop notelets that arrive beautifully packaged in Smythson's signature presentation.|Premium British notelets featuring hand-engraved designs and tissue-lined envelopes.|Luxury notelets that make every thank you, acceptance, or greeting truly memorable.|https://www.smythson.com/uk/stationery/cards
780374687982|Smythson of Bond Street™|Luxury personalised stationery|Exquisite engraving available|Order custom stationery today|Luxury custom stationery|135 years of personal service|British bespoke stationery|Add your personal touch today|Choose your perfect design|Choose border & layout styles|Designed by you crafted by us|Shop exquisite stationery|Create your perfect letterhead||Smythson personalisation service brings bespoke luxury to your correspondence.|Create bespoke stationery that perfectly represents your individual style.|Distinguished personalisation options for business cards and correspondence alike.|Exclusive personalisation service for those who appreciate bespoke quality.|https://www.smythson.com/uk/stationery
780374687985|Smythson of Bond Street™|Distinguished card range|Smythson writing cards|Luxury correspondence cards|Make letters beautiful|Luxury correspondence sets|Find perfect writing cards|Correspondence excellence|Over 135 years of letter craft||||||Make every letter beautiful with handcrafted correspondence cards from Smythson.|The ultimate in British luxury correspondence cards for discerning letter writers.|Over 135 years of expertise evident in every handcrafted correspondence card we produce.|Hand-lined envelopes complement each card for a complete luxury writing experience.|https://www.smythson.com/uk/stationery/cards/correspondence-cards
780374687991|Smythson invitation cards|Luxury invitation cards|Hand-engraved invitations|Make events truly special|Matching envelope invites|Exquisite invitation sets|Distinguished invites range|Shop invitation cards today|Shop exquisite stationery||||||Smythson invitations combine traditional craftsmanship with contemporary elegance.|Find the ideal invitation cards from Britain's premier stationery house since 1887.|Smythson creates invitations for hosts who value exceptional quality.|Transform event planning with invitations that guests will admire and remember.|https://www.smythson.com/uk/stationery/cards/invitations
780374687979|Smythson leather pencil cases|Luxury leather pencil cases|Expertly crafted pencil cases|Cases worth the investment|Quality leather pen cases|Luxury panama leather cases|Over 135 years of expertise|Explore leather case designs|Browse luxury case collection|British heritage leather cases|Personalisation available|Heritage pencil case craft|||Smythson creates pencil cases for those who value quality and organisation.|Luxury British pencil cases featuring the finest Panama leather and expert construction.|Discover pencil cases worthy of your finest pens and creative tools.|Expertly crafted from durable Panama leather for stationery storage that lasts a lifetime.|https://www.smythson.com/uk/leather-goods/accessories/pencil-cases
780374687976|Smythson pen craftsmanship|Smythson writing excellence|Over 135 years of expertise|Luxury pens & pencils range|Fountain pens from Smythson|Luxury British pens & pencils|Luxury writing essentials|Find your writing style today|Pens to inspire every word|Luxury writing companions|Complete writing solutions|Smythson signature pencils|Fountain & rollerball pens||From fountain & rollerball pens to our signature gold gilded pencils, shop now.|Smythson creates writing instruments for those who value excellence.|Discover new arrivals from luxury leather stationery, accessories, bags, notebooks & more.|Explore our bespoke stationery services for a suite that's uniquely yours.|https://www.smythson.com/uk/stationery/pens-pencils
780374687967|Smythson quality envelopes|Smythson envelope excellence|Watermarked white laid style|Distinguished envelope range|Exquisite envelope quality|King & A4 envelope sizes|Handcrafted British envelopes|British crafted excellence|Shop exquisite stationery||||||Smythson London creates envelopes for those who value quality in every detail.|Lovingly handcrafted envelopes that transform ordinary letters into special deliveries.|British made envelopes combining traditional craftsmanship with contemporary elegance.||https://www.smythson.com/uk/stationery/plain-stationery/envelopes
780374687973|Smythson luxury writing paper|Discover writing excellence|Luxury writing paper|Plain stationery excellence|Classic plain stationery range|Writing paper & envelope sets|Signature handcrafted luxury|Smythson plain paper range|Luxury plain writing paper|Handcrafted writing excellence|||||Smythson creates plain stationery for those who value quality correspondence.|Find writing materials that inspire you to put pen to paper more often than ever before.|Transform ordinary messages into extraordinary correspondence with luxury plain paper.|Smythson plain stationery where simplicity meets luxury in perfect harmony.|https://www.smythson.com/uk/stationery/plain-stationery
780374687970|Smythson of Bond Street™|Smythson writing excellence|Luxury stationery selection|Distinguished stationery range|Express elegance in writing|Find your writing style|Browse full collections online|Exclusive British stationery|137 years stationery expertise|Heritage writing collections|Refined writing accessories||||Smythson stationery bringing timeless sophistication to modern communication.|Distinguished collections encompassing every aspect of luxury writing.|137 years creating stationery that elevates the art of handwritten communication.|Browse our full range of writing accessories and fine stationery options online.|https://www.smythson.com/uk/stationery
780374687988|Smythson of Bond Street™|Luxury thank you cards|Cards for heartfelt thanks|Luxury paper craftsmanship|Express recognition in style|Gratitude cards & notelets|Thank you cards worth keeping|Sophisticated thank you notes|Find your thank you style||||||Smythson gratitude cards combining traditional values with contemporary style.|Tissue-lined elegance ensures your gratitude arrives in distinguished style.|Premium materials show recipients their kindness deserves quality recognition.|British craftsmanship brings elegance to every expression of heartfelt gratitude.|https://www.smythson.com/uk/stationery/cards/thank-you-cards
780374687994|Smythson of Bond Street™|Luxury leather writing folders|Over 135 years Of expertise|Stay effortlessly organised|Classic black leather folders|Luxury leather organisers|Enjoy complimentary returns|Polished professional finish|A4 & A5 sizes available||||||Smythson creates folders for those who demand excellence in every detail.|Exclusive folder designs that transform organisation into luxury.|Luxury British folders featuring finest leathers and expert construction.|Streamlined style meets practical function in our premium leather folder collection.|https://www.smythson.com/uk/diaries-books/writing-folders
784157389885|Smythson of Bond Street™||Shop luxury leather pieces|Over 135 years of expertise|Free delivery on orders £300+|Timeless leather craftsmanship|Personalise your order today|British luxury since 1887|||||||Discover luxury leather bags, notebooks, diaries, personalised stationery and accessories.|Add initials, text or motifs gold-stamped by our artisans for a uniquely personal touch.|Make this festive season truly special with Smythson's curated collection of luxury gifts.||https://www.smythson.com/uk/stationery
773478848874|Smythson of Bond Street™|Luxury leather diaries|Over 135 years of expertise|Luxury leather craftsmanship|Free delivery on orders £300+|Discover our 2026 Diary|Enjoy complimentary returns|Personalise your order today|Discover gifts for him & her|Shop the 2026 diary collection|Exclusive luxury gift wrapping|Uncover our latest collection|Smythson Portobello diary|Handcrafted in England||Start planning next year's adventures with our 2026 diaries.|Crafted with featherweight paper and leather for effortless planning.|Discover new arrivals from luxury leather diaries, bags, notebooks, stationery & more.|Explore gold-stamped initials motifs & more to make your diary uniquely yours.|https://www.smythson.com/uk/diaries-and-books/diaries/full-year-diaries
773478848871|Smythson of Bond Street™|Luxury leather diaries|Over 135 years Of expertise|Luxury leather craftsmanship|Free delivery on orders £300+|Discover our 2026 Diary|Enjoy complimentary returns|Personalise your order today|Discover gifts for him & her|Shop the 2026 diary collection|Exclusive luxury gift wrapping|Uncover our latest collection|Smythson Panama diary|Handcrafted in England||Start planning next year's adventures with our 2026 diaries.|Crafted with featherweight paper and leather for effortless planning.|Discover new arrivals from luxury leather diaries, bags, notebooks, stationery & more.|Explore gold-stamped initials motifs & more to make your diary uniquely yours.|https://www.smythson.com/uk/diaries-and-books/diaries/full-year-diaries"""

# Load current state
with open('../data/uk_rsa_current_state.json', 'r') as f:
    current_state = json.load(f)

print(f"✓ Loaded {len(current_state)} UK RSAs from API")

# Create lookup
current_by_id = {ad['ad_id']: ad for ad in current_state}

# Parse spreadsheet
lines = UK_SHEET_DATA.strip().split('\n')
print(f"✓ Loaded {len(lines)} rows from spreadsheet")

updates = []
changes_count = 0

for line in lines:
    parts = line.split('|')
    
    ad_id = parts[0]
    
    if ad_id not in current_by_id:
        print(f"⚠️  Ad ID {ad_id} not in current state")
        continue
    
    current = current_by_id[ad_id]
    
    # Extract headlines (indices 1-15)
    new_headlines = [h for h in parts[1:16] if h.strip()]
    
    # Extract descriptions (indices 16-19)
    new_descriptions = [d for d in parts[16:20] if d.strip()]
    
    final_url = parts[20] if len(parts) > 20 else current['final_url']
    
    # Check for changes
    has_changes = (
        current['current_headlines'] != new_headlines or
        current['current_descriptions'] != new_descriptions
    )
    
    if has_changes:
        changes_count += 1
        print(f"  ✓ Ad {ad_id}: Changes detected")
    
    updates.append({
        'campaign_name': current['campaign_name'],
        'ad_group_name': current['ad_group_name'],
        'ad_id': ad_id,
        'status': current['status'],
        'current_headlines': current['current_headlines'],
        'new_headlines': new_headlines,
        'current_descriptions': current['current_descriptions'],
        'new_descriptions': new_descriptions,
        'final_url': final_url
    })

print(f"\n✓ Built {len(updates)} update entries")
print(f"✓ {changes_count} ads have changes from spreadsheet")

# Save
output_file = '../data/uk_rsa_updates_from_sheet.json'
with open(output_file, 'w') as f:
    json.dump(updates, f, indent=2)

print(f"✓ Saved to: {output_file}")
