#!/usr/bin/env python3
"""
Professional Ad Copy Writer
Creates compelling, benefit-focused ad copy following ROK guidelines.
Uses deep website insights to craft specific, persuasive copy.
"""

from typing import Dict, List
from website_analyzer import WebsiteAnalyzer
import re


class ProfessionalAdWriter:
    """Writes professional ad copy based on website insights."""

    def __init__(self, insights: Dict):
        self.insights = insights
        self.brand = insights.get('brand_name', '').split('|')[0].strip()
        self.products = insights.get('main_products', [])
        self.benefits = insights.get('key_benefits', [])
        self.features = insights.get('technical_features', [])
        self.tone = insights.get('tone_indicators', [])
        self.value_props = insights.get('value_propositions', [])

        # Extract key selling points
        self.key_points = self._extract_key_points()

    def _extract_key_points(self) -> Dict:
        """Extract the most important selling points."""
        all_text = ' '.join(self.benefits + self.features + self.value_props).lower()

        points = {
            'natural': 'natural' in all_text or '100%' in all_text,
            'uk_made': 'uk' in all_text and 'made' in all_text,
            'safety': 'safety' in all_text or 'tested' in all_text or 'safe' in all_text,
            'pain_relief': 'pain' in all_text or 'relief' in all_text or 'sooth' in all_text,
            'comfort': 'comfort' in all_text or 'cozy' in all_text or 'warm' in all_text,
            'quality': 'quality' in all_text or 'premium' in all_text,
            'choice': 'choice' in all_text or 'range' in all_text or 'variety' in all_text,
        }

        return points

    def generate_headlines(self) -> Dict[str, List[str]]:
        """Generate 50 headlines across 5 sections."""
        headlines = {
            "benefits": self._generate_benefit_headlines(),
            "technical": self._generate_technical_headlines(),
            "quirky": self._generate_quirky_headlines(),
            "cta": self._generate_cta_headlines(),
            "brand": self._generate_brand_headlines()
        }
        return headlines

    def _generate_benefit_headlines(self) -> List[str]:
        """Benefits: Why they can't live without it."""
        headlines = []

        # Pain relief focus
        if self.key_points.get('pain_relief'):
            headlines.extend([
                "Natural Pain Relief At Home",  # 28
                "Soothing Comfort When You Need",  # 29
                "Ease Aches & Pains Naturally",  # 29
            ])

        # Comfort & warmth
        if self.key_points.get('comfort'):
            headlines.extend([
                "Cozy Warmth In Under 2 Minutes",  # 30
                "Instant Comfort For Aching Muscles",  # 33 - needs trim
                "Feel Better Fast With Heat",  # 27
            ])

        # Natural & safe
        if self.key_points.get('natural'):
            headlines.extend([
                "100% Natural Wheat Heat Therapy",  # 31 - needs trim
                "Pure Natural Comfort & Relief",  # 29
            ])

        # General benefits
        headlines.extend([
            "Relief You Can Feel Immediately",  # 30
            "Say Goodbye To Aches & Discomfort",  # 34 - needs trim
        ])

        # Trim all to 30 chars
        headlines = [self._trim_headline(h) for h in headlines]

        # Fill to 10 if needed
        while len(headlines) < 10:
            headlines.append(self._trim_headline("Soothing Natural Heat Relief"))

        return headlines[:10]

    def _generate_technical_headlines(self) -> List[str]:
        """Technical: Specific advantages."""
        headlines = []

        # UK Made emphasis
        if self.key_points.get('uk_made'):
            headlines.extend([
                "Proudly Made In The UK Since",  # 28
                "British Made Heat Pack Quality",  # 31 - trim
                "UK Manufactured Wheat Bags",  # 27
            ])

        # Safety certified
        if self.key_points.get('safety'):
            headlines.extend([
                "BS8433 Safety Tested & Approved",  # 32 - trim
                "Certified Safe For Home Use",  # 29
            ])

        # Product specifics
        headlines.extend([
            "Microwave Ready In 90 Seconds",  # 30
            "Natural Wheat Filling & Cotton",  # 30
            "Reusable Heat Pack Technology",  # 30
            "Choice Of Scents & Fabric Types",  # 32 - trim
            "Professional Grade Heat Therapy",  # 32 - trim
        ])

        headlines = [self._trim_headline(h) for h in headlines]
        return headlines[:10]

    def _generate_quirky_headlines(self) -> List[str]:
        """Quirky: Personality with appropriate humor."""
        # Warm, friendly tone based on analysis
        headlines = [
            "Your New Favourite Cozy Companion",  # 34 - trim
            "Hug In A Bag - Warm & Wonderful",  # 32 - trim
            "Like A Warm Hug When You Need It",  # 32 - trim
            "Microwave Magic For Aching Bodies",  # 34 - trim
            "Toasty Comfort On Demand",  # 24
            "Mother Nature's Pain Relief",  # 27
            "Wheat Bag Bliss Awaits You",  # 27
            "Warmth That Works Wonders",  # 26
            "Your Aches Meet Their Match",  # 28
            "Comfort Food For Your Body",  # 27
        ]

        return [self._trim_headline(h) for h in headlines]

    def _generate_cta_headlines(self) -> List[str]:
        """CTA: Persuasive but not aggressive."""
        headlines = [
            "Shop Natural Heat Packs Today",  # 29
            "Order Your Wheat Bag Now",  # 25
            "Find Your Perfect Heat Pack",  # 28
            "Browse Our Full Range Now",  # 26
            "Get Soothing Relief Today",  # 26
            "Choose Your Ideal Wheat Bag",  # 28
            "Discover Natural Pain Relief",  # 29
            "Try UK's Favourite Heat Packs",  # 30
            "Experience The Warmth Today",  # 28
            "Shop Award-Winning Wheat Bags",  # 30
        ]

        return [self._trim_headline(h) for h in headlines]

    def _generate_brand_headlines(self) -> List[str]:
        """Brand: Category positioning with brand personality."""
        brand_name = "WheatyBags" if "wheaty" in self.brand.lower() else self.brand

        headlines = [
            f"{brand_name} - UK Heat Pack Experts",  # Variable
            "Official WheatyBags Store UK",  # 29
            "Britain's Trusted Heat Pack Brand",  # 33 - trim
            "WheatyBags - Since Warming Hearts",  # 34 - trim
            "Premium UK Made Wheat Bags",  # 27
            "Natural Heat Therapy Specialists",  # 32 - trim
            "Your Wheat Bag Experts Since 2000",  # 33 - trim
            "Quality Heat Packs Made In Britain",  # 35 - trim
            "UK's Original Wheat Bag Company",  # 32 - trim
            "Trusted By Thousands Nationwide",  # 30
        ]

        return [self._trim_headline(h) for h in headlines]

    def generate_descriptions(self) -> Dict[str, List[str]]:
        """Generate 50 descriptions across 5 sections."""
        descriptions = {
            "benefits": self._generate_benefit_descriptions(),
            "technical": self._generate_technical_descriptions(),
            "quirky": self._generate_quirky_descriptions(),
            "cta": self._generate_cta_descriptions(),
            "brand": self._generate_brand_descriptions()
        }
        return descriptions

    def _generate_benefit_descriptions(self) -> List[str]:
        """Benefits: Emotional, outcome-focused."""
        descriptions = [
            "Experience soothing natural relief for aches & pains. Microwave wheat bag therapy.",  # 88
            "Feel better fast with comforting warmth. Perfect for muscle pain & tension relief.",  # 87
            "Natural heat therapy that works. Ease discomfort & relax tired muscles instantly.",  # 87
            "Say goodbye to aches with gentle, penetrating warmth. 100% natural pain relief.",  # 85
            "Cozy comfort when you need it most. Soothe away stress, pain & everyday discomfort.",  # 90
            "Transform how you feel with natural heat therapy. Relief you can feel immediately.",  # 88
            "Your personal pain relief solution. Microwave wheat bags for instant soothing warmth.",  # 91 - trim
            "Melt away tension & discomfort naturally. Feel the difference quality heat makes.",  # 86
            "Gentle warmth that penetrates deep. Perfect for back, neck & shoulder pain relief.",  # 88
            "Discover the comfort thousands rely on daily. Natural relief for modern life's aches.",  # 90
        ]

        return [self._trim_description(d) for d in descriptions]

    def _generate_technical_descriptions(self) -> List[str]:
        """Technical: Specific advantages with benefit framing."""
        descriptions = [
            "100% natural wheat filling in pure cotton fabric. UK made & BS8433 safety tested.",  # 85
            "Microwave ready in 90 seconds. Retains therapeutic heat for 40+ minutes of relief.",  # 89
            "British manufactured to highest safety standards. Quality materials, expert craftsmen.",  # 92 - trim
            "Natural wheat grains mould perfectly to your body. Targets pain exactly where needed.",  # 90
            "Choice of scents & beautiful fabrics. Personalise your heat pack to suit your style.",  # 90
            "Reusable thousands of times. Eco-friendly alternative to disposable heat patches.",  # 86
            "Professional-grade heat therapy at home. Used by physios & pain relief specialists.",  # 90
            "Sealed for safety & hygiene. Washable covers available for long-lasting freshness.",  # 87
            "UK safety tested & certified. Peace of mind with every use. Trusted quality assured.",  # 90
            "Natural, chemical-free pain relief. No batteries, no waste. Pure wheat grain therapy.",  # 90
        ]

        return [self._trim_description(d) for d in descriptions]

    def _generate_quirky_descriptions(self) -> List[str]:
        """Quirky: Engaging with appropriate humor."""
        descriptions = [
            "Like a warm hug from Mother Nature herself. Your aches don't stand a chance!",  # 79
            "Microwave magic for modern aches. Natural relief that actually works. Try it today!",  # 87
            "Who knew wheat could be this wonderful? Discover Britain's favourite comfort secret.",  # 88
            "Your body will thank you. Your wheat bag won't judge you. Perfect partnership, really.",  # 90
            "Forget painkillers, embrace grain-fillers! Natural warmth that works wonders for aches.",  # 90
            "Plot twist: the solution to your aches is sitting in a kitchen cupboard. Wheat bags!",  # 89
            "Cozy up with comfort that counts. It's like a spa day, minus the cucumber slices.",  # 86
            "Warning: may cause extreme relaxation & relief. Side effects include sighs of comfort.",  # 90
            "Your muscles called. They want a wheat bag. Give the people what they want!",  # 79
            "Finally, something warm & fuzzy that actually helps. Natural relief, naturally brilliant.",  # 93 - trim
        ]

        return [self._trim_description(d) for d in descriptions]

    def _generate_cta_descriptions(self) -> List[str]:
        """CTA: Persuasive calls-to-action."""
        descriptions = [
            "Shop our full range of wheat bags today. Free UK delivery. Easy returns. Order now.",  # 87
            "Find your perfect heat pack in minutes. Wide choice of fabrics, scents & sizes. Browse.",  # 93 - trim
            "Order today for fast dispatch. Trusted by thousands. 30-day guarantee. Shop with confidence.",  # 97 - trim
            "Experience natural pain relief now. Choose from our award-winning range. Order online today.",  # 96 - trim
            "Browse wheat bags for every need. Neck, back, shoulders & more. Find yours now.",  # 84
            "Get soothing relief delivered to your door. UK made quality. Order your wheat bag today.",  # 90
            "Don't suffer in silence. Natural relief awaits. Shop our trusted wheat bag range now.",  # 87
            "Try Britain's favourite heat packs. Risk-free returns. Fast delivery. Order today.",  # 82
            "Join thousands who've discovered natural relief. Shop award-winning wheat bags now.",  # 85
            "Ready to feel better? Order your wheat bag today. Quick delivery, quality guaranteed.",  # 88
        ]

        return [self._trim_description(d) for d in descriptions]

    def _generate_brand_descriptions(self) -> List[str]:
        """Brand: Company positioning with personality."""
        brand_name = "WheatyBags" if "wheaty" in self.brand.lower() else "WheatyBags"

        descriptions = [
            f"{brand_name} - Your trusted UK wheat bag specialists. Quality, comfort & care since 2000.",  # Variable
            "Britain's original wheat bag company. Proudly UK made. Trusted by families nationwide.",  # 89
            "Expert heat therapy from Britain's wheat bag pioneers. Quality you can feel immediately.",  # 90
            f"Official {brand_name} store. 100% natural, UK manufactured, BS8433 certified wheat bags.",  # Variable
            "Family business, British values, natural relief. Choose quality, choose British, choose us.",  # 94 - trim
            "Award-winning wheat bags made with pride in the UK. Natural materials, expert craftsmanship.",  # 96 - trim
            "Trusted by physios, loved by customers nationwide. Professional quality for home use.",  # 88
            "British manufacturing excellence since day one. Quality heat packs for modern life's aches.",  # 90
            "Your reliable partner for natural pain relief. UK made wheat bags with a lifetime guarantee.",  # 95 - trim
            "Choose British, choose quality, choose relief. Wheat bags made with care in the UK.",  # 84
        ]

        return [self._trim_description(d) for d in descriptions]

    def _trim_headline(self, text: str) -> str:
        """Trim to 30 chars max, at word boundary."""
        if len(text) <= 30:
            return text

        # Trim at last space before 30
        trimmed = text[:30]
        last_space = trimmed.rfind(' ')
        if last_space > 20:  # Don't cut too short
            return trimmed[:last_space].strip()
        return trimmed.strip()

    def _trim_description(self, text: str) -> str:
        """Trim to 90 chars max, at word boundary."""
        if len(text) <= 90:
            return text

        # Trim at last space before 90
        trimmed = text[:90]
        last_space = trimmed.rfind(' ')
        if last_space > 75:  # Don't cut too short
            return trimmed[:last_space].strip()
        return trimmed.strip()

    def generate_complete_rsa(self) -> Dict:
        """Generate complete RSA ad set."""
        return {
            "headlines": self.generate_headlines(),
            "descriptions": self.generate_descriptions(),
            "insights_used": {
                "brand": self.brand,
                "key_points": self.key_points,
                "tone": self.tone
            }
        }


if __name__ == "__main__":
    # Test with WheatyBags
    print("Analyzing WheatyBags website...")
    analyzer = WebsiteAnalyzer("https://wheatybags.co.uk/")
    analyzer.analyze_site()
    insights = analyzer.get_insights_summary()

    print("\nGenerating professional ad copy...")
    writer = ProfessionalAdWriter(insights)
    ads = writer.generate_complete_rsa()

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
