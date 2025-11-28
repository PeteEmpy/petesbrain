#!/usr/bin/env python3
"""
Simple HTTP server to receive task notes from browser and save to fixed location.
This allows the HTML workflow to save directly to PetesBrain without browser download dialogs.

Usage:
    python3 save-task-notes.py

Then update tasks-overview.html to POST to http://localhost:8765/save-notes
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime

# Fixed location within PetesBrain
NOTES_FILE = "/Users/administrator/Documents/PetesBrain/data/state/manual-task-notes.json"

class TaskNotesHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save-notes':
            # Read the JSON data from request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                # Parse and validate JSON
                notes_data = json.loads(post_data.decode('utf-8'))

                # Save to fixed location
                os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
                with open(NOTES_FILE, 'w') as f:
                    json.dump(notes_data, f, indent=2)

                # Success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # Allow from file://
                self.end_headers()

                response = {
                    'success': True,
                    'message': f'Saved {len(notes_data)} task note(s)',
                    'file': NOTES_FILE,
                    'timestamp': datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))

                print(f"✅ Saved {len(notes_data)} task note(s) to {NOTES_FILE}")

            except Exception as e:
                # Error response
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                response = {
                    'success': False,
                    'error': str(e)
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))

                print(f"❌ Error: {e}")
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server(port=8765):
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, TaskNotesHandler)

    print(f"🚀 Task Notes Server running on http://localhost:{port}")
    print(f"📁 Saving to: {NOTES_FILE}")
    print(f"💡 Tip: Keep this running in background while using task notes workflow")
    print(f"\nPress Ctrl+C to stop")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")

if __name__ == '__main__':
    run_server()
