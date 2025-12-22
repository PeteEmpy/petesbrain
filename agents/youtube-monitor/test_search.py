from googleapiclient.discovery import build

YOUTUBE_API_KEY = "AIzaSyDowdeXxrfH2TLrgxfxM70_javptOVYv4U"

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Search for Common Thread Collective channel
search_request = youtube.search().list(
    part='snippet',
    q='Common Thread Collective',
    type='channel',
    maxResults=5
)
search_response = search_request.execute()

print(f"Found {len(search_response.get('items', []))} channels:")
for item in search_response.get('items', []):
    snippet = item['snippet']
    channel_id = item['id']['channelId']
    print(f"\nChannel: {snippet['title']}")
    print(f"Channel ID: {channel_id}")
    print(f"Description: {snippet['description'][:100]}...")
