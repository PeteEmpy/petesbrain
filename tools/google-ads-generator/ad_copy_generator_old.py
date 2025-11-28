#!/usr/bin/env python3
"""
Ad Copy Generator
Generates Google Ads copy from URL content analysis.
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Dict, List, Set
import random


class AdCopyGenerator:
    """Generates ad copy based on website content."""

    def __init__(self, url: str):
        self.url = url
        self.domain = urlparse(url).netloc
        self.content = ""
        self.soup = None
        self.product_info = {}
        self.extracted_features = []
        self.extracted_benefits = []
        self.product_name = ""
        self.category = ""

    def fetch_url_content(self) -> bool:
        """Fetch and parse URL content."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()

            self.content = response.text
            self.soup = BeautifulSoup(self.content, 'html.parser')

            # Remove script and style elements
            for script in self.soup(["script", "style"]):
                script.decompose()

            return True
        except Exception as e:
            print(f"Error fetching URL: {e}")
            return False

    def extract_page_info(self) -> Dict:
        """Extract key information from the page."""
        if not self.soup:
            return {}

        info = {
            "title": "",
            "description": "",
            "h1": [],
            "h2": [],
            "h3": [],
            "keywords": [],
            "brand": "",
            "text_content": "",
            "lists": [],
            "strong_text": []
        }

        # Title
        title_tag = self.soup.find('title')
        if title_tag:
            info["title"] = title_tag.get_text().strip()
            # Extract product name from title (usually before | or -)
            title_parts = re.split(r'[|\-–]', info["title"])
            if title_parts:
                self.product_name = title_parts[0].strip()

        # Meta description
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = self.soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc and meta_desc.get('content'):
            info["description"] = meta_desc.get('content').strip()

        # Keywords
        meta_keywords = self.soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
            info["keywords"] = [k.strip() for k in meta_keywords.get('content').split(',')]

        # H1 tags
        h1_tags = self.soup.find_all('h1')
        info["h1"] = [h1.get_text().strip() for h1 in h1_tags[:5]]

        # H2 tags
        h2_tags = self.soup.find_all('h2')
        info["h2"] = [h2.get_text().strip() for h2 in h2_tags[:10]]

        # H3 tags
        h3_tags = self.soup.find_all('h3')
        info["h3"] = [h3.get_text().strip() for h3 in h3_tags[:10]]

        # Extract brand from domain
        domain_parts = self.domain.split('.')
        if len(domain_parts) >= 2:
            info["brand"] = domain_parts[-2].replace('-', ' ').replace('_', ' ').title()

        # Get main text content
        paragraphs = self.soup.find_all('p')
        text_content = ' '.join([p.get_text().strip() for p in paragraphs[:20]])
        info["text_content"] = text_content[:2000]

        # Extract list items (often contain features/benefits)
        list_items = self.soup.find_all('li')
        info["lists"] = [li.get_text().strip() for li in list_items[:20]]

        # Extract strong/bold text (often highlights key features)
        strong_tags = self.soup.find_all(['strong', 'b'])
        info["strong_text"] = [s.get_text().strip() for s in strong_tags[:15]]

        self.product_info = info
        self._analyze_content()
        return info

    def _analyze_content(self):
        """Analyze content to extract features, benefits, and keywords."""
        info = self.product_info

        # Extract features from lists and headers
        all_text = []
        all_text.extend(info.get("h2", []))
        all_text.extend(info.get("h3", []))
        all_text.extend(info.get("lists", []))
        all_text.extend(info.get("strong_text", []))

        # Look for feature keywords
        feature_keywords = [
            'advanced', 'premium', 'professional', 'quality', 'durable',
            'lightweight', 'powerful', 'fast', 'efficient', 'innovative',
            'certified', 'award', 'patented', 'exclusive', 'unique',
            'waterproof', 'wireless', 'automatic', 'smart', 'digital'
        ]

        # Look for benefit keywords
        benefit_keywords = [
            'save', 'free', 'easy', 'simple', 'comfortable', 'reliable',
            'trusted', 'guaranteed', 'secure', 'affordable', 'value',
            'satisfaction', 'results', 'improve', 'enhance', 'perfect'
        ]

        for text in all_text:
            text_lower = text.lower()
            # Extract features
            for keyword in feature_keywords:
                if keyword in text_lower and len(text) < 100:
                    self.extracted_features.append(text)
                    break
            # Extract benefits
            for keyword in benefit_keywords:
                if keyword in text_lower and len(text) < 100:
                    self.extracted_benefits.append(text)
                    break

        # Deduplicate
        self.extracted_features = list(dict.fromkeys(self.extracted_features))[:15]
        self.extracted_benefits = list(dict.fromkeys(self.extracted_benefits))[:15]

        # Determine category
        self.category = self._get_category()

    def generate_rsa_headlines(self) -> Dict[str, List[str]]:
        """Generate 50 headlines across 5 sections using actual page content."""
        info = self.product_info
        brand = info.get("brand", "")
        title = info.get("title", "")
        h1_text = info.get("h1", [""])[0] if info.get("h1") else ""
        h2_texts = info.get("h2", [])

        headlines = {
            "benefits": [],
            "technical": [],
            "quirky": [],
            "cta": [],
            "brand": []
        }

        # Get key phrases from content
        key_phrases = self._extract_key_phrases()

        # BENEFITS (10 headlines) - Focus on customer value
        benefits = []

        # Use extracted benefits
        for benefit in self.extracted_benefits[:5]:
            headline = self._create_benefit_headline(benefit)
            if headline:
                benefits.append(headline)

        # Add generic benefits with product/category context
        product_ref = self.product_name[:20] if self.product_name else self.category
        generic_benefits = [
            f"Transform Your {self.category}",
            f"Premium {product_ref}" if product_ref else "Premium Quality",
            f"Best {self.category} Solution",
            "Unmatched Quality & Value",
            "Get Results That Last",
            "Experience The Difference",
            "Your Perfect Solution",
            "Quality You Can Trust",
            "Elevate Your Experience",
            "The Smart Choice"
        ]

        benefits.extend(generic_benefits)
        headlines["benefits"] = [self._trim_to_length(h, 30) for h in benefits[:10]]

        # TECHNICAL (10 headlines) - Features and specs
        technical = []

        # Use extracted features
        for feature in self.extracted_features[:5]:
            headline = self._create_technical_headline(feature)
            if headline:
                technical.append(headline)

        # Use H2s as features if they look technical
        for h2 in h2_texts[:3]:
            if any(word in h2.lower() for word in ['feature', 'tech', 'advanced', 'premium', 'professional']):
                technical.append(h2)

        # Generic technical
        generic_technical = [
            "Advanced Technology",
            "Professional Grade Quality",
            "Industry-Leading Performance",
            "Premium Materials Used",
            "Expertly Engineered",
            "Built To Last",
            "Award-Winning Design",
            "Precision Crafted"
        ]

        technical.extend(generic_technical)
        headlines["technical"] = [self._trim_to_length(h, 30) for h in technical[:10]]

        # QUIRKY (10 headlines) - Creative and engaging
        quirky = []

        product_quirky = [
            f"Your New Favorite {self.category}",
            f"Finally, {product_ref}" if product_ref else "Finally, What You Need",
            f"{self.category} Made Easy",
            "Better Than The Rest",
            "The Upgrade You Deserve",
            "Simply Outstanding",
            "Beyond Expectations",
            "Your Happy Place",
            "Love At First Try",
            "Why Settle For Less?"
        ]

        headlines["quirky"] = [self._trim_to_length(h, 30) for h in product_quirky[:10]]

        # CALL TO ACTION (10 headlines)
        cta = [
            "Shop Now - Free Shipping",
            f"Order {product_ref} Today" if product_ref else "Order Today & Save",
            "Get Yours Today",
            "Limited Time Offer",
            "Buy Now & Save",
            f"Discover {brand}" if brand else "Discover The Range",
            "Browse Our Collection",
            "Start Shopping Now",
            "See Our Best Sellers",
            "Join Thousands Of Customers"
        ]
        headlines["cta"] = [self._trim_to_length(h, 30) for h in cta[:10]]

        # BRAND/CATEGORY (10 headlines)
        brand_headlines = []

        if brand:
            brand_headlines.extend([
                f"{brand} {self.category}",
                f"Official {brand} Store",
                f"{brand} - Trusted Quality",
                f"{brand} Collection",
                f"Premium {brand} Products"
            ])

        brand_headlines.extend([
            f"UK's Leading {self.category}",
            f"Professional {self.category}",
            f"Expert {self.category} Specialists",
            "Award-Winning Company",
            "Your Reliable Partner"
        ])

        headlines["brand"] = [self._trim_to_length(h, 30) for h in brand_headlines[:10]]

        return headlines

    def generate_rsa_descriptions(self) -> Dict[str, List[str]]:
        """Generate 50 descriptions across 5 sections using actual content."""
        info = self.product_info
        brand = info.get("brand", "")
        description = info.get("description", "")
        product_ref = self.product_name[:30] if self.product_name else self.category

        descriptions = {
            "benefits": [],
            "technical": [],
            "quirky": [],
            "cta": [],
            "brand": []
        }

        # BENEFITS (10 descriptions)
        benefits_desc = []

        # Use meta description if relevant
        if description and len(description) <= 90:
            benefits_desc.append(description)
        elif description:
            benefits_desc.append(self._trim_to_length(description, 90))

        # Use extracted benefits
        for benefit in self.extracted_benefits[:4]:
            desc = f"{benefit}. Experience the difference today."
            benefits_desc.append(desc)

        # Generic benefits with context
        generic_benefits_desc = [
            f"Transform your {self.category} experience with premium quality built to last.",
            f"Discover why thousands choose us for {self.category}. Quality guaranteed.",
            f"Premium {product_ref} designed for exceptional results and lasting value.",
            f"Experience unmatched quality. {brand if brand else 'We'} deliver excellence every time.",
            "Your satisfaction guaranteed. Quality, value, and outstanding service included.",
            "Make the smart choice. Premium products backed by expert service and support.",
            "Quality that speaks for itself. Get the results you've been looking for.",
            "Don't compromise on quality. Choose excellence backed by years of experience."
        ]

        benefits_desc.extend(generic_benefits_desc)
        descriptions["benefits"] = [self._trim_to_length(d, 90) for d in benefits_desc[:10]]

        # TECHNICAL (10 descriptions)
        technical_desc = []

        # Use extracted features
        for feature in self.extracted_features[:4]:
            desc = f"{feature}. Professional-grade performance you can trust."
            technical_desc.append(desc)

        # Generic technical with context
        generic_technical_desc = [
            f"Advanced {self.category} technology delivers superior results. Innovation you can trust.",
            "Professional-grade quality with industry-leading performance. Tested and proven.",
            "Expertly crafted using premium materials and advanced manufacturing techniques.",
            "Precision-engineered for optimal performance. Quality tested to highest standards.",
            "Superior construction ensures lasting durability. Built for years of reliable use.",
            "Premium quality materials and expert craftsmanship. Built to professional standards."
        ]

        technical_desc.extend(generic_technical_desc)
        descriptions["technical"] = [self._trim_to_length(d, 90) for d in technical_desc[:10]]

        # QUIRKY (10 descriptions)
        quirky_desc = [
            f"Spoiler: You're going to love your new {product_ref}. Join thousands of happy customers.",
            "Finally, quality that doesn't cost the earth. Your wallet will thank you.",
            "Warning: May cause sudden happiness. Side effects include complete satisfaction.",
            f"The {self.category} upgrade you didn't know you needed. Prepare to be impressed.",
            "Where quality meets affordability. It's like finding money in your pocket.",
            "Good news: We've made it easy to choose quality. You're welcome.",
            "Plot twist: Premium quality can be affordable. See for yourself today.",
            "Turns out, excellence doesn't have to be expensive. Who knew?",
            "Your search ends here. Finally, quality that delivers on its promises.",
            "Surprise! Quality products at prices that make sense. Check it out now."
        ]
        descriptions["quirky"] = [self._trim_to_length(d, 90) for d in quirky_desc[:10]]

        # CALL TO ACTION (10 descriptions)
        cta_desc = [
            "Shop now and enjoy free UK shipping on all orders. 30-day returns guaranteed.",
            f"Order your {product_ref} today. Fast delivery, easy returns, expert service.",
            "Don't miss out - limited stock available. Order now for next-day delivery.",
            "Browse our full range today. Free shipping and expert advice always available.",
            f"Get your {product_ref} today with price match guarantee. Quality and value combined.",
            "Discover our bestsellers. Fast delivery, secure checkout, and lifetime support.",
            "Buy with confidence. 5-star rated by thousands. Free shipping on all orders.",
            "Shop now and experience the difference. Easy returns and expert support included.",
            "Order today - satisfaction guaranteed. Fast delivery and great prices.",
            "Start shopping now. Thousands of happy customers. Join them today."
        ]
        descriptions["cta"] = [self._trim_to_length(d, 90) for d in cta_desc[:10]]

        # BRAND/CATEGORY (10 descriptions)
        brand_desc = []

        if brand:
            brand_desc.extend([
                f"{brand} - Your trusted partner for {self.category}. Quality and service guaranteed.",
                f"Discover the {brand} difference. Premium {self.category} trusted by thousands.",
                f"{brand} has been delivering excellence for years. Quality you can trust.",
                f"Official {brand} - Professional quality with personal service. Shop with confidence.",
                f"Choose {brand} for unmatched quality and value. Your satisfaction guaranteed."
            ])
        else:
            brand_desc.extend([
                f"Your trusted partner for {self.category}. Quality and service guaranteed.",
                f"Premium {self.category} trusted by thousands. Experience the difference.",
                "Delivering excellence for years. Quality you can trust every time.",
                "Professional quality with personal service. Shop with complete confidence.",
                "Unmatched quality and value. Your satisfaction is guaranteed."
            ])

        brand_desc.extend([
            f"Expert {self.category} specialists. Award-winning products backed by expert service.",
            f"Quality {self.category} solutions. Join our family of satisfied customers.",
            "Excellence in every detail. Your complete solution provider.",
            f"UK's leading {self.category} supplier. Professional service and premium quality.",
            f"Trusted by professionals. Premium {self.category} at accessible prices."
        ])

        descriptions["brand"] = [self._trim_to_length(d, 90) for d in brand_desc[:10]]

        return descriptions

    def _extract_key_phrases(self) -> List[str]:
        """Extract key phrases from content."""
        phrases = []

        # From H2s
        phrases.extend(self.product_info.get("h2", []))

        # From lists
        lists = self.product_info.get("lists", [])
        for item in lists[:10]:
            if len(item) < 80:
                phrases.append(item)

        return phrases[:20]

    def _create_benefit_headline(self, benefit_text: str) -> str:
        """Create a headline from a benefit text."""
        # Remove common prefixes
        text = benefit_text.strip()
        text = re.sub(r'^(Get|Enjoy|Experience|Discover)\s+', '', text, flags=re.IGNORECASE)

        # If it's already short enough, return it
        if len(text) <= 30:
            return text

        # Try to extract the core benefit
        words = text.split()
        if len(words) >= 3:
            # Return first 3-5 words
            return ' '.join(words[:4])

        return text[:30]

    def _create_technical_headline(self, feature_text: str) -> str:
        """Create a technical headline from feature text."""
        text = feature_text.strip()

        # If it's already good, return it
        if len(text) <= 30:
            return text

        # Extract key technical terms
        words = text.split()
        if len(words) >= 2:
            return ' '.join(words[:4])

        return text[:30]

    def _get_category(self) -> str:
        """Extract or infer the product category."""
        url_lower = self.url.lower()
        title_lower = self.product_info.get("title", "").lower()
        desc_lower = self.product_info.get("description", "").lower()

        all_text = f"{url_lower} {title_lower} {desc_lower}"

        categories = {
            "shoes": "Footwear",
            "shoe": "Footwear",
            "sneaker": "Sneakers",
            "boot": "Boots",
            "clothing": "Clothing",
            "clothes": "Clothing",
            "fashion": "Fashion",
            "apparel": "Apparel",
            "tech": "Technology",
            "electronic": "Electronics",
            "gadget": "Gadgets",
            "software": "Software",
            "app": "Software",
            "food": "Food",
            "restaurant": "Dining",
            "home": "Home",
            "furniture": "Furniture",
            "garden": "Garden",
            "sport": "Sports",
            "fitness": "Fitness",
            "health": "Health",
            "beauty": "Beauty",
            "cosmetic": "Cosmetics",
            "jewelry": "Jewelry",
            "watch": "Watches",
            "toy": "Toys",
            "game": "Games",
            "book": "Books",
            "music": "Music",
            "travel": "Travel",
            "hotel": "Hotels",
            "car": "Automotive",
            "auto": "Automotive",
            "service": "Services",
            "product": "Products"
        }

        for keyword, category in categories.items():
            if keyword in all_text:
                return category

        return "Products"

    def _trim_to_length(self, text: str, max_length: int) -> str:
        """Trim text to maximum length, cutting at word boundary."""
        if len(text) <= max_length:
            return text

        # Cut at last space before max_length
        trimmed = text[:max_length]
        last_space = trimmed.rfind(' ')
        if last_space > max_length * 0.7:  # Only cut at space if it's not too far back
            trimmed = trimmed[:last_space]

        return trimmed

    def generate_complete_rsa(self) -> Dict:
        """Generate complete RSA ad set."""
        if not self.product_info:
            self.extract_page_info()

        return {
            "url": self.url,
            "page_info": self.product_info,
            "headlines": self.generate_rsa_headlines(),
            "descriptions": self.generate_rsa_descriptions()
        }


def test_generator():
    """Test the generator with a real URL."""
    url = input("Enter URL to analyze: ").strip()
    if not url:
        url = "https://www.example.com"

    print(f"\nFetching and analyzing: {url}\n")

    generator = AdCopyGenerator(url)

    if generator.fetch_url_content():
        print("✅ URL fetched successfully")

        info = generator.extract_page_info()
        print(f"\nPage Info:")
        print(f"  Title: {info.get('title', 'N/A')}")
        print(f"  Brand: {info.get('brand', 'N/A')}")
        print(f"  Product Name: {generator.product_name}")
        print(f"  Category: {generator.category}")
        print(f"  Description: {info.get('description', 'N/A')[:100]}...")
        print(f"\n  Extracted Features: {len(generator.extracted_features)}")
        for feat in generator.extracted_features[:5]:
            print(f"    - {feat[:60]}")
        print(f"\n  Extracted Benefits: {len(generator.extracted_benefits)}")
        for ben in generator.extracted_benefits[:5]:
            print(f"    - {ben[:60]}")

        rsa = generator.generate_complete_rsa()

        print(f"\n{'='*80}")
        print("GENERATED HEADLINES")
        print(f"{'='*80}")
        for section, headlines in rsa["headlines"].items():
            print(f"\n{section.upper()}")
            for i, h in enumerate(headlines, 1):
                print(f"  {i:2d}. {h:<30} [{len(h):2d} chars]")

        print(f"\n{'='*80}")
        print("GENERATED DESCRIPTIONS")
        print(f"{'='*80}")
        for section, descriptions in rsa["descriptions"].items():
            print(f"\n{section.upper()}")
            for i, d in enumerate(descriptions, 1):
                print(f"  {i:2d}. {d:<90} [{len(d):2d} chars]")
    else:
        print("❌ Failed to fetch URL")


if __name__ == "__main__":
    test_generator()
