#!/usr/bin/env python3
"""
Markdown Browser Display Script

Converts a markdown file to HTML and displays it in the default browser.
"""

import sys
import os
import tempfile
import webbrowser
from pathlib import Path
from datetime import datetime

try:
    import markdown
except ImportError:
    print("Error: markdown library not found")
    print("Install with: pip3 install markdown")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).parent.parent.parent


def markdown_to_html(md_content: str, title: str = "Markdown Document") -> str:
    """
    Convert markdown content to HTML with styling.
    
    Args:
        md_content: Markdown content string
        title: Document title
    
    Returns:
        Complete HTML document string
    """
    # Convert markdown to HTML
    html_body = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'tables', 'toc']
    )
    
    # Create full HTML document with styling
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #fafafa;
        }}
        h1 {{
            color: #2563eb;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h2 {{
            color: #1e40af;
            margin-top: 40px;
            border-left: 4px solid #2563eb;
            padding-left: 15px;
        }}
        h3 {{
            color: #1e3a8a;
            margin-top: 30px;
        }}
        h4 {{
            color: #1e3a8a;
            margin-top: 25px;
        }}
        code {{
            background-color: #f3f4f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #1f2937;
            color: #f9fafb;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            border-left: 4px solid #2563eb;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
            color: inherit;
        }}
        blockquote {{
            border-left: 4px solid #d1d5db;
            padding-left: 20px;
            margin-left: 0;
            color: #6b7280;
            font-style: italic;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #e5e7eb;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f3f4f6;
            font-weight: 600;
            color: #1f2937;
        }}
        tr:nth-child(even) {{
            background-color: #f9fafb;
        }}
        a {{
            color: #2563eb;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul, ol {{
            padding-left: 25px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        hr {{
            border: none;
            border-top: 2px solid #e5e7eb;
            margin: 30px 0;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            margin: 20px 0;
        }}
        .meta {{
            background-color: #f3f4f6;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 0.9em;
            color: #6b7280;
        }}
    </style>
</head>
<body>
    <div class="meta">
        <strong>Document:</strong> {title}<br>
        <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    {html_body}
</body>
</html>"""
    
    return html


def display_markdown_in_browser(md_file_path: str):
    """
    Convert markdown file to HTML and display in browser.
    
    Args:
        md_file_path: Path to markdown file (relative or absolute)
    """
    # Resolve file path
    if os.path.isabs(md_file_path):
        md_path = Path(md_file_path)
    else:
        md_path = PROJECT_ROOT / md_file_path
    
    if not md_path.exists():
        print(f"Error: File not found: {md_path}")
        sys.exit(1)
    
    if not md_path.is_file():
        print(f"Error: Not a file: {md_path}")
        sys.exit(1)
    
    # Read markdown content
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Get document title (from filename or first H1)
    title = md_path.stem.replace('-', ' ').replace('_', ' ').title()
    
    # Check for H1 in content
    lines = md_content.split('\n')
    for line in lines[:10]:  # Check first 10 lines
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Convert to HTML
    html_content = markdown_to_html(md_content, title)
    
    # Create temporary HTML file
    temp_dir = tempfile.gettempdir()
    temp_file = Path(temp_dir) / f"markdown_display_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Get file URL
        file_url = f"file://{temp_file.absolute()}"
        
        # Open in browser
        print(f"📄 Converting: {md_path.name}")
        print(f"🌐 Opening in browser...")
        print(f"📁 Temporary file: {temp_file}")
        print()
        
        webbrowser.open(file_url)
        
        print("✅ Markdown displayed in browser!")
        print()
        print("Note: Temporary HTML file will remain in:")
        print(f"   {temp_file}")
        print("You can delete it manually or it will be cleaned up on system restart.")
        
    except Exception as e:
        print(f"Error creating/opening HTML file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: display_markdown_in_browser.py <path-to-markdown-file>")
        print()
        print("Example:")
        print("  python3 display_markdown_in_browser.py briefing/2025-11-11-briefing.md")
        print("  python3 display_markdown_in_browser.py clients/smythson/CONTEXT.md")
        sys.exit(1)
    
    md_file = sys.argv[1]
    display_markdown_in_browser(md_file)

