#!/usr/bin/env python3
"""
Calculate total daily budgets for ENABLED campaigns only
Properly handles shared budget pools
"""

# UK Account - ENABLED campaigns only
uk_enabled_budgets = {
    # Campaign ID: (Budget Pool ID, Amount Micros, Campaign Name)
    "23194794411": ("15090318700", 50000000, "SMY | UK | P Max | Diaries"),
    "22845468179": ("14805985381", 75000000, "SMY | UK | P Max | H&S"),
    "23021472678": ("14944953037", 100000000, "SMY | UK | P Max | H&S - Men's Briefcases"),
    "23233714033": ("15115980463", 75000000, "SMY | UK | P Max | H&S Christmas Gifting"),
    "13811031042": ("9072507297", 37000000, "SMY | UK | Search | Brand Exact"),
    "13813052579": ("13327874126", 50000000, "SMY | UK | Search | Brand Plus"),
    "13813053110": ("13341406045", 30000000, "SMY | UK | Search | Brand Stationery"),
    "23215754148": ("15098417162", 20000000, "SMY | UK | Search | Competitor | Ai"),
    "23074901902": ("14967677681", 18000000, "SMY | UK | Search | Generic | Ai"),
    "13810745002": ("12929756283", 150000000, "SMY | UK | Search | Semi Brand - Diaries"),
    # Brand test campaigns sharing same budget pool (9072507297 - £37)
    "19227602347": ("9072507297", 37000000, "UK - brand - core - test"),
    "20985724980": ("9072507297", 37000000, "UK - brand - core £0.30"),
    "22217168349": ("9072507297", 37000000, "UK_Brand_Core Landing Page Test"),
    "21473381978": ("9072507297", 37000000, "UK_Brand_Core Max Conv Value"),
    # Brand misspellings sharing budget pool (9068132870 - £26)
    "19221243489": ("9068132870", 26000000, "UK - brand - misspellings - test"),
    "21718634044": ("9068132870", 26000000, "UK_Brand_Misspellings Max Clicks Test"),
    # Brand plus sharing budget pool (9216581240 - £150)
    "19221139809": ("9216581240", 150000000, "UK - brand - plus - test"),
}

# USA Account - ENABLED campaigns only
usa_enabled_budgets = {
    "22796857828": ("14764145494", 150000000, "SMY | US | P Max | Bags"),
    "23210838865": ("15095915233", 75000000, "SMY | US | P Max | Diaries"),
    "18037696979": ("11405146786", 35000000, "SMY | US | P Max | H&S"),
    "23232558954": ("15118117815", 40000000, "SMY | US | P Max | H&S Christmas Gifting"),
    "22546298306": ("14551157402", 100000000, "SMY | US | PMax | Zombies"),
    "1683494533": ("11422372952", 30000000, "SMY | US | Search | Brand Exact"),
    "1602584781": ("12929893890", 30000000, "SMY | US | Search | Brand Plus"),
    "23012390791": ("14919994754", 50000000, "SMY | US | Search | Brand Plus Diaries"),
    "1602585081": ("13390322534", 20000000, "SMY | US | Search | Brand | Leather Accessories"),
    "1602584829": ("13343381269", 20000000, "SMY | US | Search | Brand | Stationery"),
    "11189913808": ("1659506859", 54000000, "Target CPA Experiment - USA - brand - misspellings"),
    # Brand test campaigns sharing budget pool (11422372952 - £30)
    "19228636229": ("11422372952", 30000000, "USA - brand test to reduce cpc"),
    "21001958524": ("11422372952", 30000000, "USA - brand test to reduce cpc £0.50"),
    "22216866387": ("11422372952", 30000000, "USA_Brand_Core Landing Page Test"),
    "21466775013": ("11422372952", 30000000, "USA_Brand_Core Max Conversion Value Test"),
    # Brand core EX
    "1734759773": ("1736951227", 78000000, "USA - brand - core [EX]"),
    # Brand locations sharing budget pool (11971109509 - £300)
    "19222158192": ("11971109509", 300000000, "USA - brand - locations"),
    # Brand misspellings sharing budget pool (11425294476 - £30)
    "19228455571": ("11425294476", 30000000, "USA - brand - misspellings"),
}

# EUR Account - ENABLED campaigns only
eur_enabled_budgets = {
    "23257901431": ("15135803680", 30000000, "SMY | EUR | IT | P Max | Diaries"),
    "23253394509": ("15139347337", 15000000, "SMY | EUR | P Max | Christmas Gifting"),
    "23292938044": ("15153614639", 10000000, "SMY | EUR | CH | Search | Brand Ai"),
    "23257639561": ("15125439263", 9690000, "SMY | EUR | DE | P Max | Christmas Gifting"),
    "23257761115": ("15135699727", 25000000, "SMY | EUR | DE | P Max | Diaries"),
    "691020848": ("1705235887", 50000000, "SMY | EUR | DE | Search | Brand Ai"),
    "22428317962": ("1705235887", 50000000, "SMY | EUR | DE | Search | Brand Max Conv Value"),
    "23237208923": ("15117709656", 6660000, "SMY | EUR | DE | Search | Competitor | Ai"),
    "21512797638": ("13788379561", 20000000, "SMY | EUR | DE | Shopping"),
    "23248988334": ("15136066780", 39980000, "SMY | EUR | FR | P Max | Christmas Gifting"),
    "691020884": ("1705540965", 20000000, "SMY | EUR | FR | Search | Brand Ai"),
    "23253230592": ("15134578062", 12110000, "SMY | EUR | IT | P Max | Christmas Gifting"),
    "1599767262": ("1656440764", 100000000, "SMY | EUR | IT | Search Brand Ai"),
    "23253890345": ("15125793782", 20000000, "SMY | EUR | P Max | Diaries"),
    "22440993281": ("14490335959", 50000000, "SMY | EUR | ROEuro | Search | Brand Ai"),
    "1603775949": ("12925013210", 12110000, "SMY | EUR | ROEuro | Search | Brand Diaries"),
    "22441297139": ("14483837445", 20000000, "SMY | EUR | RONot | Search | Brand Ai"),
    "10368145356": ("1660106876", 50000000, "Target CPA Experiment - ROE - brand"),
}

# ROW Account - ENABLED campaigns only
row_enabled_budgets = {
    "19227841675": ("11370644814", 5000000, "AUS - brand test to reduce cpc"),
    "19227775840": ("11370644370", 3750000, "ROW - CA - brand test"),
    "19229009186": ("11365331684", 3750000, "ROW - HK - brand test"),
    "19221315960": ("11370644109", 3750000, "ROW - MEX - brand test"),
    "19229034938": ("11376421816", 3750000, "ROW - SG - brand test"),
    "19175921934": ("11376425032", 10000000, "ROW - brand test to reduce cpc"),
    "6551615752": ("11370644814", 5000000, "SMY | ROW | AUS | Search | Brand Ai"),
    "23258454848": ("15134692206", 10000000, "SMY | ROW | P Max | Christmas Gifting"),
    "23253385815": ("15134691735", 10000000, "SMY | ROW | P Max | Diaries"),
    "22503794801": ("14528371083", 60000000, "SMY | ROW | Search | Brand Ai"),
    "6552020619": ("12929903025", 10000000, "SMY | ROW | Search | Brand Diaries"),
    "23241919876": ("15122745964", 2220000, "SMY | ROW | Search | Competitor | Ai"),
}

def calculate_unique_budgets(enabled_campaigns):
    """Calculate total budget from campaigns, handling shared budget pools"""
    unique_budgets = {}
    for campaign_id, (budget_id, amount_micros, name) in enabled_campaigns.items():
        if budget_id not in unique_budgets:
            unique_budgets[budget_id] = amount_micros
    return unique_budgets

# Calculate unique budget pools
uk_unique = calculate_unique_budgets(uk_enabled_budgets)
usa_unique = calculate_unique_budgets(usa_enabled_budgets)
eur_unique = calculate_unique_budgets(eur_enabled_budgets)
row_unique = calculate_unique_budgets(row_enabled_budgets)

# Calculate totals
uk_total_micros = sum(uk_unique.values())
usa_total_micros = sum(usa_unique.values())
eur_total_micros = sum(eur_unique.values())
row_total_micros = sum(row_unique.values())

# Convert to GBP
uk_total_gbp = uk_total_micros / 1_000_000
usa_total_gbp = usa_total_micros / 1_000_000
eur_total_gbp = eur_total_micros / 1_000_000
row_total_gbp = row_total_micros / 1_000_000

# Grand total
grand_total_gbp = uk_total_gbp + usa_total_gbp + eur_total_gbp + row_total_gbp

print("=" * 80)
print("CURRENT DAILY BUDGET - ENABLED CAMPAIGNS ONLY")
print("=" * 80)
print()
print(f"UK Account:   £{uk_total_gbp:,.2f}  ({len(uk_unique)} unique budget pools)")
print(f"USA Account:  £{usa_total_gbp:,.2f}  ({len(usa_unique)} unique budget pools)")
print(f"EUR Account:  £{eur_total_gbp:,.2f}  ({len(eur_unique)} unique budget pools)")
print(f"ROW Account:  £{row_total_gbp:,.2f}  ({len(row_unique)} unique budget pools)")
print()
print("-" * 80)
print(f"TOTAL:        £{grand_total_gbp:,.2f}")
print("=" * 80)
print()
print(f"Target:       £2,000.00")
print(f"Difference:   £{grand_total_gbp - 2000:+,.2f}")
print()
if grand_total_gbp < 2000:
    shortfall = 2000 - grand_total_gbp
    print(f"⚠️  SHORT by £{shortfall:,.2f}")
elif grand_total_gbp > 2000:
    print(f"✅ OVER by £{grand_total_gbp - 2000:,.2f}")
else:
    print(f"✅ EXACTLY on target")
print()
