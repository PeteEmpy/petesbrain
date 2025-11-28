# WordPress Authentication Troubleshooting

## Issue: "You are not allowed to create posts as this user"

This error means the WordPress user account needs proper permissions.

## Fix: Check User Role

1. Go to: **https://roksys.co.uk/wp-admin**
2. Navigate to: **Users → All Users**
3. Find your user account
4. Check the **Role** column
5. It should be **Administrator** or **Editor**
6. If it's **Author** or **Contributor**, change it:
   - Click **Edit** on your user
   - Change **Role** to **Administrator** or **Editor**
   - Click **Update User**

## Verify Username

The username might not be "petere". To find it:

1. Go to: **https://roksys.co.uk/wp-admin**
2. Look at top-right corner - your username is displayed there
3. Or go to **Users → Your Profile** - username is shown at top

## Update Configuration

Once you know the correct username and have verified the role:

Edit the LaunchAgent plist:
```bash
nano ~/Library/LaunchAgents/com.petesbrain.weekly-blog-generator.plist
```

Update these lines:
```xml
<key>WORDPRESS_USERNAME</key>
<string>your_actual_username</string>
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.petesbrain.weekly-blog-generator.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.weekly-blog-generator.plist
```

## Test Again

After fixing permissions/username:
```bash
cd /Users/administrator/Documents/PetesBrain
export WORDPRESS_URL="https://roksys.co.uk"
export WORDPRESS_USERNAME="your_username"
export WORDPRESS_APP_PASSWORD="qxxA8shXiVJtD9tlI0RY0Rvf"
export ANTHROPIC_API_KEY="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"
/Users/administrator/Documents/PetesBrain/shared/email-sync/.venv/bin/python3 agents/content-sync/weekly-blog-generator.py
```

## Good News!

✅ **Blog post generation is working perfectly!**
- Generated 965-word post in your tone
- Covers latest Google Ads trends
- Saved draft: `shared/data/blog-draft-20251108.html`

Once WordPress permissions are fixed, publishing will work automatically!

