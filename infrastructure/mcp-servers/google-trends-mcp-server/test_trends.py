#!/usr/bin/env python3
"""
Test script for Google Trends MCP Server
Run this to verify the server works correctly
"""

from pytrends.request import TrendReq
import json


def test_interest_over_time():
    """Test getting interest over time"""
    print("\n=== Testing Interest Over Time ===")

    pytrends = TrendReq(hl='en-GB', tz=0)
    keywords = ["christmas trees", "artificial christmas trees"]

    pytrends.build_payload(keywords, timeframe='today 3-m', geo='GB')
    df = pytrends.interest_over_time()

    if df.empty:
        print("❌ No data returned")
        return False

    print(f"✅ Retrieved {len(df)} data points")
    print(f"   Keywords: {', '.join(keywords)}")
    print(f"   Date range: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")

    # Show last 5 rows
    print("\nLast 5 data points:")
    for keyword in keywords:
        if keyword in df.columns:
            recent = df[keyword].tail()
            values = ', '.join([str(int(v)) for v in recent])
            print(f"   {keyword}: {values}")

    return True


def test_interest_by_region():
    """Test getting interest by region"""
    print("\n=== Testing Interest By Region ===")

    pytrends = TrendReq(hl='en-GB', tz=0)
    keywords = ["luxury hotels"]

    pytrends.build_payload(keywords, timeframe='today 3-m', geo='GB')
    df = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)

    if df.empty:
        print("❌ No data returned")
        return False

    # Sort by first keyword
    df = df.sort_values(by=keywords[0], ascending=False)

    print(f"✅ Retrieved data for {len(df)} regions")
    print(f"   Top 5 regions for '{keywords[0]}':")
    for region, row in df.head(5).iterrows():
        print(f"   {region}: {int(row[keywords[0]])}/100")

    return True


def test_related_queries():
    """Test getting related queries"""
    print("\n=== Testing Related Queries ===")

    pytrends = TrendReq(hl='en-GB', tz=0)
    keyword = "coffee subscription"

    pytrends.build_payload([keyword], timeframe='today 3-m', geo='GB')
    related = pytrends.related_queries()

    if keyword not in related:
        print("❌ No data returned")
        return False

    top_df = related[keyword]['top']
    rising_df = related[keyword]['rising']

    print(f"✅ Retrieved related queries for '{keyword}'")

    if top_df is not None and not top_df.empty:
        print(f"\n   Top 5 related queries:")
        for _, row in top_df.head(5).iterrows():
            print(f"   - {row['query']} ({int(row['value'])})")
    else:
        print("   No top queries available")

    if rising_df is not None and not rising_df.empty:
        print(f"\n   Top 5 rising queries:")
        for _, row in rising_df.head(5).iterrows():
            val = "Breakout" if row['value'] == float('inf') else str(int(row['value']))
            print(f"   - {row['query']} ({val})")
    else:
        print("   No rising queries available")

    return True


def test_trending_searches():
    """Test getting trending searches"""
    print("\n=== Testing Trending Searches ===")

    pytrends = TrendReq(hl='en-GB', tz=0)

    try:
        df = pytrends.trending_searches(pn='united_kingdom')

        if df.empty:
            print("❌ No data returned")
            return False

        print(f"✅ Retrieved {len(df)} trending searches")
        print(f"   Top 10 trending now:")
        for i, trend in enumerate(df[0].head(10), 1):
            print(f"   {i}. {trend}")

        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_compare_keywords():
    """Test comparing keywords"""
    print("\n=== Testing Keyword Comparison ===")

    pytrends = TrendReq(hl='en-GB', tz=0)
    keywords = ["notebooks", "planners", "journals", "diaries"]

    pytrends.build_payload(keywords, timeframe='today 12-m', geo='GB')
    df = pytrends.interest_over_time()

    if df.empty:
        print("❌ No data returned")
        return False

    print(f"✅ Compared {len(keywords)} keywords")
    print(f"   Average search volume (0-100):")

    results = []
    for keyword in keywords:
        if keyword in df.columns:
            avg = df[keyword].mean()
            results.append((keyword, avg))

    results.sort(key=lambda x: x[1], reverse=True)

    for keyword, avg in results:
        print(f"   {keyword}: {avg:.1f}")

    print(f"\n   Winner: {results[0][0]}")

    return True


def test_suggestions():
    """Test getting suggestions"""
    print("\n=== Testing Keyword Suggestions ===")

    pytrends = TrendReq(hl='en-GB', tz=0)
    keyword = "christmas"

    suggestions = pytrends.suggestions(keyword=keyword)

    if not suggestions:
        print("❌ No suggestions returned")
        return False

    print(f"✅ Retrieved {len(suggestions)} suggestions for '{keyword}'")
    print(f"   Top 5 suggestions:")
    for suggestion in suggestions[:5]:
        print(f"   - {suggestion['title']} ({suggestion['type']})")

    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Google Trends MCP Server - Test Suite")
    print("=" * 60)

    tests = [
        ("Interest Over Time", test_interest_over_time),
        ("Interest By Region", test_interest_by_region),
        ("Related Queries", test_related_queries),
        ("Trending Searches", test_trending_searches),
        ("Compare Keywords", test_compare_keywords),
        ("Keyword Suggestions", test_suggestions),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Google Trends integration is working.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.")


if __name__ == "__main__":
    main()
