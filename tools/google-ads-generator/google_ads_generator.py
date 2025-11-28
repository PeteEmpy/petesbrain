#!/usr/bin/env python3
"""
Google Ads Text Generator
Creates headlines, descriptions, sitelinks, callouts, and search themes
according to ROK specifications.
"""

import sys
from typing import List, Dict
import json


class GoogleAdsAssetGenerator:
    """Generates Google Ads text assets with character limit validation."""

    HEADLINE_MAX = 30
    DESCRIPTION_MAX = 90
    SITELINK_HEADLINE_MAX = 25
    SITELINK_DESC_MAX = 35

    def __init__(self, product_name: str, brand: str, website_url: str):
        self.product_name = product_name
        self.brand = brand
        self.website_url = website_url
        self.headlines = []
        self.descriptions = []
        self.sitelinks = []
        self.callouts = []
        self.search_themes = []

    def validate_length(self, text: str, max_length: int, field_type: str) -> bool:
        """Validate text length and return True if valid."""
        if len(text) > max_length:
            print(f"⚠️  Warning: {field_type} exceeds {max_length} chars: '{text}' ({len(text)} chars)")
            return False
        return True

    def add_headline(self, text: str, section: str) -> bool:
        """Add a headline with validation."""
        if self.validate_length(text, self.HEADLINE_MAX, "Headline"):
            self.headlines.append({"text": text, "length": len(text), "section": section})
            return True
        return False

    def add_description(self, text: str, section: str) -> bool:
        """Add a description with validation."""
        if self.validate_length(text, self.DESCRIPTION_MAX, "Description"):
            self.descriptions.append({"text": text, "length": len(text), "section": section})
            return True
        return False

    def add_sitelink(self, headline: str, desc1: str, desc2: str, url: str) -> bool:
        """Add a sitelink with validation."""
        valid = True
        valid &= self.validate_length(headline, self.SITELINK_HEADLINE_MAX, "Sitelink headline")
        valid &= self.validate_length(desc1, self.SITELINK_DESC_MAX, "Sitelink desc 1")
        valid &= self.validate_length(desc2, self.SITELINK_DESC_MAX, "Sitelink desc 2")

        if valid:
            self.sitelinks.append({
                "headline": headline,
                "desc1": desc1,
                "desc2": desc2,
                "url": url
            })
        return valid

    def add_callout(self, text: str) -> bool:
        """Add a callout extension."""
        if self.validate_length(text, 25, "Callout"):
            self.callouts.append(text)
            return True
        return False

    def add_search_theme(self, theme: str):
        """Add a search theme (no length limit)."""
        self.search_themes.append(theme)

    def generate_output(self) -> str:
        """Generate formatted output with all assets."""
        output = []
        output.append("=" * 80)
        output.append("GOOGLE ADS TEXT ASSETS - COMPLETE OUTPUT")
        output.append(f"Product: {self.product_name} | Brand: {self.brand}")
        output.append("=" * 80)
        output.append("")

        # 1. Search Themes
        output.append("1. SEARCH THEMES (for Performance Max Asset Group)")
        output.append("-" * 80)
        for theme in self.search_themes:
            output.append(theme)
        output.append(f"\nTotal: {len(self.search_themes)} search themes")
        output.append("")

        # 2. Headlines
        output.append("2. HEADLINES (30 character max)")
        output.append("-" * 80)

        sections = ["Benefits", "Technical", "Quirky", "Call to Action", "Brand/Category"]
        for section in sections:
            section_headlines = [h for h in self.headlines if h["section"] == section]
            if section_headlines:
                output.append(f"\n{section.upper()}")
                for i, h in enumerate(section_headlines, 1):
                    output.append(f"{i:2d}. {h['text']:<30} [{h['length']:2d} chars]")

        output.append(f"\nTotal: {len(self.headlines)} headlines")
        output.append("")

        # 3. Descriptions
        output.append("3. DESCRIPTIONS (90 character max)")
        output.append("-" * 80)

        for section in sections:
            section_descs = [d for d in self.descriptions if d["section"] == section]
            if section_descs:
                output.append(f"\n{section.upper()}")
                for i, d in enumerate(section_descs, 1):
                    output.append(f"{i:2d}. {d['text']:<90} [{d['length']:2d} chars]")

        output.append(f"\nTotal: {len(self.descriptions)} descriptions")
        output.append("")

        # 4. Sitelinks
        output.append("4. SITELINKS")
        output.append("-" * 80)
        for i, sl in enumerate(self.sitelinks, 1):
            output.append(f"\nSitelink {i}:")
            output.append(f"  Headline: {sl['headline']} [{len(sl['headline'])} chars]")
            output.append(f"  Desc 1:   {sl['desc1']} [{len(sl['desc1'])} chars]")
            output.append(f"  Desc 2:   {sl['desc2']} [{len(sl['desc2'])} chars]")
            output.append(f"  URL:      {sl['url']}")

        output.append(f"\nTotal: {len(self.sitelinks)} sitelinks")
        output.append("")

        # 5. Callouts
        output.append("5. CALLOUT EXTENSIONS")
        output.append("-" * 80)
        for i, callout in enumerate(self.callouts, 1):
            output.append(f"{i}. {callout}")

        output.append(f"\nTotal: {len(self.callouts)} callouts")
        output.append("")
        output.append("=" * 80)

        return "\n".join(output)

    def export_csv(self) -> str:
        """Export headlines and descriptions as CSV for Google Ads Editor."""
        lines = ["Type,Text,Length,Section,Landing Page"]

        for h in self.headlines:
            lines.append(f"Headline,\"{h['text']}\",{h['length']},{h['section']},{self.website_url}")

        for d in self.descriptions:
            lines.append(f"Description,\"{d['text']}\",{d['length']},{d['section']},{self.website_url}")

        return "\n".join(lines)


def main():
    """Interactive mode for generating assets."""
    print("=" * 80)
    print("GOOGLE ADS TEXT GENERATOR")
    print("=" * 80)
    print()

    # Get basic information
    if len(sys.argv) > 1:
        product_name = " ".join(sys.argv[1:])
    else:
        product_name = input("Enter product/service name: ").strip()

    brand = input("Enter brand name: ").strip()
    website_url = input("Enter website URL: ").strip()

    print()
    print(f"Creating assets for: {product_name} ({brand})")
    print()

    generator = GoogleAdsAssetGenerator(product_name, brand, website_url)

    # Interactive input for each section
    print("Now you can add assets interactively.")
    print()
    print("INSTRUCTIONS:")
    print("- Enter assets for each section as prompted")
    print("- Type 'done' to move to the next section")
    print("- Type 'skip' to skip a section")
    print("- Type 'quit' to finish and generate output")
    print()

    sections = [
        ("Benefits", "Benefits - why they can't live without it"),
        ("Technical", "Technical advantages"),
        ("Quirky", "Quirky/humorous descriptions"),
        ("Call to Action", "Call to action - persuade to buy now"),
        ("Brand/Category", "Product/category with brand highlights")
    ]

    # Headlines
    print("\n" + "=" * 80)
    print("HEADLINES (30 character maximum)")
    print("=" * 80)

    for section_key, section_desc in sections:
        print(f"\n--- {section_desc} ---")
        print(f"Target: 10 headlines for this section")
        count = 0
        while count < 10:
            headline = input(f"Headline {count+1}: ").strip()
            if headline.lower() == 'done':
                break
            if headline.lower() == 'skip':
                break
            if headline.lower() == 'quit':
                break
            if headline:
                if generator.add_headline(headline, section_key):
                    count += 1
        if headline.lower() == 'quit':
            break

    # Descriptions
    if headline.lower() != 'quit':
        print("\n" + "=" * 80)
        print("DESCRIPTIONS (90 character maximum)")
        print("=" * 80)

        for section_key, section_desc in sections:
            print(f"\n--- {section_desc} ---")
            print(f"Target: 10 descriptions for this section")
            count = 0
            while count < 10:
                desc = input(f"Description {count+1}: ").strip()
                if desc.lower() == 'done':
                    break
                if desc.lower() == 'skip':
                    break
                if desc.lower() == 'quit':
                    break
                if desc:
                    if generator.add_description(desc, section_key):
                        count += 1
            if desc.lower() == 'quit':
                break

    # Generate output
    print("\n" + "=" * 80)
    print("GENERATING OUTPUT...")
    print("=" * 80)

    output = generator.generate_output()
    print("\n" + output)

    # Save to file
    output_file = f"google_ads_assets_{product_name.replace(' ', '_').lower()}.txt"
    with open(output_file, 'w') as f:
        f.write(output)
    print(f"\n✅ Output saved to: {output_file}")

    # Export CSV
    csv_file = f"google_ads_assets_{product_name.replace(' ', '_').lower()}.csv"
    csv_output = generator.export_csv()
    with open(csv_file, 'w') as f:
        f.write(csv_output)
    print(f"✅ CSV export saved to: {csv_file}")
    print()


if __name__ == "__main__":
    main()
