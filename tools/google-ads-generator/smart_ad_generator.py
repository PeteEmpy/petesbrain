#!/usr/bin/env python3
"""
Smart Ad Generator - Content-First Professional Copy
Extracts page content and generates high-quality, specific ad copy.
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Dict, List


class SmartAdGenerator:
    """Generates professional ad copy from actual website content."""

    def __init__(self, url: str):
        self.url = url
        self.domain = urlparse(url).netloc
        self.soup = None

        # Extracted content
        self.title = ""
        self.meta_desc = ""
        self.h1_tags = []
        self.h2_tags = []
        self.paragraphs = []
        self.list_items = []
        self.brand = ""
        self.product_name = ""

    def fetch_and_parse(self) -> bool:
        """Fetch URL and extract content."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()

            self.soup = BeautifulSoup(response.text, 'html.parser')

            # Remove noise
            for tag in self.soup(['script', 'style', 'nav', 'footer']):
                tag.decompose()

            self._extract_content()
            return True

        except Exception as e:
            print(f"Error fetching URL: {e}")
            return False

    def _extract_content(self):
        """Extract all useful content from page."""
        # Title
        title_tag = self.soup.find('title')
        if title_tag:
            self.title = self._clean(title_tag.get_text())
            # Extract product name from title (before | or -)
            parts = re.split(r'[|\-–]', self.title)
            self.product_name = parts[0].strip() if parts else self.title
            # Clean up extra brand names from product
            for word in ['BrightMinds', 'UK', 'Shop', 'Store', 'Online']:
                self.product_name = re.sub(rf'\s*{word}\s*', ' ', self.product_name, flags=re.IGNORECASE)
            self.product_name = ' '.join(self.product_name.split()).strip()

        # Meta description
        meta = self.soup.find('meta', attrs={'name': 'description'}) or \
               self.soup.find('meta', attrs={'property': 'og:description'})
        if meta and meta.get('content'):
            self.meta_desc = self._clean(meta.get('content'))

        # Brand from domain - get the actual brand name, not TLD
        domain_parts = self.domain.replace('www.', '').split('.')
        if domain_parts:
            self.brand = domain_parts[0].replace('-', ' ').replace('_', ' ').title()

        # H1 tags
        self.h1_tags = [self._clean(h1.get_text()) for h1 in self.soup.find_all('h1')[:5]]

        # Use H1 as product name if it's cleaner than title
        if self.h1_tags and len(self.h1_tags[0]) < len(self.product_name):
            self.product_name = self.h1_tags[0]

        # H2 tags
        self.h2_tags = [self._clean(h2.get_text()) for h2 in self.soup.find_all('h2')[:15]]

        # Paragraphs
        self.paragraphs = [self._clean(p.get_text()) for p in self.soup.find_all('p')[:20]
                          if len(self._clean(p.get_text())) > 20]

        # List items
        self.list_items = [self._clean(li.get_text()) for li in self.soup.find_all('li')[:25]
                          if len(self._clean(li.get_text())) > 10]

    def _clean(self, text: str) -> str:
        """Clean text."""
        text = ' '.join(text.split())
        text = re.sub(r'[^\w\s&\-\',.]', '', text)
        return text.strip()

    def _enforce_limit(self, text: str, max_len: int) -> str:
        """STRICTLY enforce character limit, cutting at word boundary."""
        if not text:
            return ""

        # Already within limit
        if len(text) <= max_len:
            return text

        # Cut at last space before limit
        trimmed = text[:max_len]
        last_space = trimmed.rfind(' ')

        # If we have a reasonable space position, cut there
        if last_space > max_len * 0.6:
            return trimmed[:last_space].strip()

        # Otherwise just hard cut (better than exceeding limit)
        return trimmed.strip()

    def generate_headlines(self) -> Dict[str, List[str]]:
        """Generate 50 headlines across 5 sections."""
        headlines = {
            "benefits": self._generate_benefits_headlines(),
            "technical": self._generate_technical_headlines(),
            "quirky": self._generate_quirky_headlines(),
            "cta": self._generate_cta_headlines(),
            "brand": self._generate_brand_headlines()
        }

        # Ensure exactly 10 per section
        for section in headlines:
            headlines[section] = headlines[section][:10]
            while len(headlines[section]) < 10:
                headlines[section].append(self._enforce_limit(f"{self.product_name}", 30))

        return headlines

    def _generate_benefits_headlines(self) -> List[str]:
        """Benefits: Why they can't live without it."""
        headlines = []

        # Use H1s and H2s that sound like benefits
        for h in (self.h1_tags + self.h2_tags):
            if len(h) >= 10 and len(h) <= 50:
                headline = self._enforce_limit(h, 30)
                if headline and headline not in headlines:
                    headlines.append(headline)
                    if len(headlines) >= 10:
                        return headlines

        # Use meta description as source
        if self.meta_desc:
            sentences = self.meta_desc.split('.')
            for sent in sentences:
                sent = sent.strip()
                if 10 <= len(sent) <= 50:
                    headline = self._enforce_limit(sent, 30)
                    if headline and headline not in headlines:
                        headlines.append(headline)
                        if len(headlines) >= 10:
                            return headlines

        # Use list items
        for item in self.list_items:
            if 10 <= len(item) <= 50:
                headline = self._enforce_limit(item, 30)
                if headline and headline not in headlines:
                    headlines.append(headline)
                    if len(headlines) >= 10:
                        return headlines

        return headlines

    def _generate_technical_headlines(self) -> List[str]:
        """Technical: Specific advantages and features."""
        headlines = []

        # Use H2s for features/specs
        for h2 in self.h2_tags:
            if 8 <= len(h2) <= 50:
                headline = self._enforce_limit(h2, 30)
                if headline and headline not in headlines:
                    headlines.append(headline)
                    if len(headlines) >= 10:
                        return headlines

        # Use list items that sound technical
        for item in self.list_items:
            if 10 <= len(item) <= 50:
                headline = self._enforce_limit(item, 30)
                if headline and headline not in headlines:
                    headlines.append(headline)
                    if len(headlines) >= 10:
                        return headlines

        return headlines

    def _generate_quirky_headlines(self) -> List[str]:
        """Quirky: Engaging with personality."""
        product = self._enforce_limit(self.product_name, 20)

        return [
            self._enforce_limit(f"Discover {product}", 30),
            self._enforce_limit(f"Love {product}", 30),
            self._enforce_limit(f"Perfect {product}", 30),
            self._enforce_limit(f"Amazing {product} Awaits", 30),
            self._enforce_limit(f"Your {product} Journey", 30),
            self._enforce_limit(f"Experience {product}", 30),
            self._enforce_limit(f"Explore {product}", 30),
            self._enforce_limit(f"Quality {product}", 30),
            self._enforce_limit(f"Premium {product}", 30),
            self._enforce_limit(f"Best {product}", 30),
        ]

    def _generate_cta_headlines(self) -> List[str]:
        """CTA: Action-oriented, not aggressive."""
        product = self._enforce_limit(self.product_name, 15)

        return [
            self._enforce_limit(f"Shop {product}", 30),
            self._enforce_limit(f"Browse {product}", 30),
            self._enforce_limit(f"Explore {product}", 30),
            self._enforce_limit(f"Discover {product}", 30),
            self._enforce_limit(f"Find Your {product}", 30),
            self._enforce_limit(f"Order {product} Today", 30),
            self._enforce_limit(f"Get {product}", 30),
            self._enforce_limit(f"View {product} Range", 30),
            self._enforce_limit(f"Choose {product}", 30),
            self._enforce_limit(f"Buy {product}", 30),
        ]

    def _generate_brand_headlines(self) -> List[str]:
        """Brand: Company/product positioning."""
        product = self._enforce_limit(self.product_name, 18)
        brand = self._enforce_limit(self.brand, 15) if self.brand else ""

        headlines = []

        if brand:
            headlines = [
                self._enforce_limit(f"{brand} {product}", 30),
                self._enforce_limit(f"Official {brand} Store", 30),
                self._enforce_limit(f"{brand} Collection", 30),
                self._enforce_limit(f"{brand} Range", 30),
                self._enforce_limit(f"Shop {brand}", 30),
                self._enforce_limit(f"{brand} Products", 30),
                self._enforce_limit(f"Buy {brand}", 30),
                self._enforce_limit(f"{brand} Online", 30),
                self._enforce_limit(f"{brand} UK", 30),
                self._enforce_limit(f"Trusted {brand}", 30),
            ]
        else:
            headlines = [
                self._enforce_limit(f"{product} Store", 30),
                self._enforce_limit(f"{product} Collection", 30),
                self._enforce_limit(f"{product} Range", 30),
                self._enforce_limit(f"Shop {product}", 30),
                self._enforce_limit(f"Buy {product} Online", 30),
                self._enforce_limit(f"Quality {product}", 30),
                self._enforce_limit(f"Premium {product}", 30),
                self._enforce_limit(f"{product} UK", 30),
                self._enforce_limit(f"Best {product}", 30),
                self._enforce_limit(f"Top {product}", 30),
            ]

        return headlines

    def generate_descriptions(self) -> Dict[str, List[str]]:
        """Generate 50 descriptions across 5 sections."""
        descriptions = {
            "benefits": self._generate_benefits_descriptions(),
            "technical": self._generate_technical_descriptions(),
            "quirky": self._generate_quirky_descriptions(),
            "cta": self._generate_cta_descriptions(),
            "brand": self._generate_brand_descriptions()
        }

        # Ensure exactly 10 per section
        for section in descriptions:
            descriptions[section] = descriptions[section][:10]
            while len(descriptions[section]) < 10:
                fallback = f"{self.product_name}. {self.meta_desc[:60] if self.meta_desc else 'Quality products'}"
                descriptions[section].append(self._enforce_limit(fallback, 90))

        return descriptions

    def _generate_benefits_descriptions(self) -> List[str]:
        """Benefits descriptions."""
        descriptions = []

        # Use meta description
        if self.meta_desc:
            descriptions.append(self._enforce_limit(self.meta_desc, 90))

        # Use paragraphs
        for para in self.paragraphs:
            if 30 <= len(para) <= 150:
                desc = self._enforce_limit(para, 90)
                if desc and desc not in descriptions:
                    descriptions.append(desc)
                    if len(descriptions) >= 10:
                        return descriptions

        # Combine H1 + list items
        if self.h1_tags and self.list_items:
            for item in self.list_items[:5]:
                desc = f"{self.h1_tags[0]}. {item}"
                desc = self._enforce_limit(desc, 90)
                if desc and desc not in descriptions:
                    descriptions.append(desc)
                    if len(descriptions) >= 10:
                        return descriptions

        return descriptions

    def _generate_technical_descriptions(self) -> List[str]:
        """Technical descriptions."""
        descriptions = []

        # Use H2s with context
        for h2 in self.h2_tags:
            desc = f"{self.product_name}. {h2}. Quality assured."
            desc = self._enforce_limit(desc, 90)
            if desc and desc not in descriptions:
                descriptions.append(desc)
                if len(descriptions) >= 10:
                    return descriptions

        # Use list items as technical specs
        for item in self.list_items:
            if len(item) >= 20:
                desc = self._enforce_limit(item, 90)
                if desc and desc not in descriptions:
                    descriptions.append(desc)
                    if len(descriptions) >= 10:
                        return descriptions

        return descriptions

    def _generate_quirky_descriptions(self) -> List[str]:
        """Quirky descriptions."""
        product = self.product_name

        templates = [
            f"Discover why everyone loves {product}. Shop our range today for quality assured.",
            f"The {product} you've been searching for. Browse our collection now online.",
            f"Transform your experience with {product}. Trusted by thousands nationwide.",
            f"Premium {product} at great prices. Free UK delivery available on orders.",
            f"Why settle for less? Choose {product} for guaranteed satisfaction every time.",
            f"{product} made easy. Browse, choose, and enjoy. Simple as that with us.",
            f"Join thousands who've chosen {product}. See the difference for yourself today.",
            f"Your search for perfect {product} ends here. Quality guaranteed always.",
            f"Experience the {product} difference. Shop with confidence online today.",
            f"Finally, {product} that delivers. Quality products at competitive prices.",
        ]

        return [self._enforce_limit(t, 90) for t in templates]

    def _generate_cta_descriptions(self) -> List[str]:
        """CTA descriptions."""
        product = self.product_name

        templates = [
            f"Shop {product} now. Free UK delivery. Easy returns. Order today online.",
            f"Buy {product} with confidence. Quality guaranteed. Fast dispatch nationwide.",
            f"Order {product} today. Trusted by thousands. Secure checkout available.",
            f"Get your {product} delivered fast. Shop now for best selection online.",
            f"Browse {product} range. Expert advice available. Order online now easily.",
            f"Discover {product} collection. Premium quality. Great prices. Shop now.",
            f"Find your perfect {product}. Easy ordering. Fast delivery. Buy today.",
            f"Choose from our {product} range. Secure payment. Quick dispatch daily.",
            f"Explore {product} options. Quality products. Competitive prices. Order now.",
            f"Try {product} risk-free. Money-back guarantee. Shop with confidence today.",
        ]

        return [self._enforce_limit(t, 90) for t in templates]

    def _generate_brand_descriptions(self) -> List[str]:
        """Brand descriptions."""
        product = self.product_name
        brand = self.brand if self.brand else "We"

        templates = [
            f"{brand} - Your trusted source for {product}. Quality guaranteed always.",
            f"Discover the {brand} difference. Premium {product} for everyone nationwide.",
            f"Official {brand} store. {product} delivered direct. Shop now online.",
            f"{brand} delivers quality {product}. Trusted by thousands. Order today.",
            f"Choose {brand} for {product}. Expert service. Fast delivery guaranteed.",
            f"{brand} - Where quality meets value. Premium {product} at great prices.",
            f"Trust {brand} for your {product} needs. Satisfaction guaranteed always.",
            f"{brand} brings you the best {product}. Shop our full range online.",
            f"Experience {brand} quality. {product} that deliver results every time.",
            f"{brand} - Your {product} specialists. Browse our collection now online.",
        ]

        return [self._enforce_limit(t, 90) for t in templates]

    def generate_complete_rsa(self) -> Dict:
        """Generate complete RSA ad set."""
        return {
            "url": self.url,
            "headlines": self.generate_headlines(),
            "descriptions": self.generate_descriptions(),
            "page_info": {
                "brand": self.brand,
                "product": self.product_name,
                "category": self.product_name
            }
        }


if __name__ == "__main__":
    # Test
    url = "https://www.brightminds.co.uk/collections/engineering-toys"
    generator = SmartAdGenerator(url)

    if generator.fetch_and_parse():
        ads = generator.generate_complete_rsa()

        print("\n" + "="*80)
        print("HEADLINES")
        print("="*80)
        for section, headlines in ads["headlines"].items():
            print(f"\n{section.upper()}:")
            for i, h in enumerate(headlines, 1):
                print(f"  {i:2d}. {h:<30} [{len(h):2d}/30]")

        print("\n" + "="*80)
        print("DESCRIPTIONS")
        print("="*80)
        for section, descriptions in ads["descriptions"].items():
            print(f"\n{section.upper()}:")
            for i, d in enumerate(descriptions, 1):
                print(f"  {i:2d}. {d} [{len(d):2d}/90]")
