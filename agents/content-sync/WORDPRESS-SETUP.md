# WordPress Setup - Step by Step

## Step 1: Get Application Password

1. Go to: **https://roksys.co.uk/wp-admin**
2. Log in with your WordPress credentials
3. Navigate to: **Users → Your Profile** (or click your name in top right)
4. Scroll down to: **Application Passwords** section
5. Enter name: `Weekly Blog Generator`
6. Click: **Add New Application Password**
7. **IMPORTANT**: Copy the password immediately (it's shown only once!)
   - Format: `xxxx xxxx xxxx xxxx` (spaces included, or without spaces)

## Step 2: Run Setup Script

Once you have the password, run:

```bash
cd /Users/administrator/Documents/PetesBrain/agents/content-sync
./setup-weekly-blog.sh https://roksys.co.uk YOUR_USERNAME YOUR_APP_PASSWORD
```

Replace:
- `YOUR_USERNAME` = Your WordPress username
- `YOUR_APP_PASSWORD` = The password from Step 1 (can include or remove spaces)

## Step 3: Test It

After setup, test manually:

```bash
cd /Users/administrator/Documents/PetesBrain
export WORDPRESS_URL="https://roksys.co.uk"
export WORDPRESS_USERNAME="your_username"
export WORDPRESS_APP_PASSWORD="your_app_password"
/Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3 agents/content-sync/weekly-blog-generator.py
```

## What to Expect

The script will:
1. Pull recent articles from your knowledge base
2. Generate a blog post in your tone
3. Create a WordPress draft post
4. Schedule it for next Monday at 9 AM

Check the log:
```bash
tail -f ~/.petesbrain-weekly-blog.log
```

## Troubleshooting

**"401 Unauthorized"**
- Check Application Password is correct
- Make sure username is correct
- Verify Application Passwords are enabled in WordPress

**"403 Forbidden"**
- Check user has permission to publish posts
- Verify REST API is enabled

**"No recent articles found"**
- Run: `python3 agents/content-sync/knowledge-base-indexer.py`
- Check articles exist in KB from last 7 days

