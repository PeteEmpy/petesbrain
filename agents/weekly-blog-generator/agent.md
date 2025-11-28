---
name: weekly-blog-generator
status: active
last_migrated: 2025-11-13
last_fixed: 2025-11-18
---

# weekly-blog-generator

## Purpose
Generates and publishes weekly Google Ads blog posts to roksys.co.uk from knowledge base articles.

## Schedule
**Every Monday at 7:30 AM** - Recurring weekly task

## How It Works
1. Fetches recent articles from knowledge base (last 7 days)
2. Generates blog post using Claude API
3. Publishes to WordPress (scheduled for following Sunday at 9 AM)
4. Logs all activity to `~/.petesbrain-weekly-blog.log`

## Configuration
- Script: `weekly-blog-generator.py`
- LaunchAgent: `com.petesbrain.weekly-blog-generator.plist`
- Log: `~/.petesbrain-weekly-blog.log`
- Venv: `.venv/` (contains anthropic, requests, feedparser, python-wordpress-xmlrpc)

## Migration Notes
- **Nov 13, 2025**: Migrated from `agents/content-sync/` to `agents/weekly-blog-generator/`
- **Nov 18, 2025**: Fixed after migration broke dependencies - installed missing packages, updated paths to use venv
