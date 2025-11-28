# Share All Spreadsheets with Service Account
# Service account: mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com
# Spreadsheets: 14

# First, get your OAuth token:
# Visit: https://developers.google.com/oauthplayground
# 1. Select 'Drive API v3' → check 'https://www.googleapis.com/auth/drive'
# 2. Click 'Authorize APIs' and sign in
# 3. Click 'Exchange authorization code for tokens'
# 4. Copy the 'Access token'
# 5. Replace YOUR_TOKEN_HERE below with your token

TOKEN='YOUR_TOKEN_HERE'

# Smythson UK
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1DtK0MX5qwISwO8blvbBT9rEQWqn-uVFp5hS3xBR-glo/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ Smythson UK"

# BrightMinds
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/12jpLRhbMmZ-cIhmI53dY6hB520GhZGoKN_NTDxfX3ks/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ BrightMinds"

# Accessories for the Home
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1V23MwIeSDTj5ECBJAOIukENzy3YMxUoOEMiSP2IZAWM/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ Accessories for the Home"

# Go Glean UK
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1Jqy3Y4jQGUQFwyvjTHAb0JCOAxwndaIvZItvkU-xaqw/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ Go Glean UK"

# Superspace UK
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1N8H0n1qL3jWHdWxKlbyF0ywjQ1Hn5YSbgxgC4Ig2B6s/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ Superspace UK"

# Uno Lights
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1vQAD5xOA-u2LWwB1AzxJJd1RJIBbqHpHHmlseO0Ko-A/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ Uno Lights"

# Godshot
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1Hrr27rAc1PpVxefSLja5TlEAD4Dg1rqNxbqn4FeaYCk/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ Godshot"

# HappySnapGifts
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1nTJyS3I5GlkRJfTeoTWBX3ehV-EDYnHOIn7Yq7raXd0/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ HappySnapGifts"

# WheatyBags
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1htjYR0YM5TFmd1NwIS6M6jSev86VsEJ5-okkX-5MOdI/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ WheatyBags"

# BMPM
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1EenJFkPWGZ6c_ZhsKKYudDcW2Nt8Jeamc1m55BPR5dU/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ BMPM"

# Grain Guard
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1VFyGERR0OHX12CwP76YUWexegrEoyhAaReGGRX9kMjw/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ Grain Guard"

# Crowd Control
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1V3RY5Kw5b22nzveWfDNQfjzsJ8CVdV4km0pXE3Nfofw/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ Crowd Control"

# Just Bin Bags
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1zEiKnU-jJjEqchmXIX3QhML-g3H3v6ZstLFfz69CJyA/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ Just Bin Bags"

# Just Bin Bags JHD
curl -X POST \
  'https://www.googleapis.com/drive/v3/files/1p7hVR4bwMVTiBj8za6pVv3kmnVr8v3YEz2fhGun2YSk/permissions' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "user",
    "role": "writer",
    "emailAddress": "mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com"
  }'
echo " ✓ Just Bin Bags JHD"


echo 'All spreadsheets shared!'
