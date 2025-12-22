#!/usr/bin/env python3
"""
Task Manager Canonical Server

Consolidated server merging all Task Manager server functionality:
1. Serves Task Manager HTML on port 8767
2. Provides Task Notes API on port 5002
3. Includes PID file safeguards
4. Loads configuration from config.json
5. Handles CORS properly
6. Provides health check endpoints

This replaces:
- serve-task-manager.py (HTML serving)
- task-notes-api.py (API endpoints)
- save-task-notes.py (deprecated alternative)

Usage:
    python3 task-manager-server.py

Endpoints:
    Port 8767:
        GET /tasks-manager.html - Task Manager UI
        GET /health - Health check

    Port 5002:
        POST /save-note - Save manual task note
        POST /regenerate - Regenerate tasks overview
        GET /notes-count - Get manual notes count
        GET /health - Health check
"""

import json
import sys
import os
import atexit
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from typing import Dict

# Load configuration
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.json'

def load_config() -> Dict:
    """Load configuration from config.json"""
    if not CONFIG_PATH.exists():
        print(f"❌ Configuration file not found: {CONFIG_PATH}")
        sys.exit(1)

    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        sys.exit(1)

# Load configuration
CONFIG = load_config()

# Paths from configuration
BASE_DIR = Path(CONFIG['paths']['base_dir']).expanduser()
NOTES_FILE = BASE_DIR / CONFIG['paths']['state_file']
HTML_DIR = BASE_DIR / CONFIG['paths']['task_manager_dir']

# Server configuration
HTML_PORT = CONFIG['servers']['task_manager_html']['port']
API_PORT = CONFIG['servers']['task_notes_api']['port']
HTML_PID_FILE = Path(CONFIG['servers']['task_manager_html']['pid_file']).expanduser()
API_PID_FILE = Path(CONFIG['servers']['task_notes_api']['pid_file']).expanduser()

# Ensure state file directory exists
NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

class Colors:
    """Terminal colors for output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def update_original_task(task_id: str, client: str, note_text: str) -> bool:
    """Update the note in the original task file"""
    # Try client tasks first
    if client and client != 'unknown':
        client_tasks_path = BASE_DIR / 'clients' / client / 'tasks.json'
        if client_tasks_path.exists():
            try:
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

                        print(f'{Colors.GREEN}✓ Updated task in {client_tasks_path}{Colors.END}')
                        return True
            except Exception as e:
                print(f'{Colors.RED}✗ Error updating client task: {e}{Colors.END}')

    # Fall back to roksys/tasks.json
    roksys_tasks_path = BASE_DIR / 'roksys' / 'tasks.json'
    if roksys_tasks_path.exists():
        try:
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

                    print(f'{Colors.GREEN}✓ Updated task in {roksys_tasks_path}{Colors.END}')
                    return True
        except Exception as e:
            print(f'{Colors.RED}✗ Error updating roksys task: {e}{Colors.END}')

    return False

class HTMLServerHandler(SimpleHTTPRequestHandler):
    """Handler for serving HTML files on port 8767"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HTML_DIR), **kwargs)

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        # Health check endpoint
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            health = {
                'status': 'healthy',
                'port': HTML_PORT,
                'type': 'html_server',
                'timestamp': datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(health).encode())
            return

        # Serve static files
        super().do_GET()

    def log_message(self, format, *args):
        # Suppress most logging except errors
        if '200' not in str(args):
            super().log_message(format, *args)

class APIServerHandler(BaseHTTPRequestHandler):
    """Handler for API endpoints on port 5002"""

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/save-note':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body.decode('utf-8'))

                # Extract task details
                task_id = data.get('task_id')
                client = data.get('client', 'unknown')
                note_text = data.get('note_text') or data.get('manual_note', '')

                # Step 1: Update the original task
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
                response = {
                    'success': True,
                    'status': 'success',
                    'message': 'Note saved to both task and manual notes'
                }
                self.wfile.write(json.dumps(response).encode())

                print(f'{Colors.GREEN}✓ Note saved for task: {data.get("task_title")}{Colors.END}')

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {
                    'success': False,
                    'status': 'error',
                    'message': str(e)
                }
                self.wfile.write(json.dumps(response).encode())
                print(f'{Colors.RED}✗ Error saving note: {e}{Colors.END}')

        elif self.path == '/regenerate':
            try:
                # Run the generate script
                generate_script = BASE_DIR / 'generate-all-task-views.py'

                result = subprocess.run(
                    ['python3', str(generate_script)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode == 0:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    response = {
                        'success': True,
                        'status': 'success',
                        'message': 'Task views regenerated'
                    }
                    self.wfile.write(json.dumps(response).encode())
                    print(f'{Colors.GREEN}✓ Task views regenerated{Colors.END}')
                else:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    response = {
                        'success': False,
                        'status': 'error',
                        'message': result.stderr
                    }
                    self.wfile.write(json.dumps(response).encode())
                    print(f'{Colors.RED}✗ Error regenerating: {result.stderr}{Colors.END}')

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {
                    'success': False,
                    'status': 'error',
                    'message': str(e)
                }
                self.wfile.write(json.dumps(response).encode())
                print(f'{Colors.RED}✗ Error: {e}{Colors.END}')
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {'error': 'Not found'}
            self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/notes-count':
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

        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            health = {
                'status': 'healthy',
                'port': API_PORT,
                'type': 'api_server',
                'timestamp': datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(health).encode())

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {'error': 'Not found'}
            self.wfile.write(json.dumps(response).encode())

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

def check_already_running(pid_file: Path, server_name: str):
    """Check if server already running via PID file"""
    if pid_file.exists():
        try:
            with open(pid_file) as f:
                old_pid = int(f.read().strip())

            # Check if process still exists
            os.kill(old_pid, 0)

            # Process exists - server already running
            print(f"{Colors.YELLOW}ℹ️  {server_name} already running (PID {old_pid}){Colors.END}")
            print(f"{Colors.YELLOW}💡 If stuck, kill it: kill {old_pid}{Colors.END}")
            sys.exit(0)  # Exit cleanly (not a failure)

        except (ProcessLookupError, ValueError):
            # Stale PID file - process doesn't exist
            print(f"{Colors.BLUE}🧹 Removing stale PID file for {server_name}{Colors.END}")
            pid_file.unlink()
        except PermissionError:
            # Process exists but owned by another user
            print(f"{Colors.RED}❌ {server_name} running as different user (PID {old_pid}){Colors.END}")
            sys.exit(1)

    # Write current PID
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))

    print(f"{Colors.GREEN}✅ PID file created for {server_name}: {pid_file}{Colors.END}")

def cleanup_pid_files():
    """Remove PID files on shutdown"""
    for pid_file in [HTML_PID_FILE, API_PID_FILE]:
        if pid_file.exists():
            pid_file.unlink()
            print(f"{Colors.BLUE}🧹 PID file removed: {pid_file}{Colors.END}")

def run_html_server():
    """Run HTML server on port 8767"""
    try:
        httpd = HTTPServer(('localhost', HTML_PORT), HTMLServerHandler)
        print(f"{Colors.GREEN}🌐 HTML Server running on http://localhost:{HTML_PORT}/tasks-manager.html{Colors.END}")
        httpd.serve_forever()
    except Exception as e:
        print(f"{Colors.RED}❌ HTML Server error: {e}{Colors.END}")
        sys.exit(1)

def run_api_server():
    """Run API server on port 5002"""
    try:
        httpd = HTTPServer(('localhost', API_PORT), APIServerHandler)
        print(f"{Colors.GREEN}🌐 API Server running on http://localhost:{API_PORT}{Colors.END}")
        httpd.serve_forever()
    except Exception as e:
        print(f"{Colors.RED}❌ API Server error: {e}{Colors.END}")
        sys.exit(1)

def main():
    """Main entry point"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}Task Manager Canonical Server{Colors.END}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}\n")

    # Check for duplicate instances
    check_already_running(HTML_PID_FILE, "Task Manager HTML Server")
    check_already_running(API_PID_FILE, "Task Manager API Server")

    # Register cleanup handler
    atexit.register(cleanup_pid_files)

    # Print configuration
    print(f"{Colors.BOLD}Configuration:{Colors.END}")
    print(f"  Config file: {CONFIG_PATH}")
    print(f"  Version: {CONFIG.get('version', 'unknown')}")
    print(f"  HTML directory: {HTML_DIR}")
    print(f"  Notes file: {NOTES_FILE}")
    print()

    # Start both servers in separate threads
    print(f"{Colors.BOLD}Starting servers...{Colors.END}\n")

    html_thread = threading.Thread(target=run_html_server, daemon=True)
    api_thread = threading.Thread(target=run_api_server, daemon=True)

    html_thread.start()
    api_thread.start()

    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Task Manager Ready{Colors.END}")
    print(f"\n{Colors.BOLD}URLs:{Colors.END}")
    print(f"  Task Manager: http://localhost:{HTML_PORT}/tasks-manager.html")
    print(f"  Health (HTML): http://localhost:{HTML_PORT}/health")
    print(f"  Health (API): http://localhost:{API_PORT}/health")
    print(f"\n{Colors.BOLD}API Endpoints:{Colors.END}")
    print(f"  POST http://localhost:{API_PORT}/save-note")
    print(f"  POST http://localhost:{API_PORT}/regenerate")
    print(f"  GET  http://localhost:{API_PORT}/notes-count")
    print(f"\n{Colors.YELLOW}Press Ctrl+C to stop{Colors.END}\n")

    try:
        # Keep main thread alive
        while True:
            html_thread.join(timeout=1)
            api_thread.join(timeout=1)
            if not html_thread.is_alive() or not api_thread.is_alive():
                print(f"{Colors.RED}❌ Server thread died, exiting{Colors.END}")
                sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BLUE}👋 Servers stopped{Colors.END}\n")
        sys.exit(0)

if __name__ == '__main__':
    main()
