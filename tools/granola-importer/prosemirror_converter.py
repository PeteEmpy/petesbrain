"""
ProseMirror to Markdown Converter

Converts Granola's ProseMirror JSON format to clean Markdown.
"""

from typing import Dict, List, Any, Optional


class ProseMirrorConverter:
    """Converts ProseMirror JSON documents to Markdown format."""

    def __init__(self):
        """Initialize converter."""
        self.output = []
        self.list_depth = 0

    def convert(self, prosemirror_doc: Dict) -> str:
        """
        Convert a ProseMirror document to Markdown.

        Args:
            prosemirror_doc: ProseMirror JSON document structure

        Returns:
            Markdown string
        """
        self.output = []
        self.list_depth = 0

        if not prosemirror_doc:
            return ""

        # Handle nested document structure
        content = prosemirror_doc
        if isinstance(prosemirror_doc, dict):
            # Check for nested content structure
            if "last_viewed_panel" in prosemirror_doc:
                content = prosemirror_doc["last_viewed_panel"]
            if "content" in content:
                content = content["content"]

        # Process content nodes
        if isinstance(content, list):
            for node in content:
                self._process_node(node)
        elif isinstance(content, dict) and "content" in content:
            for node in content["content"]:
                self._process_node(node)

        return "\n".join(self.output).strip()

    def _process_node(self, node: Dict, in_list: bool = False) -> None:
        """
        Process a single ProseMirror node.

        Args:
            node: ProseMirror node dictionary
            in_list: Whether this node is inside a list
        """
        node_type = node.get("type", "")

        if node_type == "heading":
            level = node.get("attrs", {}).get("level", 1)
            text = self._extract_text(node)
            if text:
                self.output.append(f"{'#' * level} {text}")
                self.output.append("")

        elif node_type == "paragraph":
            text = self._extract_text(node)
            if text:
                if in_list:
                    indent = "  " * (self.list_depth - 1)
                    self.output.append(f"{indent}  {text}")
                else:
                    self.output.append(text)
                    self.output.append("")

        elif node_type == "bulletList":
            self.list_depth += 1
            items = node.get("content", [])
            for item in items:
                self._process_list_item(item)
            self.list_depth -= 1
            if self.list_depth == 0:
                self.output.append("")

        elif node_type == "orderedList":
            self.list_depth += 1
            items = node.get("content", [])
            for i, item in enumerate(items, 1):
                self._process_list_item(item, ordered=True, number=i)
            self.list_depth -= 1
            if self.list_depth == 0:
                self.output.append("")

        elif node_type == "blockquote":
            content_nodes = node.get("content", [])
            for content_node in content_nodes:
                text = self._extract_text(content_node)
                if text:
                    self.output.append(f"> {text}")
            self.output.append("")

        elif node_type == "codeBlock":
            language = node.get("attrs", {}).get("language", "")
            code = self._extract_text(node)
            if code:
                self.output.append(f"```{language}")
                self.output.append(code)
                self.output.append("```")
                self.output.append("")

        elif node_type == "horizontalRule":
            self.output.append("---")
            self.output.append("")

        elif node_type == "hardBreak":
            self.output.append("")

    def _process_list_item(self, item: Dict, ordered: bool = False, number: int = 1) -> None:
        """
        Process a list item node.

        Args:
            item: List item node
            ordered: Whether this is an ordered list
            number: Number for ordered list item
        """
        indent = "  " * (self.list_depth - 1)
        marker = f"{number}." if ordered else "-"

        content = item.get("content", [])
        if not content:
            return

        # First paragraph becomes the list item
        first_node = content[0]
        text = self._extract_text(first_node)
        if text:
            self.output.append(f"{indent}{marker} {text}")

        # Additional paragraphs are indented
        for node in content[1:]:
            self._process_node(node, in_list=True)

    def _extract_text(self, node: Dict) -> str:
        """
        Extract text content from a node, handling inline formatting.

        Args:
            node: ProseMirror node

        Returns:
            Formatted text string
        """
        if node.get("type") == "text":
            text = node.get("text", "")
            marks = node.get("marks", [])

            # Apply marks (bold, italic, code, etc.)
            for mark in marks:
                mark_type = mark.get("type", "")
                if mark_type == "bold":
                    text = f"**{text}**"
                elif mark_type == "italic":
                    text = f"*{text}*"
                elif mark_type == "code":
                    text = f"`{text}`"
                elif mark_type == "link":
                    href = mark.get("attrs", {}).get("href", "")
                    text = f"[{text}]({href})"
                elif mark_type == "strike":
                    text = f"~~{text}~~"

            return text

        # Recursively extract text from child nodes
        content = node.get("content", [])
        text_parts = []
        for child in content:
            child_text = self._extract_text(child)
            if child_text:
                text_parts.append(child_text)

        return "".join(text_parts)


def extract_transcript(document: Dict) -> Optional[str]:
    """
    Extract the full transcript from a Granola document if available.

    Args:
        document: Granola document dictionary

    Returns:
        Transcript text or None if not available
    """
    # Look for transcript in various possible locations
    transcript_content = None

    # Check for transcript field
    if "transcript" in document:
        transcript_content = document["transcript"]

    # Check for recording content
    elif "recording" in document:
        recording = document["recording"]
        if isinstance(recording, dict):
            transcript_content = recording.get("transcript") or recording.get("content")
        elif isinstance(recording, str):
            transcript_content = recording

    # Check for content with transcript type
    elif "content" in document:
        content = document["content"]
        if isinstance(content, dict) and content.get("type") == "transcript":
            transcript_content = content.get("text") or content.get("content")

    if not transcript_content:
        return None

    # Format transcript if it's structured data
    if isinstance(transcript_content, list):
        # Handle transcript as list of utterances
        lines = []
        for item in transcript_content:
            if isinstance(item, dict):
                speaker = item.get("speaker", "Unknown")
                timestamp = item.get("timestamp", "")
                text = item.get("text", "")

                if timestamp:
                    lines.append(f"**[{timestamp}] {speaker}:**")
                else:
                    lines.append(f"**{speaker}:**")

                lines.append(text)
                lines.append("")
            elif isinstance(item, str):
                lines.append(item)

        return "\n".join(lines)

    return str(transcript_content)


def fetch_external_content(url: str) -> Optional[str]:
    """
    Fetch and extract text content from an external URL.

    Args:
        url: URL to fetch

    Returns:
        Extracted text content or None if failed
    """
    try:
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    except Exception as e:
        print(f"    ⚠️  Could not fetch external content from {url}: {e}")
        return None


def fetch_granola_notes(document_id: str) -> Optional[str]:
    """
    Fetch meeting notes from Granola's public notes URL.

    Args:
        document_id: Granola document/meeting ID

    Returns:
        Markdown-formatted notes or None if failed
    """
    try:
        import requests
        import re
        import html as html_module

        notes_url = f'https://notes.granola.ai/d/{document_id}'

        response = requests.get(notes_url, timeout=30)
        response.raise_for_status()

        html_content = response.text

        # Extract HTML content from React Server Components payload
        # Pattern: self.__next_f.push([1,"...<h3>AI Tools..."])
        # The content is in escaped HTML format

        # Find all the push payloads
        # Pattern needs to handle escaped quotes: \"
        push_pattern = r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)'
        matches = re.findall(push_pattern, html_content)

        # Combine all HTML fragments
        combined_html = ''
        for match in matches:
            # Decode unicode escapes (\u003c = <) and escaped quotes (\")
            try:
                decoded = match.encode('utf-8').decode('unicode_escape')
                combined_html += decoded
            except Exception:
                # Skip malformed fragments
                continue

        # Now parse the HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(combined_html, 'html.parser')

        # Convert HTML to markdown
        markdown_lines = []

        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'ul', 'ol', 'p', 'hr']):
            if element.name == 'h1':
                markdown_lines.append(f"\n# {element.get_text(strip=True)}\n")
            elif element.name == 'h2':
                markdown_lines.append(f"\n## {element.get_text(strip=True)}\n")
            elif element.name == 'h3':
                markdown_lines.append(f"\n### {element.get_text(strip=True)}\n")
            elif element.name == 'h4':
                markdown_lines.append(f"\n#### {element.get_text(strip=True)}\n")
            elif element.name in ['ul', 'ol']:
                for li in element.find_all('li', recursive=False):
                    # Handle nested lists
                    text = li.get_text(separator=' ', strip=True)
                    # Get direct text only
                    direct_text = ''.join(li.find_all(text=True, recursive=False)).strip()
                    if not direct_text:
                        direct_text = text.split('\n')[0].strip()

                    markdown_lines.append(f"- {direct_text}")

                    # Handle nested ul/ol
                    for nested in li.find_all(['ul', 'ol'], recursive=False):
                        for nested_li in nested.find_all('li', recursive=False):
                            nested_text = nested_li.get_text(strip=True)
                            markdown_lines.append(f"  - {nested_text}")
                markdown_lines.append("")
            elif element.name == 'p':
                text = element.get_text(strip=True)
                if text:
                    markdown_lines.append(f"{text}\n")
            elif element.name == 'hr':
                markdown_lines.append("\n---\n")

        result = '\n'.join(markdown_lines)
        return result if result.strip() else None

    except Exception as e:
        print(f"    ⚠️  Could not fetch Granola notes: {e}")
        return None


if __name__ == "__main__":
    # Test conversion
    test_doc = {
        "type": "doc",
        "content": [
            {
                "type": "heading",
                "attrs": {"level": 1},
                "content": [{"type": "text", "text": "Meeting Notes"}]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "This is a "},
                    {"type": "text", "text": "test", "marks": [{"type": "bold"}]},
                    {"type": "text", "text": " document."}
                ]
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "First item"}]}
                        ]
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "Second item"}]}
                        ]
                    }
                ]
            }
        ]
    }

    converter = ProseMirrorConverter()
    markdown = converter.convert(test_doc)
    print(markdown)
