from googleapiclient.discovery import build
from datetime import datetime, timedelta

YOUTUBE_API_KEY = "AIzaSyDowdeXxrfH2TLrgxfxM70_javptOVYv4U"
channel_id = "UCXvVJYqEqB_qwvZoQQOgT3g"

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Get channel info
channel_request = youtube.channels().list(
    part='snippet,contentDetails',
    id=channel_id
)
channel_response = channel_request.execute()

if channel_response['items']:
    channel = channel_response['items'][0]
    print(f"Channel: {channel['snippet']['title']}")
    print(f"Uploads Playlist: {channel['contentDetails']['relatedPlaylists']['uploads']}")

    # Get recent uploads
    uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']
    
    published_after = (datetime.now() - timedelta(days=7)).isoformat() + 'Z'
    print(f"\nLooking for videos after: {published_after}")
    
    playlist_request = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_playlist_id,
        maxResults=10
    )
    playlist_response = playlist_request.execute()
    
    print(f"\nFound {len(playlist_response['items'])} recent videos:")
    for item in playlist_response['items']:
        snippet = item['snippet']
        print(f"  - {snippet['title']}")
        print(f"    Published: {snippet['publishedAt']}")
        print(f"    Video ID: {snippet['resourceId']['videoId']}")
else:
    print("Channel not found!")
