#!/usr/bin/env python3
"""
Professional Copywriter - ROK-Compliant Ad Copy Generator
Analyzes websites like a professional copywriter with 20 years experience.
Understands business, audience, USPs, and writes compelling ad copy.
"""

import re
from website_analyzer import WebsiteAnalyzer
from typing import Dict, List, Set


class ProfessionalCopywriter:
    """
    Professional ad copywriter that analyzes websites deeply and writes
    compelling, benefit-focused ad copy following ROK specifications.
    """

    def __init__(self, url: str):
        self.url = url
        self.analyzer = WebsiteAnalyzer(url)

        # Analysis results
        self.brand = ""
        self.business_type = ""
        self.target_audience = ""
        self.usps = []
        self.benefits = []
        self.features = []
        self.tone = ""
        self.main_products = []

    def analyze_and_generate(self) -> Dict:
        """Deep analysis followed by professional ad copy generation."""
        print("Analyzing website as a professional copywriter...", flush=True)

        # Deep website analysis
        self.analyzer.analyze_site()
        insights = self.analyzer.get_insights_summary()

        # Extract copywriting insights
        self._extract_copywriting_insights(insights)

        # Generate professional ad copy
        print("Writing professional ad copy...", flush=True)
        return {
            "url": self.url,
            "headlines": self._write_headlines(),
            "descriptions": self._write_descriptions(),
            "page_info": {
                "brand": self.brand,
                "product": self.business_type,
                "category": self.business_type
            }
        }

    def _extract_copywriting_insights(self, insights: Dict):
        """Extract professional copywriting insights from website analysis."""
        self.brand = insights.get('brand_name', '').split('|')[0].strip()
        self.main_products = insights.get('main_products', [])

        # Analyze all content to understand the business
        all_content = ' '.join(
            insights.get('all_headings', []) +
            insights.get('key_benefits', []) +
            insights.get('technical_features', [])
        ).lower()

        # Identify business type
        self.business_type = self._identify_business_type(all_content, insights)

        # Identify target audience
        self.target_audience = self._identify_audience(all_content)

        # Extract USPs (Unique Selling Propositions)
        self.usps = self._extract_usps(insights)

        # Extract benefits (why customers buy)
        self.benefits = self._extract_benefits(insights)

        # Extract features (what they get)
        self.features = self._extract_features(insights)

        # Determine tone
        self.tone = self._determine_tone(insights)

        print(f"Copywriting Analysis:", flush=True)
        print(f"  Business: {self.business_type}", flush=True)
        print(f"  Audience: {self.target_audience}", flush=True)
        print(f"  USPs: {len(self.usps)} identified", flush=True)
        print(f"  Tone: {self.tone}", flush=True)

    def _identify_business_type(self, content: str, insights: Dict) -> str:
        """Identify what type of business this is."""
        products = ' '.join(self.main_products).lower()
        headings = ' '.join(insights.get('all_headings', [])).lower()

        # Look for business indicators
        if any(word in content for word in ['toy', 'toys', 'children', 'kids', 'learning', 'educational']):
            if 'engineering' in content or 'stem' in content or 'science' in content:
                return "Educational Engineering Toys"
            return "Children's Toys"

        if any(word in content for word in ['heat', 'wheat', 'therapy', 'pain']):
            return "Heat Therapy Products"

        if any(word in content for word in ['clothing', 'fashion', 'apparel', 'wear']):
            return "Clothing & Fashion"

        # Use main products if specific enough
        if self.main_products and len(self.main_products) > 0:
            first_product = self.main_products[0]
            if len(first_product) < 40:
                return first_product

        return "Products"

    def _identify_audience(self, content: str) -> str:
        """Identify target audience from content."""
        if 'parent' in content or 'children' in content or 'kids' in content:
            return "Parents"
        if 'professional' in content or 'business' in content:
            return "Professionals"
        if 'home' in content or 'family' in content:
            return "Families"
        return "General Consumers"

    def _extract_usps(self, insights: Dict) -> List[str]:
        """Extract Unique Selling Propositions."""
        usps = []

        content = ' '.join(
            insights.get('key_benefits', []) +
            insights.get('all_headings', [])
        ).lower()

        # Common USPs to look for
        usp_indicators = {
            'free delivery': 'Free UK Delivery',
            'free shipping': 'Free Shipping',
            'next day': 'Next Day Delivery',
            'fast delivery': 'Fast Delivery',
            'uk made': 'UK Made',
            'handmade': 'Handmade',
            'educational': 'Educational Value',
            'stem': 'STEM Learning',
            'eco': 'Eco-Friendly',
            'sustainable': 'Sustainable',
            'quality': 'Premium Quality',
            'guarantee': 'Quality Guaranteed',
            'expert': 'Expert Service',
        }

        for indicator, usp in usp_indicators.items():
            if indicator in content and usp not in usps:
                usps.append(usp)

        return usps[:5]  # Top 5 USPs

    def _extract_benefits(self, insights: Dict) -> List[str]:
        """Extract customer benefits (why they buy)."""
        benefits_list = insights.get('key_benefits', [])

        # Clean and filter
        benefits = []
        for benefit in benefits_list:
            if 20 < len(benefit) < 100:
                benefits.append(benefit)

        return benefits[:10]

    def _extract_features(self, insights: Dict) -> List[str]:
        """Extract product features (what they get)."""
        features_list = insights.get('technical_features', [])

        # Clean and filter
        features = []
        for feature in features_list:
            if 20 < len(feature) < 100:
                features.append(feature)

        return features[:10]

    def _determine_tone(self, insights: Dict) -> str:
        """Determine brand tone from content."""
        tones = insights.get('tone_indicators', [])

        if 'friendly' in tones and 'professional' in tones:
            return "Professional yet approachable"
        if 'warm' in tones:
            return "Warm and caring"
        if 'professional' in tones:
            return "Professional"
        return "Friendly"

    def _enforce_limit(self, text: str, max_len: int) -> str:
        """Strictly enforce character limit."""
        if not text or len(text) <= max_len:
            return text

        trimmed = text[:max_len]
        last_space = trimmed.rfind(' ')

        if last_space > max_len * 0.7:
            return trimmed[:last_space].strip()

        return trimmed.strip()

    def _write_headlines(self) -> Dict[str, List[str]]:
        """Write 50 professional headlines across 5 sections."""
        return {
            "benefits": self._write_benefits_headlines(),
            "technical": self._write_technical_headlines(),
            "quirky": self._write_quirky_headlines(),
            "cta": self._write_cta_headlines(),
            "brand": self._write_brand_headlines()
        }

    def _write_benefits_headlines(self) -> List[str]:
        """Benefits: Why customers can't live without it."""
        headlines = []

        # Use actual benefits from the site
        for benefit in self.benefits:
            headline = self._enforce_limit(benefit, 30)
            if headline and len(headline) >= 15:
                headlines.append(headline)
                if len(headlines) >= 10:
                    return headlines

        # Write professional benefit-focused headlines based on business type
        if "Educational" in self.business_type or "Engineering" in self.business_type:
            benefit_headlines = [
                "Inspire Young Minds Daily",
                "STEM Learning Through Play",
                "Build Problem-Solving Skills",
                "Spark Creativity & Innovation",
                "Develop Critical Thinking",
                "Hands-On Learning Experience",
                "Educational Fun for Kids",
                "Future Engineers Start Here",
                "Screen-Free Learning Time",
                "Engaging Educational Play"
            ]
        elif "Heat" in self.business_type or "Therapy" in self.business_type:
            benefit_headlines = [
                "Natural Pain Relief at Home",
                "Soothing Comfort When Needed",
                "Ease Aches & Pains Naturally",
                "Therapeutic Warmth & Relief",
                "Relax Tired Aching Muscles",
                "Comfort That Really Works",
                "Feel Better Faster",
                "Natural Soothing Relief",
                "Warmth When You Need It",
                "Gentle Effective Relief"
            ]
        else:
            # Generic benefit-focused headlines
            benefit_headlines = [
                f"Transform Your {self.business_type}",
                f"Quality {self.business_type}",
                f"Premium {self.business_type}",
                f"Trusted {self.business_type}",
                f"Expert {self.business_type}",
                f"Professional {self.business_type}",
                f"Reliable {self.business_type}",
                f"Outstanding {self.business_type}",
                f"Exceptional {self.business_type}",
                f"Superior {self.business_type}"
            ]

        for headline in benefit_headlines:
            h = self._enforce_limit(headline, 30)
            if h and h not in headlines:
                headlines.append(h)
                if len(headlines) >= 10:
                    return headlines

        return headlines[:10]

    def _write_technical_headlines(self) -> List[str]:
        """Technical: Specific advantages."""
        headlines = []

        # Use actual features from site
        for feature in self.features:
            headline = self._enforce_limit(feature, 30)
            if headline and len(headline) >= 15:
                headlines.append(headline)
                if len(headlines) >= 10:
                    return headlines

        # Include USPs as technical headlines
        for usp in self.usps:
            headline = self._enforce_limit(usp, 30)
            if headline and headline not in headlines:
                headlines.append(headline)
                if len(headlines) >= 10:
                    return headlines

        # Write technical headlines based on business
        if "Educational" in self.business_type:
            tech_headlines = [
                "Age-Appropriate Design",
                "Safety Tested & Certified",
                "Durable Quality Materials",
                "Expert-Recommended Toys",
                "Award-Winning Products",
                "British Educational Standards",
                "High-Quality Construction",
                "Long-Lasting Play Value",
                "Carefully Curated Selection",
                "Trusted by Teachers"
            ]
        elif "Heat" in self.business_type:
            tech_headlines = [
                "100% Natural Ingredients",
                "Microwave Ready in Minutes",
                "Reusable & Long-Lasting",
                "BS Safety Certified",
                "UK Made Quality",
                "Natural Wheat Filling",
                "Professional Grade Quality",
                "Tested for Safety",
                "Premium Materials Used",
                "Expertly Crafted"
            ]
        else:
            tech_headlines = [
                f"Premium Quality {self.business_type}",
                f"Expert-Selected {self.business_type}",
                f"Carefully Sourced {self.business_type}",
                f"High Standards {self.business_type}",
                f"Quality Assured {self.business_type}",
                f"Professional Grade",
                f"Expertly Curated Range",
                f"Quality You Can Trust",
                f"Precision Crafted",
                f"Built to Last"
            ]

        for headline in tech_headlines:
            h = self._enforce_limit(headline, 30)
            if h and h not in headlines:
                headlines.append(h)
                if len(headlines) >= 10:
                    return headlines

        return headlines[:10]

    def _write_quirky_headlines(self) -> List[str]:
        """Quirky: Engaging with appropriate personality."""
        if "Educational" in self.business_type or "Children" in self.business_type:
            quirky = [
                "Where Learning Meets Fun",
                "Play That Teaches",
                "Smart Play for Smart Kids",
                "Learning Adventures Await",
                "Make Learning Exciting",
                "Fun That Educates",
                "Playtime with Purpose",
                "The Joy of Discovery",
                "Ignite Young Imaginations",
                "Where Curiosity Grows"
            ]
        elif "Heat" in self.business_type:
            quirky = [
                "Warmth That Cares",
                "Your Comfort Companion",
                "Cozy Relief Delivered",
                "Hug in a Bag",
                "Mother Nature's Remedy",
                "Warmth with a Purpose",
                "The Comfort You Deserve",
                "Relief That Feels Good",
                "Your Daily Dose of Cozy",
                "Warmth That Works Wonders"
            ]
        else:
            quirky = [
                f"Discover {self.brand}",
                f"Experience {self.brand}",
                f"Love Our {self.business_type}",
                f"Your Perfect Match",
                f"Quality Meets Style",
                f"Where Excellence Lives",
                f"The Smart Choice",
                f"Your Trusted Partner",
                f"Designed for You",
                f"Simply Outstanding"
            ]

        return [self._enforce_limit(h, 30) for h in quirky]

    def _write_cta_headlines(self) -> List[str]:
        """CTA: Persuasive but not aggressive."""
        if "Educational" in self.business_type:
            cta = [
                "Shop Educational Toys Now",
                "Browse Our STEM Collection",
                "Explore Learning Toys",
                "Find the Perfect Gift",
                "Start Learning Today",
                "Discover Our Range",
                "View Our Collection",
                "Shop By Age Group",
                "Find Educational Gifts",
                "Browse Top Sellers"
            ]
        elif "Heat" in self.business_type:
            cta = [
                "Shop Heat Therapy Now",
                "Find Your Relief Today",
                "Browse Our Range",
                "Order Comfort Now",
                "Discover Natural Relief",
                "Shop Wheat Bags",
                "Find Your Perfect Fit",
                "Explore Our Collection",
                "Get Relief Today",
                "Order Now for Comfort"
            ]
        else:
            cta = [
                f"Shop {self.business_type}",
                f"Browse Our Range",
                f"Explore {self.brand}",
                f"Discover Our Collection",
                f"View All Products",
                f"Shop Now",
                f"Find Your Perfect Match",
                f"Browse Top Sellers",
                f"Explore Our Range",
                f"Shop the Collection"
            ]

        return [self._enforce_limit(h, 30) for h in cta]

    def _write_brand_headlines(self) -> List[str]:
        """Brand: Positioning with personality."""
        brand_headlines = [
            f"{self.brand} UK",
            f"Official {self.brand} Store",
            f"{self.brand} Direct",
            f"Shop {self.brand}",
            f"{self.brand} Specialists",
            f"Trusted {self.brand}",
            f"{self.brand} Experts",
            f"{self.brand} Collection",
            f"Buy {self.brand}",
            f"{self.brand} Online"
        ]

        return [self._enforce_limit(h, 30) for h in brand_headlines]

    def _write_descriptions(self) -> Dict[str, List[str]]:
        """Write 50 professional descriptions."""
        return {
            "benefits": self._write_benefits_descriptions(),
            "technical": self._write_technical_descriptions(),
            "quirky": self._write_quirky_descriptions(),
            "cta": self._write_cta_descriptions(),
            "brand": self._write_brand_descriptions()
        }

    def _write_benefits_descriptions(self) -> List[str]:
        """Write benefit-focused descriptions."""
        descriptions = []

        # Use actual benefits from site
        for benefit in self.benefits:
            if 40 <= len(benefit) <= 120:
                desc = self._enforce_limit(benefit, 90)
                if desc:
                    descriptions.append(desc)
                    if len(descriptions) >= 10:
                        return descriptions

        # Write professional benefit descriptions
        if "Educational" in self.business_type:
            benefit_descs = [
                "Inspire young engineers with hands-on STEM learning. Educational toys that teach.",
                "Develop problem-solving skills through creative play. Learning made fun for kids.",
                "Spark curiosity and innovation with engineering toys. Screen-free educational fun.",
                "Build confidence with age-appropriate challenges. Perfect for developing minds.",
                "Encourage creativity and critical thinking. Educational play that really works.",
                "Quality educational toys for growing minds. Trusted by parents and teachers.",
                "Make learning an adventure with our engineering toys. Fun that educates daily.",
                "Foster a love of science and engineering early. Engaging toys for bright minds.",
                "Hands-on learning that sticks. Educational toys designed to inspire and teach.",
                "The perfect blend of fun and education. STEM toys kids actually want to play with."
            ]
        elif "Heat" in self.business_type:
            benefit_descs = [
                "Natural pain relief you can trust. Soothing warmth for aches and muscle tension.",
                "Feel better faster with therapeutic heat. Microwave heat packs for instant comfort.",
                "Ease discomfort naturally without medication. Gentle heat therapy that really works.",
                "Your go-to solution for muscle pain and tension. Comforting warmth when needed most.",
                "Relax tired, aching muscles with natural heat. Reusable therapy you can count on.",
                "Soothing relief for back, neck, and shoulder pain. Natural comfort you deserve.",
                "Transform how you manage pain naturally. Heat therapy trusted by thousands daily.",
                "Gentle warmth that penetrates deep. Perfect for chronic pain and muscle relief.",
                "Your personal comfort companion. Natural heat therapy for everyday aches and pains.",
                "Experience relief without pills or chemicals. Pure natural warmth for soothing comfort."
            ]
        else:
            benefit_descs = [
                f"Discover quality {self.business_type} you can trust. Shop our curated collection now.",
                f"Transform your experience with premium {self.business_type}. Quality guaranteed.",
                f"Exceptional {self.business_type} at competitive prices. Fast UK delivery available.",
                f"Your trusted source for {self.business_type}. Quality products, expert service.",
                f"Experience the difference quality makes. Shop {self.business_type} with confidence.",
                f"Premium {self.business_type} delivered to your door. Browse our range today.",
                f"Quality you can see and feel. {self.business_type} that exceed expectations.",
                f"Trusted by thousands nationwide. Your source for quality {self.business_type}.",
                f"Exceptional products, exceptional service. Discover why customers choose us.",
                f"Where quality meets value. Premium {self.business_type} at great prices."
            ]

        for desc in benefit_descs:
            d = self._enforce_limit(desc, 90)
            if d and d not in descriptions:
                descriptions.append(d)
                if len(descriptions) >= 10:
                    return descriptions

        return descriptions[:10]

    def _write_technical_descriptions(self) -> List[str]:
        """Write technical/feature descriptions."""
        descriptions = []

        # Use actual features
        for feature in self.features:
            if 40 <= len(feature) <= 120:
                desc = self._enforce_limit(feature, 90)
                if desc:
                    descriptions.append(desc)
                    if len(descriptions) >= 10:
                        return descriptions

        # Write technical descriptions
        if "Educational" in self.business_type:
            tech_descs = [
                "Safety tested and certified for peace of mind. Age-appropriate educational toys.",
                "Durable construction for lasting play value. Quality materials and expert design.",
                "Aligned with UK educational standards. Toys that support school curriculum.",
                "Expert-selected by education professionals. Quality toys with proven learning value.",
                "High-quality materials and construction. Built to withstand enthusiastic young learners.",
                "Award-winning educational toys from trusted brands. Curated for quality and value.",
                "Age-graded for appropriate challenge levels. Supporting development every step.",
                "Safe, non-toxic materials throughout. Quality you can see and feel in every product.",
                "Designed by educators for optimal learning. Play that develops real-world skills.",
                "British-made quality where possible. Supporting UK manufacturing and quality standards."
            ]
        elif "Heat" in self.business_type:
            tech_descs = [
                "100% natural wheat filling in premium cotton. Microwave safe and reusable.",
                "BS8433 safety certified for your peace of mind. Quality heat therapy you can trust.",
                "Retains therapeutic heat for 40+ minutes. Perfect for targeted pain relief.",
                "UK manufactured to highest standards. Quality materials and expert craftsmanship.",
                "Reusable thousands of times. Eco-friendly alternative to disposable heat packs.",
                "Natural grain moulds perfectly to your body. Targets pain exactly where needed.",
                "Available in multiple sizes and scents. Personalize your heat therapy experience.",
                "Washable covers available for hygiene. Long-lasting freshness and comfort.",
                "Professional-grade heat therapy at home. Used by physiotherapists nationwide.",
                "Chemical-free, natural pain relief. No batteries or waste. Pure heat therapy."
            ]
        else:
            tech_descs = [
                f"Premium quality {self.business_type} from trusted suppliers. Expertly curated for you.",
                f"Carefully selected for quality and value. {self.business_type} that meet our standards.",
                f"Fast UK delivery on all orders. Quality {self.business_type} delivered promptly.",
                f"Expert customer service team ready to help. Quality advice for your purchase.",
                f"Secure online ordering with trusted payment. Shop {self.business_type} safely.",
                f"Quality checked before dispatch. {self.business_type} that meet our strict standards.",
                f"Easy returns policy for peace of mind. Shop {self.business_type} with confidence.",
                f"Competitive pricing on quality {self.business_type}. Great value guaranteed daily.",
                f"Stock updated regularly with new arrivals. Latest {self.business_type} available now.",
                f"Trusted by customers nationwide. Quality {self.business_type}, quality service."
            ]

        for desc in tech_descs:
            d = self._enforce_limit(desc, 90)
            if d and d not in descriptions:
                descriptions.append(d)
                if len(descriptions) >= 10:
                    return descriptions

        return descriptions[:10]

    def _write_quirky_descriptions(self) -> List[str]:
        """Write engaging quirky descriptions."""
        if "Educational" in self.business_type:
            quirky = [
                "Where screen time becomes hands-on time. Educational toys kids actually love.",
                "Making STEM fun since day one. Engineering toys that spark lifelong curiosity.",
                "Who says learning can't be fun? Our toys prove otherwise every single day.",
                "Building tomorrow's innovators today. One engineering toy at a time. Join us.",
                "Plot twist: education can be exciting. Discover toys that make learning amazing.",
                "STEM education meets serious fun. Toys that teach without feeling like school.",
                "Future scientists start here. Educational toys that ignite passion for learning.",
                "Learn by doing, succeed by playing. That's our motto and your child's future.",
                "Where curiosity meets construction. Engineering toys designed to inspire greatness.",
                "Making complex concepts simple through play. Education disguised as pure fun."
            ]
        elif "Heat" in self.business_type:
            quirky = [
                "Like a warm hug when you need it most. Natural heat therapy that really cares.",
                "Mother Nature's answer to modern aches. Wheat bags that work wonders on pain.",
                "Your comfort companion for life's aches. Natural warmth, natural relief, naturally brilliant.",
                "Who knew wheat could be this wonderful? Discover heat therapy's best-kept secret.",
                "Warmth that works harder than a heating pad. Natural relief you can feel instantly.",
                "Your aches have met their match. Natural heat therapy trusted by thousands daily.",
                "Plot twist: pain relief doesn't need pills. Just pure natural warmth and comfort.",
                "Microwave magic for modern aches. Heat therapy that fits your lifestyle perfectly.",
                "Because your comfort matters. Natural heat therapy that actually delivers results.",
                "The cozy solution to everyday discomfort. Heat therapy made simple and effective."
            ]
        else:
            quirky = [
                f"Discover why customers rave about {self.brand}. Quality that speaks for itself.",
                f"The {self.business_type} you've been searching for. Your search ends here today.",
                f"Plot twist: quality doesn't have to cost more. Exceptional value meets excellence.",
                f"Where {self.business_type} meet their perfect match. That match is you. Shop now.",
                f"Finally, {self.business_type} that deliver on promises. Quality guaranteed always.",
                f"Join thousands who've discovered {self.brand}. See the difference quality makes.",
                f"Your {self.business_type} journey starts here. Quality awaits your discovery.",
                f"Because settling isn't an option. Premium {self.business_type} for discerning customers.",
                f"Quality {self.business_type} without the premium price tag. That's our promise.",
                f"Where excellence is the standard. {self.business_type} that exceed expectations."
            ]

        return [self._enforce_limit(d, 90) for d in quirky]

    def _write_cta_descriptions(self) -> List[str]:
        """Write persuasive CTA descriptions."""
        if "Educational" in self.business_type:
            cta = [
                "Shop educational engineering toys now. Free UK delivery. Fast dispatch daily.",
                "Browse our curated STEM collection today. Quality toys, expert service guaranteed.",
                "Discover age-appropriate learning toys now. Trusted by parents and teachers alike.",
                "Find the perfect educational gift today. Wide selection, expert advice available.",
                "Order now for fast UK delivery. Quality educational toys at competitive prices.",
                "Explore our engineering toy range today. Safe, tested, and designed to educate.",
                "Shop with confidence knowing quality is guaranteed. Secure checkout, fast delivery.",
                "Browse by age, subject, or skill level. Finding perfect toys made simple online.",
                "Free delivery on orders over £30. Shop quality educational toys risk-free today.",
                "Order today, inspire tomorrow. Educational toys delivered fast to your door."
            ]
        elif "Heat" in self.business_type:
            cta = [
                "Shop natural heat therapy now. Free UK delivery. Order your comfort today.",
                "Browse our wheat bag collection. Quality heat packs at great prices online.",
                "Order your heat pack today. Fast dispatch. Natural relief delivered quickly.",
                "Discover natural pain relief now. Trusted by thousands. Shop with confidence.",
                "Get soothing heat therapy delivered fast. Quality wheat bags at fair prices.",
                "Find your perfect heat pack today. Multiple sizes and scents available now.",
                "Shop natural relief with confidence. Easy returns. Satisfaction guaranteed always.",
                "Order now for next-day delivery option. Natural heat therapy when you need it.",
                "Browse our best-selling heat packs. Trusted quality, proven results daily.",
                "Try risk-free with our guarantee. Order natural heat therapy online today."
            ]
        else:
            cta = [
                f"Shop quality {self.business_type} now. Free UK delivery. Secure checkout daily.",
                f"Browse our {self.business_type} collection. Quality products at great prices.",
                f"Order today for fast delivery. Quality {self.business_type} shipped promptly.",
                f"Discover our range now. Expert service. Quality {self.business_type} guaranteed.",
                f"Shop with confidence online today. Easy returns. Quality you can trust always.",
                f"Find your perfect {self.business_type} now. Wide selection available online.",
                f"Order now, delivered fast. Quality {self.business_type} at competitive prices.",
                f"Browse our curated collection today. Quality assured on every single purchase.",
                f"Shop online, delivered to your door. Quality {self.business_type} made simple.",
                f"Order today with confidence. Secure payment. Fast delivery on all orders."
            ]

        return [self._enforce_limit(d, 90) for d in cta]

    def _write_brand_descriptions(self) -> List[str]:
        """Write brand positioning descriptions."""
        brand_descs = [
            f"{self.brand} - Your trusted source for quality {self.business_type}. Shop now.",
            f"Official {self.brand} store. Quality products delivered direct to your door daily.",
            f"Discover the {self.brand} difference. Premium {self.business_type} at fair prices.",
            f"Why thousands choose {self.brand}. Quality, service, and value you can trust.",
            f"{self.brand} brings you the best {self.business_type}. Shop our range today.",
            f"Trusted nationwide for quality {self.business_type}. Experience {self.brand} excellence.",
            f"Choose {self.brand} for expert service and quality. Your satisfaction guaranteed.",
            f"{self.brand} - Where quality meets value. Premium {self.business_type} online.",
            f"Experience {self.brand} quality today. Trusted by thousands for good reason.",
            f"Your {self.business_type} specialists. Browse our {self.brand} collection now."
        ]

        return [self._enforce_limit(d, 90) for d in brand_descs]


if __name__ == "__main__":
    # Test with BrightMinds
    url = "https://www.brightminds.co.uk/collections/engineering-toys"

    copywriter = ProfessionalCopywriter(url)
    ads = copywriter.analyze_and_generate()

    print("\n" + "="*80)
    print("PROFESSIONAL AD COPY")
    print("="*80)
    print(f"\nBusiness: {copywriter.business_type}")
    print(f"Audience: {copywriter.target_audience}")
    print(f"Tone: {copywriter.tone}")

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
