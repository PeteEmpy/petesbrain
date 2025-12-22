#!/usr/bin/env python3
"""
Generate team update emails for Alex Clarke - P9 Status
December 19, 2025
"""

import os
import sys
from pathlib import Path

# Add shared module to path
sys.path.insert(0, '/Users/administrator/Documents/PetesBrain.nosync/shared')
from email_template import render_email, save_email_draft

# Email 1: Quick Team Update
content_quick = '''
    <p><strong>P9 Status Update - December 19</strong></p>

    <p>Quick heads up on where we are with P9:</p>

    <p><strong>Current Position (Dec 1-19)</strong><br>
    • Spend: £117,889 (69% of £171k budget)<br>
    • Revenue: £877,085<br>
    • ROAS: 744% (excellent)</p>

    <p><strong>Today's Performance</strong><br>
    UK showing strength at £2,599 revenue from £1,406 spend. USA particularly strong at 1184% ROAS.</p>

    <p><strong>Trajectory</strong><br>
    On track to hit £1.2M+ revenue. Sale launch Christmas Eve 6pm will drive final push.</p>

    <p>Full analysis to follow.</p>
'''

html_quick = render_email(
    content=content_quick,
    recipient_name="Alex",
    sender_name="Peter",
    sign_off="Best"
)

# Email 2: Detailed P9 Status Report
content_detailed = '''
    <p><strong>P9 Performance Analysis & Final Week Strategy</strong></p>

    <p>Here's the comprehensive P9 status as we head into the critical final week.</p>

    <p><strong>📊 Performance Through December 19</strong></p>

    <table>
        <tr>
            <th>Account</th>
            <th>Spend</th>
            <th>Revenue</th>
            <th>ROAS</th>
        </tr>
        <tr>
            <td>UK</td>
            <td>£58,287</td>
            <td>£419,076</td>
            <td>719%</td>
        </tr>
        <tr>
            <td>USA</td>
            <td>£34,931</td>
            <td>£268,425</td>
            <td>768%</td>
        </tr>
        <tr>
            <td>EUR</td>
            <td>£12,697</td>
            <td>£100,542</td>
            <td>792%</td>
        </tr>
        <tr>
            <td>ROW</td>
            <td>£5,436</td>
            <td>£49,532</td>
            <td>911%</td>
        </tr>
        <tr style="background-color: #f0f0f0;">
            <td><strong>TOTAL</strong></td>
            <td><strong>£117,889</strong></td>
            <td><strong>£877,085</strong></td>
            <td><strong>744%</strong></td>
        </tr>
    </table>

    <p><strong>📈 Budget Pacing</strong></p>

    <p>• <strong>Budget Used:</strong> £117,889 of £171,128 (68.9%)<br>
    • <strong>Days Elapsed:</strong> 19 of 28 (67.9%)<br>
    • <strong>Remaining Budget:</strong> £53,239<br>
    • <strong>Days Remaining:</strong> 9 days</p>

    <p>We're tracking perfectly on budget - 68.9% spent in 67.9% of the time.</p>

    <p><strong>🎯 Final 9 Days Strategy (Dec 20-28)</strong></p>

    <table>
        <tr>
            <th>Phase</th>
            <th>Dates</th>
            <th>Budget</th>
            <th>Focus</th>
        </tr>
        <tr>
            <td><strong>UK Last Orders</strong></td>
            <td>Dec 20-21</td>
            <td>£10,000</td>
            <td>Maximum UK push before cutoff</td>
        </tr>
        <tr>
            <td><strong>Pre-Sale Quiet</strong></td>
            <td>Dec 22-23</td>
            <td>£2,000</td>
            <td>Minimal spend, prep for sale</td>
        </tr>
        <tr>
            <td><strong>Sale Launch</strong></td>
            <td>Dec 24 (6pm)</td>
            <td>£3,000</td>
            <td>Ramp up from 6pm</td>
        </tr>
        <tr>
            <td><strong>Christmas Day</strong></td>
            <td>Dec 25</td>
            <td>£2,000</td>
            <td>Moderate coverage</td>
        </tr>
        <tr>
            <td><strong>Boxing Day Spike</strong></td>
            <td>Dec 26</td>
            <td>£10,000</td>
            <td>Maximum all regions</td>
        </tr>
        <tr>
            <td><strong>Sale Continuation</strong></td>
            <td>Dec 27-28</td>
            <td>£12,000</td>
            <td>Strong finish</td>
        </tr>
        <tr style="background-color: #f0f0f0;">
            <td><strong>Total Allocated</strong></td>
            <td></td>
            <td><strong>£39,000</strong></td>
            <td></td>
        </tr>
    </table>

    <p>This leaves £14,239 buffer for opportunities or to scale Boxing Day further if performance warrants.</p>

    <p><strong>💰 Revenue Projections</strong></p>

    <p>Based on current performance and historical sale period data:</p>

    <p>• <strong>Conservative:</strong> £1.15M (assuming 600% ROAS on remaining spend)<br>
    • <strong>Likely:</strong> £1.22M (assuming 800% ROAS matching current performance)<br>
    • <strong>Optimistic:</strong> £1.35M+ (if sale period hits 1000%+ ROAS as per 2024)</p>

    <p>Last year's Boxing Day delivered exceptional results:<br>
    • UK: 1205% ROAS<br>
    • USA: 1638% ROAS<br>
    • EUR: 2929% ROAS</p>

    <p><strong>🎄 Key Actions for Next 48 Hours</strong></p>

    <p>1. <strong>Tomorrow (Dec 20):</strong> Ensure UK campaigns at maximum for last full delivery day<br>
    2. <strong>Saturday (Dec 21):</strong> Monitor UK last orders, prepare USA/EUR for sale reactivation<br>
    3. <strong>Sunday (Dec 22):</strong> Reduce to minimum, verify sale launch timing configured</p>

    <p><strong>📝 Critical Reminders</strong></p>

    <p>• Sale goes live at <strong>6pm on Christmas Eve</strong><br>
    • All regions reactivate for sale (even post-delivery cutoff)<br>
    • Boxing Day historically our strongest day - ensure budget ready<br>
    • P9 ends December 28 (not 31st)</p>

    <p><strong>Summary</strong></p>

    <p>We're in an excellent position heading into the final stretch. Current ROAS of 744% gives us confidence to maintain spend levels through the sale period. The December 15-17 budget increase was the right call - it captured strong demand without compromising overall pacing.</p>

    <p>With £53k remaining and the sale period ahead, we're set up for a strong finish to Q4. I'll monitor closely through the weekend and ensure we're ready for the sale launch.</p>

    <p>Let me know if you need any adjustments to the final week strategy.</p>
'''

html_detailed = render_email(
    content=content_detailed,
    recipient_name="Alex",
    sender_name="Peter",
    sign_off="Best"
)

# Save both emails
filepath_quick = "/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/documents/email-draft-2025-12-19-p9-team-update.html"
filepath_detailed = "/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/documents/email-draft-2025-12-19-p9-detailed-status.html"

save_email_draft(html_quick, filepath_quick, open_in_browser=True)
print(f"✅ Quick team update saved to: {filepath_quick}")

save_email_draft(html_detailed, filepath_detailed, open_in_browser=True)
print(f"✅ Detailed P9 status saved to: {filepath_detailed}")