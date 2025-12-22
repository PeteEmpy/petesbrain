#!/usr/bin/env python3
"""
Simple HTTP API for saving task notes to manual-task-notes.json AND original task file
Run: python3 task-notes-api.py
Server will listen on http://localhost:5002
"""

import json
import sys
import os
import atexit
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
NOTES_FILE = PROJECT_ROOT / 'data' / 'state' / 'manual-task-notes.json'
PID_FILE = Path.home() / '.petesbrain-task-notes-server.pid'

def update_original_task(task_id, client, note_text):
    """Update the note in the original task file (clients/{client}/tasks.json or roksys/tasks.json)"""
    # Try client tasks first
    if client and client != 'unknown':
        client_tasks_path = PROJECT_ROOT / 'clients' / client / 'tasks.json'
        if client_tasks_path.exists():
            with open(client_tasks_path) as f:
                data = json.load(f)

            # Handle both formats: dict with 'tasks' key or direct list
            tasks_list = data.get('tasks', []) if isinstance(data, dict) else data

            # Find and update the task
            for task in tasks_list:
                if task.get('id') == task_id:
                    # Append note to existing notes or create new notes field
                    if 'notes' in task and task['notes']:
                        task['notes'] = task['notes'] + '\n\n' + note_text
                    else:
                        task['notes'] = note_text

                    # Write back to file (preserve original structure)
                    if isinstance(data, dict) and 'tasks' in data:
                        data['tasks'] = tasks_list

                    with open(client_tasks_path, 'w') as f:
                        json.dump(data, f, indent=2)

                    print(f'✓ Updated original task in {client_tasks_path}')
                    return True

    # Fall back to roksys/tasks.json
    roksys_tasks_path = PROJECT_ROOT / 'roksys' / 'tasks.json'
    if roksys_tasks_path.exists():
        with open(roksys_tasks_path) as f:
            data = json.load(f)

        # Handle both formats: dict with 'tasks' key or direct list
        tasks_list = data.get('tasks', []) if isinstance(data, dict) else data

        for task in tasks_list:
            if task.get('id') == task_id:
                # Append note to existing notes or create new notes field
                if 'notes' in task and task['notes']:
                    task['notes'] = task['notes'] + '\n\n' + note_text
                else:
                    task['notes'] = note_text

                # Write back to file (preserve original structure)
                if isinstance(data, dict) and 'tasks' in data:
                    data['tasks'] = tasks_list

                with open(roksys_tasks_path, 'w') as f:
                    json.dump(data, f, indent=2)

                print(f'✓ Updated original task in {roksys_tasks_path}')
                return True

    return False

class TaskNotesHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests to save notes"""
        if self.path == '/save-note':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body.decode('utf-8'))

                # Step 1: Update the original task
                task_id = data.get('task_id')
                client = data.get('client', 'unknown')
                note_text = data.get('note_text')

                update_original_task(task_id, client, note_text)

                # Step 2: Load existing manual notes
                if NOTES_FILE.exists():
                    with open(NOTES_FILE) as f:
                        notes = json.load(f)
                else:
                    notes = []

                # Create note entry for manual notes file
                note_entry = {
                    'task_id': task_id,
                    'client': client,
                    'task_title': data.get('task_title'),
                    'task_type': 'standalone',
                    'task_priority': data.get('priority', 'P2'),
                    'task_notes': data.get('due_date', 'No due date'),
                    'manual_note': note_text,
                    'timestamp': datetime.now().isoformat() + 'Z'
                }

                # Append to manual notes
                notes.append(note_entry)

                # Save back to manual notes file
                with open(NOTES_FILE, 'w') as f:
                    json.dump(notes, f, indent=2)

                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'message': 'Note saved to both task and manual notes'}).encode())

                print(f'✓ Note saved for task: {data.get("task_title")} (to both original task and manual notes)')

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())
                print(f'✗ Error saving note: {e}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/regenerate':
            try:
                import subprocess
                result = subprocess.run(
                    ['python3', str(PROJECT_ROOT / 'shared' / 'scripts' / 'generate-task-manager.py')],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode == 0:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success', 'message': 'Task manager regenerated'}).encode())
                    print('✓ Task manager regenerated via API')
                else:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'error', 'message': result.stderr}).encode())
                    print(f'✗ Error regenerating task manager: {result.stderr}')
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
                print(f'✗ Error: {e}')
        elif self.path == '/notes-count':
            try:
                count = 0
                if NOTES_FILE.exists():
                    with open(NOTES_FILE) as f:
                        notes = json.load(f)
                        count = len(notes) if isinstance(notes, list) else 0

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'count': count}).encode())

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def check_already_running():
    """Check if server already running via PID file"""
    if PID_FILE.exists():
        try:
            with open(PID_FILE) as f:
                old_pid = int(f.read().strip())

            # Check if process still exists
            os.kill(old_pid, 0)

            # Process exists - server already running
            print(f"ℹ️  Task Notes Server already running (PID {old_pid})")
            print(f"💡 If stuck, kill it: kill {old_pid}")
            sys.exit(0)  # Exit cleanly (not a failure)

        except (ProcessLookupError, ValueError):
            # Stale PID file - process doesn't exist
            print(f"🧹 Removing stale PID file")
            PID_FILE.unlink()
        except PermissionError:
            # Process exists but owned by another user
            print(f"❌ Server running as different user (PID {old_pid})")
            sys.exit(1)

    # Write current PID
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

    print(f"✅ PID file created: {PID_FILE}")

def cleanup_pid_file():
    """Remove PID file on shutdown"""
    if PID_FILE.exists():
        PID_FILE.unlink()
        print(f"🧹 PID file removed")

if __name__ == '__main__':
    # Check for duplicate instance FIRST
    check_already_running()

    # Register cleanup handler
    atexit.register(cleanup_pid_file)

    server = HTTPServer(('localhost', 5002), TaskNotesHandler)
    print('Task Notes API listening on http://localhost:5002')
    print(f'Notes file: {NOTES_FILE}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n✓ Server stopped')
        sys.exit(0)
