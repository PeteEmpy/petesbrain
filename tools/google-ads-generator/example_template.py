#!/usr/bin/env python3
"""
Example Google Ads Text Assets Template
Demonstrates proper formatting for all 5 sections.
"""

from google_ads_generator import GoogleAdsAssetGenerator


def generate_example_assets():
    """Generate a complete example for a fictional product."""

    # Example: High-performance running shoes
    generator = GoogleAdsAssetGenerator(
        product_name="CloudRun Pro Running Shoes",
        brand="RunTech",
        website_url="https://www.example.com/cloudrun-pro"
    )

    # ========================================================================
    # SECTION 1: BENEFITS - Why they can't live without it
    # ========================================================================
    headlines_benefits = [
        "Run Faster, Feel Better",      # 23 chars
        "Transform Your Running Game",   # 27 chars
        "Maximum Comfort Every Mile",    # 26 chars
        "Run Like Never Before",         # 22 chars
        "Your Best Run Starts Here",     # 27 chars
        "Unstoppable Performance",       # 24 chars
        "Elevate Every Stride",          # 21 chars
        "Run Further Without Pain",      # 25 chars
        "Feel The Difference",           # 20 chars
        "Revolutionary Comfort Tech",    # 27 chars
    ]

    descriptions_benefits = [
        "Experience unmatched comfort with our cloud-foam technology. Run longer and recover faster.",  # 93 - need to trim
        "Revolutionary cushioning reduces impact by 40%. Your joints will thank you after every run.",  # 93 - need to trim
        "Lightweight design that won't slow you down. Feel like you're running on clouds.",  # 82 chars
        "Engineered for runners who demand the best. Maximum comfort meets peak performance.",  # 88 chars
        "Say goodbye to foot fatigue. Our advanced design keeps you comfortable mile after mile.",  # 91 - need to trim
        "Transform your training with shoes that work as hard as you do. Feel the difference.",  # 87 chars
        "Designed by runners, for runners. Experience the perfect balance of support and flexibility.",  # 97 - need to trim
        "Don't let discomfort hold you back. Run your best with shoes built for champions.",  # 84 chars
        "Your perfect run awaits. Premium comfort technology that adapts to your stride.",  # 83 chars
        "Break your personal records with footwear engineered for speed and endurance.",  # 81 chars
    ]

    # Trim descriptions to 90 chars
    descriptions_benefits = [
        "Experience unmatched comfort with cloud-foam tech. Run longer and recover faster.",  # 85 chars
        "Revolutionary cushioning reduces impact by 40%. Your joints will thank you.",  # 78 chars
        "Lightweight design that won't slow you down. Feel like you're running on clouds.",  # 84 chars
        "Engineered for runners who demand the best. Maximum comfort meets peak performance.",  # 88 chars
        "Say goodbye to foot fatigue. Advanced design keeps you comfortable mile after mile.",  # 87 chars
        "Transform your training with shoes that work as hard as you do. Feel the difference.",  # 89 chars
        "Designed by runners, for runners. Perfect balance of support and flexibility.",  # 81 chars
        "Don't let discomfort hold you back. Run your best with shoes built for champions.",  # 85 chars
        "Your perfect run awaits. Premium comfort technology that adapts to your stride.",  # 83 chars
        "Break personal records with footwear engineered for speed and endurance. Shop now.",  # 86 chars
    ]

    for h in headlines_benefits:
        generator.add_headline(h, "Benefits")
    for d in descriptions_benefits:
        generator.add_description(d, "Benefits")

    # ========================================================================
    # SECTION 2: TECHNICAL ADVANTAGES
    # ========================================================================
    headlines_technical = [
        "Advanced Carbon Plate Tech",    # 27 chars
        "40% More Energy Return",        # 23 chars
        "Breathable Mesh Upper",         # 22 chars
        "Waterproof & Lightweight",      # 25 chars
        "Anti-Slip Grip Technology",     # 26 chars
        "Shock-Absorbing Midsole",       # 24 chars
        "Engineered Knit Construction",  # 29 chars
        "Temperature-Regulating Fabric", # 30 chars
        "Responsive Foam System",        # 23 chars
        "Durable Outsole Design",        # 23 chars
    ]

    descriptions_technical = [
        "Carbon fiber plate provides explosive propulsion with every step. Tested by athletes.",  # 88 chars
        "Our proprietary foam returns 40% more energy than leading competitors. Feel the boost.",  # 90 chars
        "Engineered mesh keeps feet cool and dry even during intense workouts. Maximum airflow.",  # 90 chars
        "Waterproof membrane blocks moisture while remaining incredibly lightweight. All-weather.",  # 91 - trim
        "Advanced rubber compound delivers superior grip on wet and dry surfaces. Total control.",  # 90 chars
        "Triple-density midsole absorbs impact and reduces stress on joints. Run pain-free.",  # 86 chars
        "Seamless knit construction eliminates hotspots and provides custom-like fit. Premium.",  # 88 chars
        "Smart fabric adapts to your body temperature for optimal comfort in any conditions.",  # 87 chars
        "Responsive foam technology delivers energy return and cushioning exactly when you need it.",  # 94 - trim
        "Military-grade rubber outsole withstands 500+ miles of training. Built to last.",  # 84 chars
    ]

    descriptions_technical = [
        "Carbon fiber plate provides explosive propulsion with every step. Tested by athletes.",  # 88 chars
        "Our proprietary foam returns 40% more energy than leading competitors. Feel the boost.",  # 90 chars
        "Engineered mesh keeps feet cool and dry even during intense workouts. Maximum airflow.",  # 90 chars
        "Waterproof membrane blocks moisture while remaining lightweight. All-weather performance.",  # 90 chars
        "Advanced rubber compound delivers superior grip on wet and dry surfaces. Total control.",  # 90 chars
        "Triple-density midsole absorbs impact and reduces stress on joints. Run pain-free.",  # 86 chars
        "Seamless knit construction eliminates hotspots and provides custom-like fit. Premium.",  # 88 chars
        "Smart fabric adapts to your body temperature for optimal comfort in any conditions.",  # 87 chars
        "Responsive foam delivers energy return and cushioning exactly when you need it. Proven.",  # 90 chars
        "Military-grade rubber outsole withstands 500+ miles of training. Built to last.",  # 84 chars
    ]

    for h in headlines_technical:
        generator.add_headline(h, "Technical")
    for d in descriptions_technical:
        generator.add_description(d, "Technical")

    # ========================================================================
    # SECTION 3: QUIRKY / HUMOROUS
    # ========================================================================
    headlines_quirky = [
        "Shoes That Make You Smile",     # 27 chars
        "Your Feet Called. They're Happy", # 32 - too long, trim
        "Cloud Nine For Your Feet",      # 25 chars
        "Running Made Ridiculously Easy", # 31 - too long, trim
        "Like Butter, But For Running",  # 29 chars
        "Your New Secret Weapon",        # 24 chars
        "Fast Feet, Happy Heart",        # 23 chars
        "Basically Rocket Boosters",     # 27 chars
        "Where Comfort Meets Crazy Fast", # 31 - too long, trim
        "The Shoe Your Feet Deserve",    # 28 chars
    ]

    headlines_quirky = [
        "Shoes That Make You Smile",     # 27 chars
        "Your Feet's New Best Friend",   # 28 chars
        "Cloud Nine For Your Feet",      # 25 chars
        "Running Made Easy & Fun",       # 24 chars
        "Like Butter, But For Running",  # 29 chars
        "Your New Secret Weapon",        # 24 chars
        "Fast Feet, Happy Heart",        # 23 chars
        "Basically Rocket Boosters",     # 27 chars
        "Comfort Meets Crazy Fast",      # 25 chars
        "The Shoe Your Feet Deserve",    # 28 chars
    ]

    descriptions_quirky = [
        "Spoiler alert: Your old running shoes are about to get very jealous. Upgrade today.",  # 86 chars
        "Who knew clouds could be this fast? Experience the magic yourself. Free shipping.",  # 86 chars
        "Warning: May cause sudden urge to run everywhere. Side effects include happiness.",  # 86 chars
        "If shoes had feelings, these would be doing backflips right now. Your turn next.",  # 85 chars
        "Finally, shoes that understand you. It's like therapy, but for your feet. Try now.",  # 87 chars
        "Your morning run just went from 'ugh' to 'let's go!' in one shoe change. Game on.",  # 86 chars
        "Forget magic carpets. These shoes are your ticket to flying. (On the ground, legally.)",  # 91 - trim
        "The only thing faster? Your decision to buy them. Limited stock available now.",  # 82 chars
        "Coffee might wake you up, but these shoes will keep you going all day long.",  # 79 chars
        "Running shoes so good, they should probably come with a warning label. Try them.",  # 85 chars
    ]

    descriptions_quirky = [
        "Spoiler alert: Your old running shoes are about to get very jealous. Upgrade today.",  # 86 chars
        "Who knew clouds could be this fast? Experience the magic yourself. Free shipping.",  # 86 chars
        "Warning: May cause sudden urge to run everywhere. Side effects include happiness.",  # 86 chars
        "If shoes had feelings, these would be doing backflips right now. Your turn next.",  # 85 chars
        "Finally, shoes that understand you. Like therapy, but for your feet. Try now.",  # 81 chars
        "Your morning run just went from 'ugh' to 'let's go!' in one shoe change. Game on.",  # 86 chars
        "Forget magic carpets. These shoes are your ticket to flying. On the ground, legally.",  # 88 chars
        "The only thing faster? Your decision to buy them. Limited stock available now.",  # 82 chars
        "Coffee might wake you up, but these shoes will keep you going all day long.",  # 79 chars
        "Running shoes so good, they should come with a warning label. Try them now.",  # 79 chars
    ]

    for h in headlines_quirky:
        generator.add_headline(h, "Quirky")
    for d in descriptions_quirky:
        generator.add_description(d, "Quirky")

    # ========================================================================
    # SECTION 4: CALL TO ACTION
    # ========================================================================
    headlines_cta = [
        "Shop Now - Free Shipping",      # 25 chars
        "Order Today, Run Tomorrow",     # 26 chars
        "Limited Stock - Act Fast",      # 25 chars
        "Get Yours Today",               # 15 chars
        "Start Your Journey Now",        # 23 chars
        "Buy Now, Save 20%",             # 18 chars
        "Transform Your Run Today",      # 25 chars
        "Join 100K+ Happy Runners",      # 26 chars
        "Try Risk-Free For 30 Days",     # 26 chars
        "Upgrade Your Game Now",         # 22 chars
    ]

    descriptions_cta = [
        "Don't wait! Free shipping on all orders today. 30-day money-back guarantee included.",  # 87 chars
        "Join thousands of runners who've already made the switch. Order now and save 20%.",  # 85 chars
        "Limited time offer: Buy now and get free premium insoles worth £25. While stocks last.",  # 91 - trim
        "Experience the difference today. Fast delivery, easy returns, and lifetime support.",  # 87 chars
        "Ready to transform your running? Click to order now. Your best run starts today.",  # 85 chars
        "Shop now and discover why we're rated 5 stars by over 10,000 runners. Free shipping.",  # 89 chars
        "Take the first step towards better running. Order now with our 30-day guarantee.",  # 85 chars
        "Don't miss out on this game-changing technology. Buy today and feel the difference.",  # 87 chars
        "Your perfect running shoe is just one click away. Order now for next-day delivery.",  # 86 chars
        "Invest in your running future today. Premium quality at an accessible price. Shop now.",  # 90 chars
    ]

    descriptions_cta = [
        "Don't wait! Free shipping on all orders today. 30-day money-back guarantee included.",  # 87 chars
        "Join thousands of runners who've already made the switch. Order now and save 20%.",  # 85 chars
        "Limited offer: Buy now and get free premium insoles worth £25. While stocks last.",  # 85 chars
        "Experience the difference today. Fast delivery, easy returns, and lifetime support.",  # 87 chars
        "Ready to transform your running? Click to order now. Your best run starts today.",  # 85 chars
        "Shop now and discover why we're rated 5 stars by over 10,000 runners. Free shipping.",  # 89 chars
        "Take the first step towards better running. Order now with our 30-day guarantee.",  # 85 chars
        "Don't miss out on this game-changing technology. Buy today and feel the difference.",  # 87 chars
        "Your perfect running shoe is just one click away. Order now for next-day delivery.",  # 86 chars
        "Invest in your running future today. Premium quality at an accessible price. Shop now.",  # 90 chars
    ]

    for h in headlines_cta:
        generator.add_headline(h, "Call to Action")
    for d in descriptions_cta:
        generator.add_description(d, "Call to Action")

    # ========================================================================
    # SECTION 5: BRAND / CATEGORY DESCRIPTION
    # ========================================================================
    headlines_brand = [
        "RunTech CloudRun Pro",          # 21 chars
        "Premium Running Footwear",      # 25 chars
        "Official RunTech Store",        # 23 chars
        "Professional Running Shoes",    # 27 chars
        "CloudRun Pro Collection",       # 24 chars
        "RunTech Performance Range",     # 26 chars
        "Elite Running Technology",      # 25 chars
        "Trusted By Pro Athletes",       # 24 chars
        "Award-Winning Design",          # 21 chars
        "UK's #1 Running Shoe",          # 21 chars
    ]

    descriptions_brand = [
        "RunTech CloudRun Pro: The UK's best-selling premium running shoe. Trusted by athletes.",  # 89 chars
        "Discover the CloudRun Pro collection. Professional-grade running shoes for all levels.",  # 90 chars
        "RunTech has been engineering performance footwear for over 20 years. Quality guaranteed.",  # 92 - trim
        "Official CloudRun Pro range. Designed in London, tested by champions worldwide.",  # 83 chars
        "Premium running shoes combining cutting-edge technology with exceptional craftsmanship.",  # 90 chars
        "RunTech: Innovation in every stride. Award-winning running shoes trusted by thousands.",  # 90 chars
        "The CloudRun Pro series represents the pinnacle of running shoe technology. Shop now.",  # 88 chars
        "From casual joggers to marathon runners, RunTech delivers performance for everyone.",  # 87 chars
        "British-designed excellence. RunTech CloudRun Pro - where innovation meets the road.",  # 88 chars
        "Join the RunTech family. Premium performance running shoes with unmatched quality.",  # 86 chars
    ]

    descriptions_brand = [
        "RunTech CloudRun Pro: The UK's best-selling premium running shoe. Trusted by athletes.",  # 89 chars
        "Discover the CloudRun Pro collection. Professional-grade running shoes for all levels.",  # 90 chars
        "RunTech has engineered performance footwear for over 20 years. Quality guaranteed.",  # 85 chars
        "Official CloudRun Pro range. Designed in London, tested by champions worldwide.",  # 83 chars
        "Premium running shoes combining cutting-edge technology with exceptional craftsmanship.",  # 90 chars
        "RunTech: Innovation in every stride. Award-winning running shoes trusted by thousands.",  # 90 chars
        "The CloudRun Pro series represents the pinnacle of running shoe technology. Shop now.",  # 88 chars
        "From casual joggers to marathon runners, RunTech delivers performance for everyone.",  # 87 chars
        "British-designed excellence. RunTech CloudRun Pro - where innovation meets the road.",  # 88 chars
        "Join the RunTech family. Premium performance running shoes with unmatched quality.",  # 86 chars
    ]

    for h in headlines_brand:
        generator.add_headline(h, "Brand/Category")
    for d in descriptions_brand:
        generator.add_description(d, "Brand/Category")

    # ========================================================================
    # SITELINKS
    # ========================================================================
    sitelinks = [
        {
            "headline": "Shop Men's Range",
            "desc1": "Explore our full men's collection",
            "desc2": "Free shipping on all orders",
            "url": "https://www.example.com/mens"
        },
        {
            "headline": "Shop Women's Range",
            "desc1": "Discover women's running shoes",
            "desc2": "30-day returns guarantee",
            "url": "https://www.example.com/womens"
        },
        {
            "headline": "Size Guide",
            "desc1": "Find your perfect fit",
            "desc2": "Expert fitting advice available",
            "url": "https://www.example.com/size-guide"
        },
        {
            "headline": "Customer Reviews",
            "desc1": "See what runners are saying",
            "desc2": "5-star rated by 10,000+ customers",
            "url": "https://www.example.com/reviews"
        },
        {
            "headline": "Technology Explained",
            "desc1": "Learn about our innovations",
            "desc2": "See the science behind comfort",
            "url": "https://www.example.com/technology"
        }
    ]

    for sl in sitelinks:
        generator.add_sitelink(sl["headline"], sl["desc1"], sl["desc2"], sl["url"])

    # ========================================================================
    # CALLOUT EXTENSIONS
    # ========================================================================
    callouts = [
        "Free UK Shipping",
        "30-Day Returns",
        "Lifetime Support",
        "Eco-Friendly Materials",
        "5-Star Rated"
    ]

    for callout in callouts:
        generator.add_callout(callout)

    # ========================================================================
    # SEARCH THEMES (for Performance Max)
    # ========================================================================
    search_themes = [
        "premium running shoes",
        "best running shoes uk",
        "comfortable running trainers",
        "professional running footwear",
        "running shoes for marathon",
        "lightweight running shoes",
        "cushioned running shoes",
        "breathable running trainers",
        "carbon plate running shoes",
        "energy return running shoes",
        "long distance running shoes",
        "training shoes for runners",
        "performance running footwear",
        "running shoes with support",
        "shock absorbing running shoes",
        "waterproof running trainers",
        "running shoes for beginners",
        "advanced running technology",
        "running shoes online",
        "buy running shoes uk",
        "men's running shoes",
        "women's running shoes",
        "neutral running shoes",
        "stability running shoes",
        "trail running shoes",
        "road running shoes",
        "racing running shoes",
        "tempo running shoes",
        "daily training shoes",
        "running shoes sale",
        "best cushioned running shoes",
        "running shoes for flat feet",
        "running shoes for high arches",
        "wide fit running shoes",
        "narrow running shoes",
        "vegan running shoes",
        "sustainable running footwear",
        "running shoes free shipping",
        "running trainers next day delivery",
        "running shoes with warranty",
        "professional athlete running shoes",
        "competition running shoes",
        "running shoes for speed",
        "running shoes for comfort",
        "injury prevention running shoes",
        "running shoes for recovery",
        "best rated running shoes",
        "top running shoes 2024",
        "award winning running shoes",
        "innovative running technology"
    ]

    for theme in search_themes:
        generator.add_search_theme(theme)

    return generator


if __name__ == "__main__":
    print("Generating example Google Ads assets...\n")
    generator = generate_example_assets()

    # Display output
    output = generator.generate_output()
    print(output)

    # Save files
    with open("example_google_ads_assets.txt", "w") as f:
        f.write(output)
    print("\n✅ Example saved to: example_google_ads_assets.txt")

    csv_output = generator.export_csv()
    with open("example_google_ads_assets.csv", "w") as f:
        f.write(csv_output)
    print("✅ CSV saved to: example_google_ads_assets.csv")
