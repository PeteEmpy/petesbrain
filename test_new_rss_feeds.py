#!/usr/bin/env python3
"""
Test script to verify new RSS feeds are valid
"""

import feedparser
import sys

# New feeds to test
NEW_FEEDS = {
    # Google Ads Authorities
    "Adalysis - Brad Geddes": "https://adalysis.com/blog/feed/",
    "Optmyzr - Frederick Vallaeys": "https://www.optmyzr.com/blog/feed/",
    "ZATO Marketing - Kirk Williams": "https://www.zatomarketing.com/blog-feed.xml",

    # Meta Authorities
    "Andrew Foxwell": "https://www.andrewfoxwell.com/feed/",
    "Depesh Mandalia": "https://www.depeshm.com/feed/",
}

def test_feed(name, url):
    """Test a single RSS feed"""
    print(f"\nTesting: {name}")
    print(f"URL: {url}")

    try:
        feed = feedparser.parse(url)

        if feed.bozo:
            print(f"  ❌ PARSE ERROR: {feed.bozo_exception}")
            return False

        if not feed.entries:
            print(f"  ⚠️  WARNING: No entries found")
            return False

        print(f"  ✅ SUCCESS: {len(feed.entries)} entries found")

        # Show first entry as sample
        if feed.entries:
            first = feed.entries[0]
            print(f"  📄 Sample: {first.title[:60]}...")
            if hasattr(first, 'published'):
                print(f"  📅 Published: {first.published}")

        return True

    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        return False

def main():
    print("=" * 70)
    print("RSS FEED VALIDATION TEST")
    print("=" * 70)

    results = {}

    for name, url in NEW_FEEDS.items():
        results[name] = test_feed(name, url)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in results.values() if r)
    failed = len(results) - passed

    print(f"\n✅ Passed: {passed}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")

    if failed > 0:
        print("\nFailed feeds:")
        for name, success in results.items():
            if not success:
                print(f"  - {name}")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
