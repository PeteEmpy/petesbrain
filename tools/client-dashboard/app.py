#!/usr/bin/env python3
"""
Client Dashboard - Flask Web Application

Browser-based dashboard for viewing client information and managing tasks.
"""

from flask import Flask, render_template, request, jsonify, send_file, abort
from pathlib import Path
import sys
import re
import markdown
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

CLIENTS_DIR = PROJECT_ROOT / 'clients'
TODO_DIR = PROJECT_ROOT / 'todo'
ROKSYS_DIR = PROJECT_ROOT / 'roksys'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'petesbrain-client-dashboard-local-only'

# Add markdown filter to Jinja2
@app.template_filter('markdown')
def markdown_filter(text):
    return markdown.markdown(text, extensions=['fenced_code', 'tables', 'codehilite'])

# Cache for file listings (5 minute TTL)
_file_cache = {}
_cache_timestamps = {}


def get_all_clients() -> List[str]:
    """Get list of all client folder names"""
    if not CLIENTS_DIR.exists():
        return []
    
    clients = [
        d.name for d in CLIENTS_DIR.iterdir() 
        if d.is_dir() and not d.name.startswith('_')
    ]
    return sorted(clients)


def parse_task_file(file_path: Path) -> Optional[Dict]:
    """Parse a todo markdown file and extract task information"""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Extract title (first line after #)
        title_match = re.match(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem
        
        # Extract metadata
        created = None
        source = None
        google_task_id = None
        
        for line in content.split('\n'):
            if line.startswith('**Created:**'):
                created_match = re.search(r'\*\*Created:\*\*\s+(.+)', line)
                if created_match:
                    created = created_match.group(1).strip()
            elif line.startswith('**Source:**'):
                source_match = re.search(r'\*\*Source:\*\*\s+(.+)', line)
                if source_match:
                    source = source_match.group(1).strip()
            elif line.startswith('**Google Task ID:**'):
                task_id_match = re.search(r'\*\*Google Task ID:\*\*\s+(.+)', line)
                if task_id_match:
                    google_task_id = task_id_match.group(1).strip()
        
        # Extract status
        status = 'pending'
        if re.search(r'- \[x\]', content, re.IGNORECASE):
            status = 'completed'
        elif re.search(r'- \[ \]', content):
            status = 'pending'
        
        # Extract details section
        details_match = re.search(r'## Details\s*\n\n(.*?)(?=\n## |$)', content, re.DOTALL)
        details = details_match.group(1).strip() if details_match else ''
        
        # Extract due date
        due_date = None
        due_match = re.search(r'Due:\s*(.+)', content, re.IGNORECASE)
        if due_match:
            due_date = due_match.group(1).strip()
        
        # Detect client from title/content
        client = detect_client_from_task(title, details)
        
        return {
            'filename': file_path.name,
            'title': title,
            'status': status,
            'created': created,
            'source': source,
            'google_task_id': google_task_id,
            'details': details,
            'due_date': due_date,
            'client': client,
            'content': content,
            'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        }
    except Exception as e:
        print(f"Error parsing task file {file_path}: {e}")
        return None


def detect_client_from_task(title: str, details: str) -> Optional[str]:
    """Detect client name from task title or details"""
    clients = get_all_clients()
    search_text = f"{title} {details}".lower()
    
    # Also check for "Client:" prefix in details
    client_match = re.search(r'client:\s*([^\n]+)', details, re.IGNORECASE)
    if client_match:
        client_name = client_match.group(1).strip().lower()
        # Try to match against known clients
        for client in clients:
            if client.lower() == client_name or client.replace('-', ' ').lower() == client_name:
                return client
    
    for client in clients:
        # Check for exact client name match
        client_display = client.replace('-', ' ')
        if client in search_text or client_display in search_text:
            return client
        
        # Check for client in brackets
        if f"[{client}]" in title or f"[{client_display}]" in title:
            return client
    
    return None


def get_all_tasks() -> List[Dict]:
    """Get all tasks from todo directory"""
    if not TODO_DIR.exists():
        return []
    
    tasks = []
    for file_path in TODO_DIR.glob('*.md'):
        task = parse_task_file(file_path)
        if task:
            tasks.append(task)
    
    return sorted(tasks, key=lambda x: x.get('modified', ''), reverse=True)


def get_client_tasks(client_name: str) -> List[Dict]:
    """Get tasks for a specific client"""
    all_tasks = get_all_tasks()
    return [t for t in all_tasks if t.get('client') == client_name]


def safe_path(base: Path, user_path: str) -> Path:
    """Safely resolve a user-provided path within base directory"""
    # Remove any leading slashes and resolve
    user_path = user_path.lstrip('/')
    resolved = (base / user_path).resolve()
    
    # Ensure resolved path is within base
    try:
        resolved.relative_to(base.resolve())
    except ValueError:
        abort(403)  # Forbidden - path outside base
    
    return resolved


@app.route('/')
def index():
    """Main dashboard with all clients"""
    clients = get_all_clients()
    
    # Get stats for each client
    client_stats = []
    all_tasks = get_all_tasks()
    
    for client in clients:
        client_tasks = [t for t in all_tasks if t.get('client') == client]
        pending_tasks = [t for t in client_tasks if t.get('status') == 'pending']
        
        # Get last activity (most recent file modification)
        client_dir = CLIENTS_DIR / client
        last_activity = None
        if client_dir.exists():
            try:
                # Find most recently modified file
                files = list(client_dir.rglob('*'))
                if files:
                    most_recent = max(files, key=lambda p: p.stat().st_mtime if p.is_file() else 0)
                    if most_recent.is_file():
                        last_activity = datetime.fromtimestamp(most_recent.stat().st_mtime)
            except Exception:
                pass
        
        # Get recent tasks (3 most recent)
        recent_tasks = sorted(client_tasks, key=lambda x: x.get('modified', ''), reverse=True)[:3]
        
        client_stats.append({
            'name': client,
            'display_name': client.replace('-', ' ').title(),
            'pending_count': len(pending_tasks),
            'total_tasks': len(client_tasks),
            'last_activity': last_activity,
            'recent_tasks': recent_tasks
        })
    
    return render_template('index.html', clients=client_stats)


@app.route('/client/<client_name>')
def client_detail(client_name: str):
    """Client detail page"""
    client_dir = CLIENTS_DIR / client_name
    
    if not client_dir.exists():
        abort(404)
    
    # Get client tasks
    client_tasks = get_client_tasks(client_name)
    
    # Get CONTEXT.md content
    context_file = client_dir / 'CONTEXT.md'
    context_content = None
    if context_file.exists():
        context_content = context_file.read_text(encoding='utf-8')
    
    # Get file structure
    files = get_client_files(client_dir)
    
    return render_template('client.html', 
                         client_name=client_name,
                         client_display=client_name.replace('-', ' ').title(),
                         tasks=client_tasks,
                         context_content=context_content,
                         files=files)


@app.route('/tasks')
def tasks_page():
    """Task management page"""
    all_tasks = get_all_tasks()
    clients = get_all_clients()
    
    return render_template('tasks.html', tasks=all_tasks, clients=clients)


@app.route('/api/tasks')
def api_tasks():
    """API endpoint for all tasks"""
    tasks = get_all_tasks()
    return jsonify({'tasks': tasks})


@app.route('/api/task/<filename>')
def api_task(filename: str):
    """API endpoint for single task"""
    task_file = TODO_DIR / filename
    if not task_file.exists():
        abort(404)
    
    task = parse_task_file(task_file)
    if not task:
        abort(500)
    
    return jsonify(task)


@app.route('/api/task/create', methods=['POST'])
def api_create_task():
    """Create a new task"""
    data = request.get_json()
    
    title = data.get('title', '').strip()
    details = data.get('details', '').strip()
    due_date = data.get('due_date', '').strip()
    client = data.get('client', '').strip()
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    # Create filename
    safe_title = re.sub(r'[^a-z0-9-]', '-', title.lower())
    safe_title = re.sub(r'-+', '-', safe_title).strip('-')[:50]
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f"{timestamp}-{safe_title}.md"
    task_path = TODO_DIR / filename
    
    # Build task content
    content = f"# {title}\n\n"
    content += f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    
    if client:
        content += f"**Client:** {client}\n"
    
    if due_date:
        content += f"**Due Date:** {due_date}\n"
    
    content += f"\n## Details\n\n{details}\n\n"
    content += "## Status\n\n- [ ] Todo\n\n"
    content += "## Notes\n\n"
    
    # Write file
    TODO_DIR.mkdir(parents=True, exist_ok=True)
    task_path.write_text(content, encoding='utf-8')
    
    # Parse and return
    task = parse_task_file(task_path)
    return jsonify(task), 201


@app.route('/api/task/<filename>/update', methods=['PUT'])
def api_update_task(filename: str):
    """Update an existing task"""
    task_file = TODO_DIR / filename
    if not task_file.exists():
        abort(404)
    
    data = request.get_json()
    
    # Read current content
    current_content = task_file.read_text(encoding='utf-8')
    
    # Update title if provided
    if 'title' in data:
        current_content = re.sub(r'^#\s+.+$', f"# {data['title']}", current_content, flags=re.MULTILINE)
    
    # Update details if provided
    if 'details' in data:
        details_section = f"## Details\n\n{data['details']}\n\n"
        current_content = re.sub(r'## Details\s*\n\n.*?(?=\n## |$)', details_section, current_content, flags=re.DOTALL)
    
    # Update due date if provided
    if 'due_date' in data:
        if re.search(r'\*\*Due Date:\*\*', current_content):
            current_content = re.sub(r'\*\*Due Date:\*\*.*', f"**Due Date:** {data['due_date']}", current_content)
        else:
            # Insert after Created line
            current_content = re.sub(r'(\*\*Created:\*\*.*\n)', r'\1**Due Date:** ' + data['due_date'] + '\n', current_content)
    
    # Write back
    task_file.write_text(current_content, encoding='utf-8')
    
    task = parse_task_file(task_file)
    return jsonify(task)


@app.route('/api/task/<filename>/complete', methods=['PUT'])
def api_complete_task(filename: str):
    """Mark a task as complete"""
    task_file = TODO_DIR / filename
    if not task_file.exists():
        abort(404)
    
    content = task_file.read_text(encoding='utf-8')
    
    # Replace checkbox
    content = re.sub(r'- \[ \]', '- [x]', content)
    content = re.sub(r'- \[x\]', '- [x]', content, flags=re.IGNORECASE)
    
    # Add completed date if not present
    if '**Completed:**' not in content:
        completed_line = f"**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        content = re.sub(r'(\*\*Created:\*\*.*\n)', r'\1' + completed_line, content)
    
    task_file.write_text(content, encoding='utf-8')
    
    task = parse_task_file(task_file)
    return jsonify(task)


@app.route('/api/task/<filename>', methods=['DELETE'])
def api_delete_task(filename: str):
    """Delete (archive) a task"""
    task_file = TODO_DIR / filename
    if not task_file.exists():
        abort(404)
    
    # Create archive directory
    archive_dir = TODO_DIR / '_archived'
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Move to archive
    archive_path = archive_dir / filename
    task_file.rename(archive_path)
    
    return jsonify({'status': 'deleted'})


@app.route('/api/client/<client_name>/files')
def api_client_files(client_name: str):
    """Get file listing for a client"""
    client_dir = CLIENTS_DIR / client_name
    if not client_dir.exists():
        abort(404)
    
    files = get_client_files(client_dir)
    return jsonify({'files': files})


@app.route('/api/client/<client_name>/context')
def api_client_context(client_name: str):
    """Get CONTEXT.md content for a client"""
    context_file = CLIENTS_DIR / client_name / 'CONTEXT.md'
    if not context_file.exists():
        abort(404)
    
    content = context_file.read_text(encoding='utf-8')
    return jsonify({'content': content})


@app.route('/api/file/view')
def api_file_view():
    """View file content"""
    file_path = request.args.get('path', '')
    if not file_path:
        abort(400)
    
    # Resolve path safely
    resolved_path = safe_path(PROJECT_ROOT, file_path)
    
    if not resolved_path.exists() or not resolved_path.is_file():
        abort(404)
    
    # Determine file type
    ext = resolved_path.suffix.lower()
    
    if ext == '.md':
        content = resolved_path.read_text(encoding='utf-8')
        html = markdown.markdown(content, extensions=['fenced_code', 'tables'])
        return jsonify({'type': 'markdown', 'content': html})
    elif ext == '.html':
        content = resolved_path.read_text(encoding='utf-8')
        return jsonify({'type': 'html', 'content': content})
    elif ext in ['.png', '.jpg', '.jpeg', '.gif']:
        return jsonify({'type': 'image', 'path': str(resolved_path.relative_to(PROJECT_ROOT))})
    else:
        # Return as text
        try:
            content = resolved_path.read_text(encoding='utf-8')
            return jsonify({'type': 'text', 'content': content})
        except:
            return jsonify({'type': 'binary', 'path': str(resolved_path.relative_to(PROJECT_ROOT))})


@app.route('/api/file/download')
def api_file_download():
    """Download a file"""
    file_path = request.args.get('path', '')
    if not file_path:
        abort(400)
    
    resolved_path = safe_path(PROJECT_ROOT, file_path)
    
    if not resolved_path.exists() or not resolved_path.is_file():
        abort(404)
    
    return send_file(str(resolved_path), as_attachment=True)


def get_client_files(client_dir: Path, base_path: Optional[Path] = None) -> List[Dict]:
    """Get file structure for a client directory"""
    if base_path is None:
        base_path = client_dir
    
    files = []
    
    try:
        for item in sorted(client_dir.iterdir()):
            if item.name.startswith('.') or item.name.startswith('_'):
                continue
            
            relative_path = item.relative_to(base_path)
            
            if item.is_dir():
                files.append({
                    'name': item.name,
                    'type': 'directory',
                    'path': str(relative_path),
                    'children': get_client_files(item, base_path)
                })
            else:
                files.append({
                    'name': item.name,
                    'type': 'file',
                    'path': str(relative_path),
                    'size': item.stat().st_size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat(),
                    'extension': item.suffix.lower()
                })
    except PermissionError:
        pass
    
    return files


if __name__ == '__main__':
    import sys
    app.run(debug=True, host='127.0.0.1', port=5002)

