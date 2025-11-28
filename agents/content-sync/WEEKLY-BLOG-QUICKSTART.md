# Weekly Blog Generator - Quick Start

## What Was Built

✅ **Fully automated WordPress blog post generator**
- Pulls articles from your knowledge base (last 7 days)
- Writes in your tone of voice (from roksys.co.uk)
- Auto-publishes to WordPress every Monday
- Zero manual intervention needed

## Quick Setup (3 Steps)

### Step 1: Get WordPress Application Password

1. Go to: `https://roksys.co.uk/wp-admin`
2. Navigate to: **Users → Your Profile**
3. Scroll to: **Application Passwords**
4. Name: `Weekly Blog Generator`
5. Click: **Add New Application Password**
6. **Copy the password** (shown only once!)

### Step 2: Run Setup Script

```bash
cd /Users/administrator/Documents/PetesBrain/agents/weekly-blog-generator
./setup-weekly-blog.sh https://roksys.co.uk your_username your_app_password
```

Replace:
- `your_username` = Your WordPress username
- `your_app_password` = The password from Step 1

### Step 3: Test It

```bash
cd /Users/administrator/Documents/PetesBrain
export WORDPRESS_URL="https://roksys.co.uk"
export WORDPRESS_USERNAME="your_username"
export WORDPRESS_APP_PASSWORD="your_app_password"
/Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3 agents/weekly-blog-generator/weekly-blog-generator.py
```

Check the log:
```bash
tail -f ~/.petesbrain-weekly-blog.log
```

## That's It!

The system will now:
- Run every Monday at 8:00 AM
- Generate blog post from recent KB articles
- Schedule for publication at 9:00 AM
- Write in your tone of voice
- Require zero weekly involvement

## Files Created

- `agents/weekly-blog-generator/weekly-blog-generator.py` - Main script
- `agents/launchagents/com.petesbrain.weekly-blog-generator.plist` - LaunchAgent config
- `agents/content-sync/setup-weekly-blog.sh` - Setup script
- `agents/content-sync/WEEKLY-BLOG-GENERATOR-README.md` - Full documentation

## Need Help?

Check the full README: `agents/content-sync/WEEKLY-BLOG-GENERATOR-README.md`

