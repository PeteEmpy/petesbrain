#!/usr/bin/env python3
"""
Retrieve Google Chat conversation by conversation ID
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

SCOPES = [
    "https://www.googleapis.com/auth/chat.messages.readonly",
    "https://www.googleapis.com/auth/chat.spaces.readonly"
]


def get_chat_service():
    """Create and return a Google Chat service instance using OAuth"""
    # Try to use Google Tasks credentials (same OAuth pattern)
    token_path = Path(__file__).parent.parent / "mcp-servers" / "google-tasks-mcp-server" / "token.json"
    credentials_path = Path(__file__).parent.parent / "mcp-servers" / "google-tasks-mcp-server" / "credentials.json"
    
    creds = None
    
    # Load existing token if available
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception as e:
            print(f"Warning: Could not load existing token: {e}")
            creds = None
    
    # Refresh token if expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Refreshing expired token...")
                creds.refresh(Request())
                # Save refreshed token
                with open(token_path, "w") as token_file:
                    token_file.write(creds.to_json())
                print("Token refreshed successfully")
            except Exception as e:
                print(f"Error refreshing token: {e}")
                print("\nYou may need to re-authenticate with Google Chat API scopes.")
                print("Run: python3 -c \"from google_auth_oauthlib.flow import InstalledAppFlow; flow = InstalledAppFlow.from_client_secrets_file('{}', {}); creds = flow.run_local_server(); open('{}', 'w').write(creds.to_json())\"".format(
                    credentials_path, SCOPES, token_path
                ))
                sys.exit(1)
        else:
            print(f"OAuth credentials not found or invalid.")
            print(f"Token path: {token_path}")
            print(f"Credentials path: {credentials_path}")
            print("\nTo authenticate:")
            print("1. Ensure credentials.json exists at the credentials path")
            print("2. Run OAuth flow with Chat API scopes")
            sys.exit(1)
    
    return build("chat", "v1", credentials=creds)


def get_conversation(conversation_id):
    """Retrieve a Google Chat conversation by ID"""
    try:
        service = get_chat_service()
        
        # Try to get the space/conversation
        # Note: Google Chat API uses spaces and threads
        # The ID format suggests this might be a space ID or thread ID
        
        print(f"Retrieving conversation: {conversation_id}")
        
        # Try as a space first
        try:
            space = service.spaces().get(name=f"spaces/{conversation_id}").execute()
            print(f"Found space: {space.get('displayName', 'Unnamed')}")
            
            # Get messages from this space
            messages_result = service.spaces().messages().list(
                parent=f"spaces/{conversation_id}",
                pageSize=100
            ).execute()
            
            return {
                "type": "space",
                "space": space,
                "messages": messages_result.get("messages", [])
            }
        except Exception as e:
            print(f"Not a space: {e}")
        
        # Try as a message thread
        try:
            # If it's a message ID, get the message and its thread
            message = service.spaces().messages().get(
                name=f"spaces/*/messages/{conversation_id}"
            ).execute()
            
            # Get thread messages
            thread_name = message.get("thread", {}).get("name", "")
            if thread_name:
                thread_messages = service.spaces().messages().list(
                    parent=thread_name,
                    pageSize=100
                ).execute()
            else:
                thread_messages = {"messages": [message]}
            
            return {
                "type": "message_thread",
                "message": message,
                "messages": thread_messages.get("messages", [])
            }
        except Exception as e:
            print(f"Not a message: {e}")
        
        # Try listing spaces and searching
        print("Searching all accessible spaces...")
        spaces_result = service.spaces().list(pageSize=100).execute()
        spaces = spaces_result.get("spaces", [])
        
        for space in spaces:
            space_name = space.get("name", "")
            if conversation_id in space_name:
                print(f"Found matching space: {space.get('displayName', 'Unnamed')}")
                messages_result = service.spaces().messages().list(
                    parent=space_name,
                    pageSize=100
                ).execute()
                return {
                    "type": "space",
                    "space": space,
                    "messages": messages_result.get("messages", [])
                }
        
        return None
        
    except Exception as e:
        print(f"Error retrieving conversation: {e}")
        import traceback
        traceback.print_exc()
        return None


def format_conversation(conversation_data):
    """Format conversation data as markdown"""
    if not conversation_data:
        return None
    
    output = []
    
    if conversation_data["type"] == "space":
        space = conversation_data["space"]
        output.append(f"# Google Chat Conversation")
        output.append("")
        output.append(f"**Space:** {space.get('displayName', 'Unnamed')}")
        output.append(f"**Space ID:** {space.get('name', 'N/A')}")
        output.append(f"**Type:** {space.get('type', 'N/A')}")
        output.append(f"**Retrieved:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("")
        output.append("---")
        output.append("")
    else:
        output.append(f"# Google Chat Message Thread")
        output.append("")
        output.append(f"**Retrieved:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("")
        output.append("---")
        output.append("")
    
    messages = conversation_data.get("messages", [])
    output.append(f"## Messages ({len(messages)} total)")
    output.append("")
    
    for msg in messages:
        sender = msg.get("sender", {})
        sender_name = sender.get("name", "Unknown")
        sender_email = sender.get("email", "")
        
        create_time = msg.get("createTime", "")
        text = msg.get("text", "")
        thread = msg.get("thread", {})
        
        output.append(f"### {sender_name}")
        if sender_email:
            output.append(f"**Email:** {sender_email}")
        output.append(f"**Time:** {create_time}")
        if thread.get("name"):
            output.append(f"**Thread:** {thread.get('name')}")
        output.append("")
        output.append(text)
        output.append("")
        output.append("---")
        output.append("")
    
    return "\n".join(output)


def save_conversation(conversation_data, conversation_id):
    """Save conversation to appropriate location"""
    formatted = format_conversation(conversation_data)
    
    if not formatted:
        print("No conversation data to save")
        return None
    
    # Save to inbox for processing
    inbox_path = Path(__file__).parent.parent.parent.parent / "!inbox"
    inbox_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}-google-chat-{conversation_id[:8]}.md"
    filepath = inbox_path / filename
    
    with open(filepath, "w") as f:
        f.write(formatted)
    
    print(f"\n✅ Conversation saved to: {filepath}")
    return filepath


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 retrieve-chat-conversation.py <conversation-id>")
        print("\nExample:")
        print("  python3 retrieve-chat-conversation.py 0817580f-67ce-45a2-9f8d-1f29964e1f49")
        sys.exit(1)
    
    conversation_id = sys.argv[1]
    
    print("=" * 60)
    print("Google Chat Conversation Retriever")
    print("=" * 60)
    print()
    
    conversation_data = get_conversation(conversation_id)
    
    if conversation_data:
        print(f"\n✅ Successfully retrieved conversation")
        print(f"   Type: {conversation_data['type']}")
        print(f"   Messages: {len(conversation_data.get('messages', []))}")
        
        filepath = save_conversation(conversation_data, conversation_id)
        
        if filepath:
            print(f"\n📝 Next steps:")
            print(f"   1. Review the conversation in: {filepath}")
            print(f"   2. Add routing keywords if needed (client:, task:, knowledge:)")
            print(f"   3. Process with: python3 agents/system/inbox-processor.py")
    else:
        print("\n❌ Could not retrieve conversation")
        print("\nPossible reasons:")
        print("  - Conversation ID is incorrect")
        print("  - You don't have access to this conversation")
        print("  - OAuth scopes need to be updated")
        print("  - The conversation may have been deleted")
































