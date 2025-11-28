---
name: wordpress-blog-manager
description: Manages WordPress blog posts, navigation, and content for roksys.co.uk. Use when user asks about publishing blog posts, WordPress access, blog navigation, editing blog content, or needs WordPress admin credentials.
allowed-tools: Bash, Read
---

# WordPress Blog Manager Skill

**Capabilities**:
- Publish scheduled blog posts immediately
- Remove text from blog posts
- Set up blog navigation (Elementor-compatible)
- Access WordPress admin and site information
- Manage blog categories and tags
- View blog post status and URLs
- Provide WordPress access credentials and URLs

**WordPress Access Information**:
- **Site URL**: https://roksys.co.uk
- **Admin URL**: https://roksys.co.uk/wp-admin
- **Username**: Peter
- **Application Password**: Stored in LaunchAgent environment variables (`com.petesbrain.weekly-blog-generator.plist`)
- **Application Password Name**: "Weekly Blog Generator"
- **Blog Category**: "Google Ads Weekly" (ID: 5)
- **Blog Page**: "Google Ads Blog" (ID: 507)
- **Category Archive**: https://roksys.co.uk/category/google-ads-weekly/
- **Blog Page URL**: https://roksys.co.uk/google-ads-blog/

**Platform Details**:
- **CMS**: WordPress
- **Page Builder**: Elementor
- **Navigation**: Managed via Elementor Header Builder (not standard WordPress menu)
- **Note**: Blog menu items must be added manually in Elementor

**Available Scripts**:
- `agents/content-sync/weekly-blog-generator.py` - Auto-generates weekly posts (runs Monday 7:30 AM)
- `agents/content-sync/publish-blog-post-now.py` - Publish scheduled posts immediately
- `agents/content-sync/remove-text-from-post.py` - Remove text from posts
- `agents/content-sync/wordpress-blog-navigation-setup.py` - Set up navigation

**Automation**:
- **Blog Generator**: Runs every Monday at 7:30 AM
- **Publishes**: Every Monday at 9:00 AM (scheduled)
- **Sunday KB Update**: Sunday 11:00 PM (ensures fresh content for blog)

**When This Skill Activates**:
1. User asks about WordPress access or credentials
2. User wants to publish/edit blog posts
3. User needs to manage blog navigation
4. User asks about blog post status or URLs
5. User needs WordPress admin access information

**How to Use**:
- For publishing: Run `publish-blog-post-now.py` script
- For editing: Provide WordPress admin URL and post ID
- For navigation: Use `wordpress-blog-navigation-setup.py` or provide Elementor instructions
- For access: Provide admin URL, username, and note where password is stored

**Resources**:
- `agents/content-sync/WORDPRESS-SETUP.md` - Setup and configuration guide
- `agents/content-sync/WORDPRESS-TROUBLESHOOTING.md` - Common issues and fixes
- `agents/content-sync/BLOG-NAVIGATION-SETUP.md` - Navigation setup guide (Elementor)
- `roksys/CONTEXT.md` - WordPress access credentials and site information
- `agents/launchagents/com.petesbrain.weekly-blog-generator.plist` - LaunchAgent with credentials

**Quick Reference**:
- **Admin Login**: https://roksys.co.uk/wp-admin
- **Blog Archive**: https://roksys.co.uk/category/google-ads-weekly/
- **Edit Post**: https://roksys.co.uk/wp-admin/post.php?post=[ID]&action=edit
- **Application Password**: Check LaunchAgent plist file for current password

