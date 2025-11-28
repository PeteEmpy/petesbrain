#!/usr/bin/env python3
"""
AI News Monitor

Monitors RSS feeds from respected AI and machine learning news websites.
Fetches new articles, scores them for relevance to AI in marketing/advertising,
and adds relevant ones to the knowledge base inbox for automated processing.

Runs automatically every 6 hours via LaunchAgent.
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import anthropic
import feedparser
import requests
from urllib.parse import urlparse

# Configuration
PROJECT_ROOT = Path("/Users/administrator/Documents/PetesBrain")
INBOX_DIR = PROJECT_ROOT / "roksys/knowledge-base/_inbox/documents"
STATE_FILE = PROJECT_ROOT / "shared/data/ai-news-state.json"
LOG_FILE = PROJECT_ROOT / "shared/data/ai-news-monitor.log"

# Minimum relevance score (0-10) to import article
MIN_RELEVANCE_SCORE = 6

# RSS Feeds from respected AI news sources
RSS_FEEDS = {
    # Marketing AI Specific
    "Marketing AI Institute": "https://www.marketingaiinstitute.com/blog/rss.xml",
    "MarTech - AI": "https://martech.org/feed/",
    "Adweek - AI": "https://www.adweek.com/category/artificial-intelligence/feed/",

    # Major AI Research & Companies
    "OpenAI Blog": "https://openai.com/blog/rss/",
    "Google AI Blog": "https://ai.googleblog.com/feeds/posts/default",
    "Microsoft AI Blog": "https://blogs.microsoft.com/ai/feed/",
    "Anthropic News": "https://www.anthropic.com/news/rss.xml",

    # AI News & Analysis
    "MIT Technology Review - AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "VentureBeat - AI": "https://venturebeat.com/category/ai/feed/",
    "AI News": "https://www.artificialintelligence-news.com/feed/",

    # Practical AI & ML
    "Machine Learning Mastery": "https://machinelearningmastery.com/feed/",
    "Towards Data Science": "https://towardsdatascience.com/feed",
}


def log_message(message):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    print(log_entry.strip())

    # Ensure log directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)


def load_state():
    """Load previously processed article IDs"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"processed_articles": [], "last_run": None}


def save_state(state):
    """Save state to file"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def generate_article_id(entry):
    """Generate unique ID for article"""
    # Use URL or combination of title + published date
    if hasattr(entry, 'link'):
        return hashlib.md5(entry.link.encode()).hexdigest()

    identifier = f"{entry.title}_{entry.get('published', '')}"
    return hashlib.md5(identifier.encode()).hexdigest()


def score_article_relevance(title, summary, content_preview):
    """Use Claude to score article relevance for AI in marketing/advertising knowledge base"""

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        log_message("ERROR: ANTHROPIC_API_KEY not set")
        return 0, None

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Analyze this article and score its relevance for an AI strategy knowledge base focused on marketing, advertising, and business automation.

Title: {title}

Summary/Description: {summary}

Content Preview: {content_preview[:2000]}

Score the article from 0-10 based on:
- Relevance to AI in marketing, advertising, or PPC
- Actionable insights for marketers using AI
- Strategic guidance for AI adoption
- Practical applications of AI/ML in business

Criteria for HIGH scores (8-10):
- AI tools and platforms for marketing/advertising
- Generative AI for content creation and ad copy
- AI automation for campaign management
- Machine learning for audience targeting
- AI-powered analytics and insights
- Marketing AI strategy and best practices
- Claude/ChatGPT/GPT use cases in marketing

Criteria for MEDIUM scores (5-7):
- General AI trends relevant to business
- AI ethics and regulation affecting marketing
- AI product launches (tools, APIs, models)
- Machine learning fundamentals applicable to marketing
- AI research with practical implications

Criteria for LOW scores (0-4):
- Pure academic AI research (no marketing application)
- AI in unrelated fields (healthcare, robotics, etc.)
- Highly technical ML papers without business context
- AI news with no marketing/advertising relevance
- Speculative AI content without actionable insights

Respond in JSON format:
{{
    "relevance_score": 0-10,
    "primary_topic": "brief topic description",
    "reason": "1-2 sentence explanation of score",
    "recommended_action": "import|skip"
}}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text

        # Extract JSON
        if '{' in response_text and '}' in response_text:
            json_start = response_text.index('{')
            json_end = response_text.rindex('}') + 1
            json_str = response_text[json_start:json_end]
            analysis = json.loads(json_str)

            return analysis.get('relevance_score', 0), analysis

        return 0, None

    except Exception as e:
        log_message(f"Error scoring article: {e}")
        return 0, None


def create_inbox_file(entry, feed_name, score_analysis):
    """Create formatted file in inbox for processing"""

    # Generate safe filename
    title_slug = entry.title[:50].lower()
    title_slug = "".join(c if c.isalnum() or c in [' ', '-'] else '' for c in title_slug)
    title_slug = title_slug.replace(' ', '-').strip('-')

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_ai_{title_slug}.md"

    filepath = INBOX_DIR / filename

    # Build markdown content
    content = f"""---
source: {feed_name}
url: {entry.link}
published: {entry.get('published', 'N/A')}
relevance_score: {score_analysis['relevance_score']}
primary_topic: {score_analysis['primary_topic']}
fetched: {datetime.now().isoformat()}
category: AI News
---

# {entry.title}

**Source**: {feed_name}
**URL**: {entry.link}
**Published**: {entry.get('published', 'N/A')}
**Relevance Score**: {score_analysis['relevance_score']}/10

## Summary

{entry.get('summary', 'No summary available')}

## Scoring Analysis

**Primary Topic**: {score_analysis['primary_topic']}
**Reason**: {score_analysis['reason']}

---

*Article fetched by AI news monitor*
*Full content will be processed by knowledge base system*

**Original URL**: {entry.link}
"""

    # Write to inbox
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    log_message(f"✓ Added to inbox: {filename}")
    return filepath


def process_feed(feed_url, feed_name, state):
    """Process a single RSS feed"""

    log_message(f"Checking: {feed_name}")

    try:
        # Parse RSS feed
        feed = feedparser.parse(feed_url)

        if not feed.entries:
            log_message(f"  No entries found in {feed_name}")
            return 0

        new_articles = 0
        relevant_articles = 0

        # Process each entry
        for entry in feed.entries[:10]:  # Limit to 10 most recent
            article_id = generate_article_id(entry)

            # Skip if already processed
            if article_id in state['processed_articles']:
                continue

            # Check if article is recent (last 7 days)
            try:
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_date = datetime(*entry.published_parsed[:6])
                    if published_date < datetime.now() - timedelta(days=7):
                        continue  # Skip older articles on first run
            except:
                pass  # If date parsing fails, process anyway

            new_articles += 1

            # Get article summary/description
            summary = entry.get('summary', entry.get('description', ''))

            # Score relevance
            log_message(f"  Scoring: {entry.title[:60]}...")
            score, analysis = score_article_relevance(
                entry.title,
                summary,
                summary  # Use summary as content preview
            )

            if score >= MIN_RELEVANCE_SCORE and analysis:
                log_message(f"  ✓ Relevant ({score}/10): {analysis['primary_topic']}")

                # Add to inbox
                create_inbox_file(entry, feed_name, analysis)
                relevant_articles += 1

            else:
                log_message(f"  ✗ Skipped ({score}/10): Not relevant enough")

            # Mark as processed
            state['processed_articles'].append(article_id)

        log_message(f"  Summary: {new_articles} new, {relevant_articles} relevant")
        return relevant_articles

    except Exception as e:
        log_message(f"ERROR processing {feed_name}: {e}")
        return 0


def monitor_feeds():
    """Main function to monitor all RSS feeds"""

    log_message("=" * 70)
    log_message("AI News Monitor Started")
    log_message("=" * 70)

    # Load state
    state = load_state()
    last_run = state.get('last_run')

    if last_run:
        log_message(f"Last run: {last_run}")
    else:
        log_message("First run - will process recent articles from last 7 days")

    total_relevant = 0

    # Process each feed
    for feed_name, feed_url in RSS_FEEDS.items():
        try:
            relevant_count = process_feed(feed_url, feed_name, state)
            total_relevant += relevant_count
        except Exception as e:
            log_message(f"ERROR with feed {feed_name}: {e}")

    # Update state
    state['last_run'] = datetime.now().isoformat()

    # Keep only last 1000 processed article IDs to prevent state file from growing forever
    if len(state['processed_articles']) > 1000:
        state['processed_articles'] = state['processed_articles'][-1000:]

    save_state(state)

    log_message("=" * 70)
    log_message(f"Monitoring Complete: {total_relevant} relevant articles added to inbox")
    log_message("=" * 70)

    if total_relevant > 0:
        log_message(f"Articles will be processed by knowledge-base-processor.py within 6 hours")


if __name__ == "__main__":
    monitor_feeds()
