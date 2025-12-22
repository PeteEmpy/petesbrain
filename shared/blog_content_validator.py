#!/usr/bin/env python3
"""
Blog Content Validator

Validates blog post content BEFORE publishing to prevent client information leakage.
Used by weekly-blog-generator to ensure NO client-specific information appears in public posts.

CRITICAL: This validator MUST be run before ANY blog post is published.
"""

import re
from typing import List, Dict, Tuple
from pathlib import Path

# Client names to flag (all clients, past and present)
CLIENT_NAMES = [
    # Current clients
    'devonshire', 'devonshire hotels',
    'smythson',
    'tree2mydoor', 'tree 2 my door', 'tree to my door',
    'superspace',
    'crowd control',
    'uno lights', 'accessories for the home',
    'bmpm',
    'nma', 'national design academy',
    'nda',

    # Past clients (if any need to be added)
]

# Generic client-related keywords
CLIENT_KEYWORDS = [
    'my client', 'our client', 'a client', 'the client',
    'hotel client', 'fashion client', 'ecommerce client',
    'client\'s account', 'client\'s campaign',
    'working with a', 'working with this',
]

# Internal/meeting language
INTERNAL_KEYWORDS = [
    'google rep', 'our google rep',
    'meeting with google', 'call with google',
    'internal meeting', 'team meeting',
    'discussed with', 'talked to our rep',
    'in our meeting', 'during the call',
]

# Specific campaign/strategy language (too specific for public blog)
SPECIFIC_CAMPAIGN_KEYWORDS = [
    'haemorrhaging revenue', 'hemorrhaging revenue',
    'losing money compared to',
    'performance max campaign for a',
    'shopping campaign for a',
    'i uploaded', 'i tested this with',
    'i implemented', 'we implemented for',
]


def validate_blog_content(
    title: str,
    content: str,
    strict_mode: bool = True
) -> Tuple[bool, List[Dict[str, str]]]:
    """
    Validate blog post content for client information leakage.

    Args:
        title: Blog post title
        content: Blog post HTML content
        strict_mode: If True, flags generic keywords too (default True)

    Returns:
        Tuple of (is_valid, issues_found)
        - is_valid: False if client info detected
        - issues_found: List of dicts with {category, keyword, context}
    """

    # Strip HTML tags for text analysis
    text_content = re.sub(r'<[^<]+?>', '', content)
    combined_text = f"{title} {text_content}".lower()

    issues = []

    # Check 1: Client names
    for client_name in CLIENT_NAMES:
        if client_name.lower() in combined_text:
            context = _extract_context(combined_text, client_name.lower())
            issues.append({
                'category': 'CLIENT_NAME',
                'keyword': client_name,
                'context': context,
                'severity': 'CRITICAL'
            })

    # Check 2: Generic client keywords
    for keyword in CLIENT_KEYWORDS:
        if keyword.lower() in combined_text:
            context = _extract_context(combined_text, keyword.lower())
            issues.append({
                'category': 'CLIENT_REFERENCE',
                'keyword': keyword,
                'context': context,
                'severity': 'HIGH'
            })

    # Check 3: Internal meeting language
    if strict_mode:
        for keyword in INTERNAL_KEYWORDS:
            if keyword.lower() in combined_text:
                context = _extract_context(combined_text, keyword.lower())
                issues.append({
                    'category': 'INTERNAL_LANGUAGE',
                    'keyword': keyword,
                    'context': context,
                    'severity': 'MEDIUM'
                })

    # Check 4: Specific campaign language
    if strict_mode:
        for keyword in SPECIFIC_CAMPAIGN_KEYWORDS:
            if keyword.lower() in combined_text:
                context = _extract_context(combined_text, keyword.lower())
                issues.append({
                    'category': 'SPECIFIC_CAMPAIGN',
                    'keyword': keyword,
                    'context': context,
                    'severity': 'HIGH'
                })

    # Content is valid only if NO issues found
    is_valid = len(issues) == 0

    return is_valid, issues


def _extract_context(text: str, keyword: str, window: int = 100) -> str:
    """Extract surrounding context for a keyword match"""
    try:
        pos = text.lower().find(keyword.lower())
        if pos == -1:
            return ""

        start = max(0, pos - window)
        end = min(len(text), pos + len(keyword) + window)

        context = text[start:end]
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."

        return context.strip()
    except:
        return ""


def format_validation_report(
    title: str,
    is_valid: bool,
    issues: List[Dict[str, str]]
) -> str:
    """Format validation results as a readable report"""

    if is_valid:
        return f"""
✅ VALIDATION PASSED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Blog Post: {title}
Status: SAFE TO PUBLISH
No client information detected.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    report = f"""
🔴 VALIDATION FAILED - CLIENT INFORMATION DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Blog Post: {title}
Status: DO NOT PUBLISH
Issues Found: {len(issues)}

"""

    # Group by severity
    critical_issues = [i for i in issues if i['severity'] == 'CRITICAL']
    high_issues = [i for i in issues if i['severity'] == 'HIGH']
    medium_issues = [i for i in issues if i['severity'] == 'MEDIUM']

    if critical_issues:
        report += "🚨 CRITICAL ISSUES (Client Names Detected):\n"
        for issue in critical_issues:
            report += f"   • {issue['keyword']}\n"
            report += f"     Context: {issue['context'][:100]}...\n\n"

    if high_issues:
        report += "⚠️  HIGH SEVERITY (Client References):\n"
        for issue in high_issues:
            report += f"   • {issue['keyword']}\n"
            report += f"     Context: {issue['context'][:100]}...\n\n"

    if medium_issues:
        report += "⚠️  MEDIUM SEVERITY (Internal Language):\n"
        for issue in medium_issues:
            report += f"   • {issue['keyword']}\n"
            report += f"     Context: {issue['context'][:100]}...\n\n"

    report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    report += "ACTION REQUIRED: Remove client-specific content before publishing.\n"
    report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

    return report


def validate_and_report(title: str, content: str, strict_mode: bool = True) -> bool:
    """
    Validate blog content and print report.
    Returns True if valid, False if issues detected.
    """
    is_valid, issues = validate_blog_content(title, content, strict_mode)
    report = format_validation_report(title, is_valid, issues)
    print(report)
    return is_valid


# CLI usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python blog_content_validator.py <title> <content_file>")
        print("Example: python blog_content_validator.py 'My Blog Post' content.html")
        sys.exit(1)

    title = sys.argv[1]
    content_file = Path(sys.argv[2])

    if not content_file.exists():
        print(f"ERROR: Content file not found: {content_file}")
        sys.exit(1)

    with open(content_file, 'r') as f:
        content = f.read()

    is_valid = validate_and_report(title, content, strict_mode=True)

    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)
