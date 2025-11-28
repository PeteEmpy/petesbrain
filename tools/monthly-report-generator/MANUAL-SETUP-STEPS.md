# Manual Setup Steps - Google Slides API

Follow these steps to set up the Google API credentials for automated report generation.

## Step 1: Create Google Cloud Project (2 minutes)

1. Go to: https://console.cloud.google.com/
2. Click "Select a project" dropdown at the top
3. Click "NEW PROJECT"
4. Name: **PetesBrain Reports**
5. Click "CREATE"
6. Wait for project to be created (~30 seconds)

## Step 2: Enable APIs (2 minutes)

1. Make sure "PetesBrain Reports" is selected
2. Go to: https://console.cloud.google.com/apis/library
3. Search for "Google Slides API"
4. Click it, then click "ENABLE"
5. Go back to APIs library
6. Search for "Google Drive API"
7. Click it, then click "ENABLE"

## Step 3: Create Service Account (3 minutes)

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Make sure "PetesBrain Reports" project is selected
3. Click "CREATE SERVICE ACCOUNT" button
4. Fill in:
   - **Name**: `monthly-report-generator`
   - **Description**: `Automated monthly report generation for Devonshire Hotels`
5. Click "CREATE AND CONTINUE"
6. **Skip the permissions** - Click "CONTINUE" (we don't need special permissions)
7. Click "DONE"

## Step 4: Create and Download Key (2 minutes)

1. You should see your service account listed
2. Click on the service account email (looks like `monthly-report-generator@...`)
3. Go to the "KEYS" tab
4. Click "ADD KEY" → "Create new key"
5. Select "JSON" format
6. Click "CREATE"
7. A JSON file will automatically download to your Downloads folder

## Step 5: Move Credentials File (1 minute)

Open Terminal and run these commands:

```bash
# Create credentials directory
mkdir -p ~/Documents/PetesBrain/shared/credentials

# Move the downloaded key (replace the filename with yours)
mv ~/Downloads/petesbrain-reports-*.json ~/Documents/PetesBrain/shared/credentials/google-slides-credentials.json

# Verify it's there
ls -la ~/Documents/PetesBrain/shared/credentials/google-slides-credentials.json
```

## Step 6: Get Service Account Email (1 minute)

We need the service account email to share the Drive folder.

```bash
# Extract the email from the credentials file
cat ~/Documents/PetesBrain/shared/credentials/google-slides-credentials.json | grep client_email
```

Copy the email address that looks like:
`monthly-report-generator@petesbrain-reports-XXXXX.iam.gserviceaccount.com`

## Step 7: Share Drive Folder with Service Account (2 minutes)

1. Open Google Drive: https://drive.google.com
2. Create a new folder called "Devonshire Reports" (or use an existing one)
3. Right-click the folder → "Share"
4. Paste the service account email from Step 6
5. Give it "Editor" access
6. **Uncheck "Notify people"** (it's a service account, not a person)
7. Click "Share"

## Step 8: Install Python Dependencies (2 minutes)

```bash
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Step 9: Test the Setup (1 minute)

```bash
cd ~/Documents/PetesBrain/tools/monthly-report-generator
python3 generate_devonshire_slides.py --month 2025-10
```

If successful, you'll see:
```
✅ Presentation created successfully!
🔗 Presentation ID: [ID]
🔗 URL: https://docs.google.com/presentation/d/[ID]
```

Open the URL to see your presentation with:
- Estate Blue (#00333D) headers
- Stone (#E5E3DB) data cell backgrounds
- Properly formatted native tables

## Troubleshooting

**"Credentials file not found"**
- Check the file is at: `~/Documents/PetesBrain/shared/credentials/google-slides-credentials.json`
- Verify the path with: `ls -la ~/Documents/PetesBrain/shared/credentials/`

**"Permission denied" errors**
- Make sure you shared the Drive folder with the service account email
- Wait 1-2 minutes for permissions to propagate
- Try the generation command again

**"Module not found" errors**
- Run: `pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib`

## You're Done!

Once setup is complete, generating monthly reports is just:

```bash
python3 ~/Documents/PetesBrain/tools/monthly-report-generator/generate_devonshire_slides.py --month 2025-11
```

**Total setup time**: ~15 minutes
**Monthly usage time**: ~2 minutes
**Annual time saved**: ~30 hours
