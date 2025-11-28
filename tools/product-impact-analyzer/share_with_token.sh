#!/bin/bash
TOKEN='ya29.a0ATi6K2vUhRJdtLyUaoprFv7f2yF47rtpHjRNA20NT55yrFwLyTiBytKl5q-Zvzz1xbXo4o3hPJatB7LSQazjukzL_3-t3XabmDHvkfF4ZRdzv06I_rUR6vWq_W2YEJeb6VxUhUqBZfQW6bJdn-JzO34jWMJ4SmD9Conje4mInOYQU7P8qTQz-X02CVy-5tW0vgdg5lAaCgYKATESARUSFQHGX2Mi7-bEAW33LHPiKufe24nGOA0206'
SERVICE_ACCOUNT='mcp-sheets-reader@petesbrain-emailsync.iam.gserviceaccount.com'

share_spreadsheet() {
  local name="$1"
  local id="$2"
  
  echo "Sharing: $name"
  curl -s -X POST \
    "https://www.googleapis.com/drive/v3/files/$id/permissions" \
    -H "Authorization: Bearer $TOKEN" \
    -H 'Content-Type: application/json' \
    -d "{
      \"type\": \"user\",
      \"role\": \"writer\",
      \"emailAddress\": \"$SERVICE_ACCOUNT\"
    }" > /dev/null
  
  if [ $? -eq 0 ]; then
    echo "  ✓ Success"
  else
    echo "  ❌ Failed"
  fi
}

share_spreadsheet "Smythson UK" "1DtK0MX5qwISwO8blvbBT9rEQWqn-uVFp5hS3xBR-glo"
share_spreadsheet "BrightMinds" "12jpLRhbMmZ-cIhmI53dY6hB520GhZGoKN_NTDxfX3ks"
share_spreadsheet "Accessories for the Home" "1V23MwIeSDTj5ECBJAOIukENzy3YMxUoOEMiSP2IZAWM"
share_spreadsheet "Go Glean UK" "1Jqy3Y4jQGUQFwyvjTHAb0JCOAxwndaIvZItvkU-xaqw"
share_spreadsheet "Superspace UK" "1N8H0n1qL3jWHdWxKlbyF0ywjQ1Hn5YSbgxgC4Ig2B6s"
share_spreadsheet "Uno Lights" "1vQAD5xOA-u2LWwB1AzxJJd1RJIBbqHpHHmlseO0Ko-A"
share_spreadsheet "Godshot" "1Hrr27rAc1PpVxefSLja5TlEAD4Dg1rqNxbqn4FeaYCk"
share_spreadsheet "HappySnapGifts" "1nTJyS3I5GlkRJfTeoTWBX3ehV-EDYnHOIn7Yq7raXd0"
share_spreadsheet "WheatyBags" "1htjYR0YM5TFmd1NwIS6M6jSev86VsEJ5-okkX-5MOdI"
share_spreadsheet "BMPM" "1EenJFkPWGZ6c_ZhsKKYudDcW2Nt8Jeamc1m55BPR5dU"
share_spreadsheet "Grain Guard" "1VFyGERR0OHX12CwP76YUWexegrEoyhAaReGGRX9kMjw"
share_spreadsheet "Crowd Control" "1V3RY5Kw5b22nzveWfDNQfjzsJ8CVdV4km0pXE3Nfofw"
share_spreadsheet "Just Bin Bags" "1zEiKnU-jJjEqchmXIX3QhML-g3H3v6ZstLFfz69CJyA"
share_spreadsheet "Just Bin Bags JHD" "1p7hVR4bwMVTiBj8za6pVv3kmnVr8v3YEz2fhGun2YSk"

echo ""
echo "All spreadsheets shared with service account!"
