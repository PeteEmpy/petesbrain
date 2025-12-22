#!/usr/bin/env python3
"""
Generate team update email for Alex Clarke - P9 Status Evening Update
December 19, 2025 (Evening)
"""

import os
import sys
from pathlib import Path

# Add shared module to path
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain.nosync/shared')
from email_template import render_email, save_email_draft

# Email: Quick Team Update (Evening Version)
content_quick = '''
    <p><strong>P9 Update - Heading into Final Week</strong></p>

    <p>Quick evening update as we close out the 19th:</p>

    <p><strong>Where We Stand</strong><br>
    • Spent: £117,889 of £171k budget (69%)<br>
    • Revenue to date: £877,085<br>
    • ROAS: 744% (strong performance continuing)</p>

    <p><strong>Final Push (Dec 20-28)</strong><br>
    • Tomorrow & Saturday: Max push for UK last orders<br>
    • Sunday: Scale back pre-sale<br>
    • Christmas Eve: Sale launches 6pm - all regions reactivate</p>

    <p><strong>Trajectory</strong><br>
    £53k budget remaining, positioned well for £1.2M+ total revenue. Boxing Day looking promising based on current momentum.</p>

    <p>Will monitor closely through the weekend.</p>
'''

html_quick = render_email(
    content=content_quick,
    recipient_name="Alex",
    sender_name="Peter",
    sign_off="Best"
)

# Save email
filepath_quick = "/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/documents/email-draft-2025-12-19-evening-p9-update.html"

save_email_draft(html_quick, filepath_quick, open_in_browser=True)
print(f"✅ Evening team update saved to: {filepath_quick}")