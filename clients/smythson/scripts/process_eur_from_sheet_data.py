#!/usr/bin/env python3
"""Process EUR spreadsheet data and create update JSON."""

import json
from pathlib import Path

# EUR spreadsheet data (14 rows fetched from MCP)
EUR_SHEET_DATA = [
    ["23292938044", "SMY | EUR | CH | Search | Brand Ai", "187736454383", "RONot | Brand", "785121413211", "Smythson of Bond Street™", "British heritage since 1887", "Over 135 years of expertise", "Shop luxury leather pieces", "Free delivery on orders €300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Shop luxury stocking fillers", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Luxury personalised gifts", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/int/"],
    ["23292938044", "SMY | EUR | CH | Search | Brand Ai", "187736454463", "RONot | Brand | Sale", "785121413223", "Smythson of Bond Street™", "British heritage since 1887", "Shop luxury leather pieces", "Free delivery on orders £300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Over 135 years of expertise", "Timeless leather craftsmanship", "Personalise your order today", "Luxury gifts for her", "Gifts for the Home", "Luxury personalised gifts", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/int/"],
    ["691020848", "SMY | EUR | DE | Search | Brand Ai", "37376548964", "DE | Brand", "784327102022", "Smythson of Bond Street™", "Kostenlose Rücksendungen", "Personalisierung möglich", "Personalisierte Bestellung", "Geschenke für sie und ihn", "Luxus-Geschenkverpackung", "Zeitlose Kollektionen", "Kostenloser Versand ab 300 €", "1887 gegründet", "Hochwertige Geschenkideen", "Feine Kalender & Planer", "Zeitlose Lederhandwerkskunst", "Die personalisierte Bestellung", "", "", "In Großbritannien gebunden – Unveränderte Buchbindetechniken seit über 135 Jahren.", "Entwerfen Sie Schreibwaren und personalisieren Sie Ihre Bestellung mit Goldprägung.", "Feinste Lederwaren – von Taschen bis Reiseetuis in ikonischem Smythson-Stil", "Von London nach Deutschland: Ikonisches Design, direkt zu Ihnen", "https://www.smythson.com/de/"],
    ["691020848", "SMY | EUR | DE | Search | Brand Ai", "37376548964", "DE | Brand", "784941557977", "Smythson of Bond Street™", "Kostenlose Rücksendungen", "Personalisierung möglich", "Personalisierte Bestellung", "Geschenke für sie und ihn", "Luxus-Geschenkverpackung", "Zeitlose Kollektionen", "Kostenloser Versand ab 300 €", "1887 gegründet", "Hochwertige Geschenkideen", "Feine Kalender & Planer", "Die personalisierte Bestellung", "", "", "", "In Großbritannien gebunden – Unveränderte Buchbindetechniken seit über 135 Jahren.", "Entwerfen Sie Schreibwaren und personalisieren Sie Ihre Bestellung mit Goldprägung.", "Feinste Lederwaren – von Taschen bis Reiseetuis in ikonischem Smythson-Stil", "Von London nach Deutschland: Ikonisches Design, direkt zu Ihnen", "https://www.smythson.com/de/"],
    ["22428317962", "SMY | EUR | DE | Search | Brand Max Conv Value No Target Max Conv with target ROAS", "181478552807", "DE | Brand | Exact", "732880000699", "Smythson of Bond Street™", "Luxuriöse Lederhandwerkskunst", "Kostenlose Rücksendungen", "Personalisierung möglich", "Personalisierte Bestellung", "Geschenke für sie und ihn", "Luxus-Geschenkverpackung", "Zeitlose Kollektionen", "Kostenloser Versand ab 300 €", "1887 gegründet", "Hochwertige Geschenkideen", "Feine Kalender & Planer", "", "", "", "In Großbritannien gebunden – Unveränderte Buchbindetechniken seit über 135 Jahren.", "Entwerfen Sie Schreibwaren und personalisieren Sie Ihre Bestellung mit Goldprägung.", "Feinste Lederwaren – von Taschen bis Reiseetuis in ikonischem Smythson-Stil", "Von London nach Deutschland: Ikonisches Design, direkt zu Ihnen", "https://www.smythson.com/de/"],
    ["22428317962", "SMY | EUR | DE | Search | Brand Max Conv Value No Target Max Conv with target ROAS", "181478553047", "DE | Brand | Phrase", "732880000696", "Smythson of Bond Street™", "Über 135 Jahre Erfahrung", "Luxuriöse Lederhandwerkskunst", "Kostenlose Rücksendungen", "Personalisierung möglich", "Personalisierte Bestellung", "Geschenke für sie und ihn", "Luxus-Geschenkverpackung", "Zeitlose Kollektionen", "Kostenloser Versand ab 300 €", "", "", "", "", "", "In Großbritannien gebunden – Unveränderte Buchbindetechniken seit über 135 Jahren.", "Entwerfen Sie Schreibwaren und personalisieren Sie Ihre Bestellung mit Goldprägung.", "Feinste Lederwaren – von Taschen bis Reiseetuis in ikonischem Smythson-Stil", "Von London nach Deutschland: Ikonisches Design, direkt zu Ihnen", "https://www.smythson.com/de/"],
    ["23237208923", "SMY | EUR | DE | Search | Competitor | Ai", "187803433586", "DE | Brand", "784327102043", "Smythson of Bond Street™", "Kostenlose Rücksendungen", "Personalisierung möglich", "Personalisierte Bestellung", "Geschenke für sie und ihn", "Luxus-Geschenkverpackung", "Zeitlose Kollektionen", "Kostenloser Versand ab 300 €", "1887 gegründet", "Hochwertige Geschenkideen", "Feine Kalender & Planer", "Die personalisierte Bestellung", "Kostenlose Geschenkverpackung", "", "", "In Großbritannien gebunden – Unveränderte Buchbindetechniken seit über 135 Jahren.", "Entwerfen Sie Schreibwaren und personalisieren Sie Ihre Bestellung mit Goldprägung.", "Feinste Lederwaren – von Taschen bis Reiseetuis in ikonischem Smythson-Stil", "Von London nach Deutschland: Ikonisches Design, direkt zu Ihnen", "https://www.smythson.com/fr/"],
    ["691020884", "SMY | EUR | FR | Search | Brand Ai", "37376559524", "FR | Brand | Exact", "784327102025", "Smythson of Bond Street™", "", "", "", "", "", "", "", "Plus de 135 années d'expertise", "Livraison gratuite dès 300 €", "Le savoir-faire du cuir", "Personnalisez votre commande", "", "", "", "", "", "", "", "https://www.smythson.com/fr/"],
    ["1599767262", "SMY | EUR | IT | Search Brand Ai", "60111469123", "IT Brand", "784327102028", "Smythson of Bond Street™", "", "", "", "", "", "", "Personalizza subito l'ordine", "Articoli in pelle pregiata", "Oltre 135 anni di esperienza", "Spendi +300 €: consegna gratis", "Articoli in pelle artigianali", "", "", "", "", "", "", "", "https://www.smythson.com/it/"],
    ["22440993281", "SMY | EUR | ROEuro | Search | Brand Ai", "178040664196", "ROEuro | Brand", "784327102031", "Smythson of Bond Street™", "British heritage since 1887", "Over 135 years of expertise", "Shop luxury leather pieces", "Free delivery on orders €300+", "Complimentary gift wrapping", "Discover gifts for him & her", "Explore luxury Christmas gifts", "Shop luxury stocking fillers", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Luxury personalised gifts", "", "", "Explore Our Collection - Signature Luxury Leather Bags & Accessories.", "Crafting Stories For Over 135 Years, Designed To Celebrate The Joy Of The Handwritten.", "", "From Notebooks to Handbags, Explore Luxury Design That Celebrates Craftsmanship.", "https://www.smythson.com/eur"],
    ["22440993281", "SMY | EUR | ROEuro | Search | Brand Ai", "178040664196", "ROEuro | Brand", "784941557980", "Smythson of Bond Street™", "Quintessential British Luxury", "Over 135 Years Of Expertise", "Luxury Leather Craftsmanship", "Free Delivery On Orders €300+", "Enjoy Complimentary Returns", "Personalisation Available", "Personalise Your Order Today", "Discover Gifts For Him & Her", "Shop The 2026 Diary Collection", "Exclusive Luxury Gift Wrapping", "Uncover Our Latest Collection", "Discover Timeless Collections", "Crafted for Modern Life", "", "Explore Our Collection - Signature Luxury Leather Bags & Accessories.", "Crafting Stories For Over 135 Years, Designed To Celebrate The Joy Of The Handwritten.", "Smythson's New Autumn Winter Arrivals - Discover Now.", "From Notebooks to Handbags, Explore Luxury Design That Celebrates Craftsmanship.", "https://www.smythson.com/eur"],
    ["1603775949", "SMY | EUR | ROEuro | Search | Brand Diaries and Organisers", "143673725201", "ROE - EN - semi-brand - diaries and organisers - agendas", "773539871911", "Smythson of Bond Street™", "Smythson 2026 diary", "Over 135 years of expertise", "Luxury leather craftsmanship", "Free delivery on orders €300+", "Enjoy complimentary returns", "Smythson panama diary", "Personalise your order today", "Discover gifts for him & her", "Shop the 2026 diary collection", "Exclusive luxury gift wrapping", "Smythson agendas", "Smythson portobello diary", "Smythson chelsea diary", "", "Start planning next year's adventures with our 2026 diaries.", "Crafted with featherweight paper and leather for effortless planning.", "Shop luxury leather diaries, bags, notebooks, stationery & more.", "Explore gold-stamped initials motifs & more to make your diary uniquely yours.", "https://www.Smythson.com/eur/diaries-and-books/diaries/all-diaries"],
    ["22441297139", "SMY | EUR | RONot | Search | Brand Ai", "176696220703", "RONot | Brand", "784327102034", "Smythson of Bond Street™", "Luxury gifts for him", "Luxury gifts for her", "Gifts for the Home", "Luxury personalised gifts", "", "Personalise your order today", "Shop luxury leather pieces", "Over 135 years of expertise", "Free delivery on orders £300+", "Timeless leather craftsmanship", "", "", "", "", "Make the ordinary extraordinary and the everyday timeless with Smythson", "A distinctly unique, extraordinary brand catering to extraordinary people since 1887", "Discover the perfect gift this Christmas. Thoughtfully made, meaningfully given", "This Christmas, celebrate the art of thoughtful gifting with Smythson", "https://www.smythson.com/int/"],
    ["23048760213", "SMY | EUR | RONot | Search | Brand Diaries and Organisers", "187396806873", "ROE - EN - semi-brand - diaries and organisers - agendas", "775856922188", "Smythson of Bond Street™", "Luxury leather diaries", "Over 135 years of expertise", "Luxury leather craftsmanship", "Free delivery on orders €300+", "Enjoy complimentary returns", "Personalisation available", "Personalise your order today", "Discover gifts for him & her", "Shop the 2026 diary collection", "Exclusive luxury gift wrapping", "Uncover our latest collection", "Smythson portobello diary", "Crafted in england", "", "Start planning next year's adventures with our 2026 diaries.", "Crafted with featherweight paper and leather for effortless planning.", "Shop luxury leather diaries, bags, notebooks, stationery & more.", "Explore gold-stamped initials motifs & more to make your diary uniquely yours.", "https://www.Smythson.com/int/diaries-and-books/diaries/all-diaries"],
]

def parse_row(row):
    """Parse spreadsheet row - columns 5-19 headlines, 20-23 descriptions, 24 final URL"""
    if len(row) < 25:
        return None
    headlines = [row[i].strip() for i in range(5, 20) if row[i] and row[i].strip()]
    descriptions = [row[i].strip() for i in range(20, 24) if row[i] and row[i].strip()]
    return {
        'campaign_id': row[0], 'campaign_name': row[1], 'ad_group_id': row[2],
        'ad_group_name': row[3], 'ad_id': row[4], 'headlines': headlines,
        'descriptions': descriptions, 'final_url': row[24] if len(row) > 24 else ""
    }

# Load current state
current_state_file = Path(__file__).parent.parent / 'data' / 'eur_rsa_current_state.json'
with open(current_state_file, 'r') as f:
    current_state = json.load(f)
current_by_id = {ad['ad_id']: ad for ad in current_state}

print(f"✓ Loaded {len(current_by_id)} current EUR RSAs\n")

# Parse spreadsheet
spreadsheet_ads = {}
for i, row in enumerate(EUR_SHEET_DATA, 1):
    parsed = parse_row(row)
    if parsed:
        spreadsheet_ads[parsed['ad_id']] = parsed
        print(f"  Row {i}: Ad {parsed['ad_id']} - {len(parsed['headlines'])} headlines, {len(parsed['descriptions'])} descriptions")

print(f"\n✓ Parsed {len(spreadsheet_ads)} ads from spreadsheet\n")

# Compare and build updates
updates = []
changes_count = 0

for ad_id, sheet_ad in spreadsheet_ads.items():
    current_ad = current_by_id.get(ad_id)
    if not current_ad:
        print(f"⚠️  Ad {ad_id} in spreadsheet but not in current state - skipping")
        continue
    
    headlines_changed = sheet_ad['headlines'] != current_ad['current_headlines']
    descriptions_changed = sheet_ad['descriptions'] != current_ad['current_descriptions']
    url_changed = sheet_ad['final_url'] != current_ad['final_url']
    
    if headlines_changed or descriptions_changed or url_changed:
        changes_count += 1
        print(f"✓ Changes for Ad {ad_id}: {current_ad['campaign_name']}")
    
    updates.append({
        'campaign_name': current_ad['campaign_name'], 'ad_group_name': current_ad['ad_group_name'],
        'ad_id': ad_id, 'status': current_ad['status'],
        'current_headlines': current_ad['current_headlines'], 'new_headlines': sheet_ad['headlines'],
        'current_descriptions': current_ad['current_descriptions'], 'new_descriptions': sheet_ad['descriptions'],
        'final_url': sheet_ad['final_url']
    })

# Save
output_file = Path(__file__).parent.parent / 'data' / 'eur_rsa_updates_from_sheet.json'
with open(output_file, 'w') as f:
    json.dump(updates, f, indent=2)

print(f"\n{'='*80}")
print(f"✓ EUR processing complete: {len(updates)} ads, {changes_count} with changes")
print(f"  Output: {output_file}")
print(f"{'='*80}")
