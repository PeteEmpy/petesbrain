# NDA Automated Scripts

## Enrolment File Manager

**Script**: `enrolment-file-manager.py`

### Purpose

Automatically monitors emails from Paul Reilly (pk@nda.ac.uk) and extracts weekly enrolment data attachments. The system maintains current "active" versions of enrolment files and archives previous versions with datestamps.

### What It Does

1. **Monitors Gmail** for emails from pk@nda.ac.uk
2. **Extracts attachments**:
   - "NDA UK Enrolments 25-26.xlsx" → saved as `NDA-UK-Enrolments-ACTIVE.xlsx`
   - "NDA International Enrolments 25-26.xlsx" → saved as `NDA-International-Enrolments-ACTIVE.xlsx`
3. **Archives old versions**: Before updating, moves current active file to `history/` with datestamp
4. **Tracks processed emails**: Prevents duplicate processing via state file

### File Structure

```
clients/national-design-academy/
├── enrolments/
│   ├── NDA-UK-Enrolments-ACTIVE.xlsx          # Always current
│   ├── NDA-International-Enrolments-ACTIVE.xlsx  # Always current
│   ├── .processed-emails.json                   # State tracking
│   └── history/
│       ├── NDA-UK-Enrolments-2025-10-20.xlsx
│       ├── NDA-International-Enrolments-2025-10-20.xlsx
│       ├── NDA-UK-Enrolments-2025-10-27.xlsx
│       └── NDA-International-Enrolments-2025-10-27.xlsx
```

### Automation

**Schedule**: Runs every 6 hours via LaunchAgent
**LaunchAgent**: `com.petesbrain.nda-enrolments`
**Location**: `~/Library/LaunchAgents/com.petesbrain.nda-enrolments.plist`

### Manual Execution

To run the script manually:

```bash
GMAIL_USER="petere@roksys.co.uk" \
GMAIL_APP_PASSWORD="your-password" \
python3 /Users/administrator/Documents/PetesBrain/clients/national-design-academy/scripts/enrolment-file-manager.py
```

Or with environment variables already set in `~/.bashrc`:

```bash
python3 /Users/administrator/Documents/PetesBrain/clients/national-design-academy/scripts/enrolment-file-manager.py
```

### Checking Status

**View logs**:
```bash
tail -50 ~/.petesbrain-nda-enrolments.log
```

**Check LaunchAgent status**:
```bash
launchctl list | grep nda-enrolments
```

**View processed emails state**:
```bash
cat /Users/administrator/Documents/PetesBrain/clients/national-design-academy/enrolments/.processed-emails.json
```

### Troubleshooting

**Script not running automatically**:
```bash
# Reload the LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.petesbrain.nda-enrolments.plist
launchctl load ~/Library/LaunchAgents/com.petesbrain.nda-enrolments.plist
```

**Check for errors**:
```bash
tail -100 ~/.petesbrain-nda-enrolments.log | grep ERROR
```

**Gmail connection issues**:
- Verify `GMAIL_APP_PASSWORD` is set correctly in LaunchAgent plist
- Check Gmail app password hasn't expired
- Ensure IMAP is enabled in Gmail settings

**Files not updating**:
- Check if emails are actually from pk@nda.ac.uk (sender must match exactly)
- Verify attachment filenames contain "NDA UK Enrolments" or "NDA International Enrolments"
- Check state file to see if email was already processed

### Why This Matters

**Business Value**: Enrolment data represents actual revenue outcomes from Google Ads lead generation. By automatically tracking this data:
- Calculate true ROAS (not just cost per lead, but cost per actual enrolment/revenue)
- Identify which campaigns drive applications vs which drive actual enrolments
- Track conversion rate from application to enrolment by traffic source
- Measure lifetime value and optimize bidding accordingly

**Data Flow**:
1. Google Ads drives traffic → Applications
2. Applications tracked in Google Ads (leads)
3. Applications convert to enrolments (captured in weekly emails)
4. Enrolments = Revenue (tuition fees)
5. **This script captures step 3-4 automatically**

### Configuration

The script configuration is embedded in the script itself:

- `SENDER_EMAIL`: pk@nda.ac.uk (Paul Reilly)
- `FILE_MAPPINGS`: Pattern matching for attachment filenames
- `ENROLMENTS_DIR`: Target directory for active files
- `HISTORY_DIR`: Archive directory for old versions

To modify behavior, edit the constants at the top of `enrolment-file-manager.py`.

---

## Enrolment Analytics Script

**Script**: `create-monthly-comparison-chart.py`

### Purpose

Creates professional data visualizations of international enrolment trends for client reporting and analysis.

### What It Does

1. **Reads enrolment data** from `NDA-International-Enrolments-ACTIVE.xlsx`
2. **Analyzes data** by academic year and calendar month
3. **Generates professional chart** with:
   - Last 4 academic years comparison
   - 12-month X-axis (Jan-Dec) for year-over-year comparison
   - Professional Roksys branding (small logo in bottom-right)
   - High resolution (2700x1500px at 150 DPI)
4. **Saves chart** to `../enrolments/nda-international-by-month-comparison.png`

### How to Run

```bash
cd /Users/administrator/Documents/PetesBrain/clients/national-design-academy/scripts
.venv/bin/python3 create-monthly-comparison-chart.py
```

### View the Chart

```bash
open ../enrolments/nda-international-by-month-comparison.png
```

### When to Run

- **After new enrolment data arrives** (automatically every 6 hours via enrolment-file-manager)
- **Before client meetings** to show latest trends
- **For reports and presentations** requiring visual data
- **Monthly** for tracking year-over-year performance

### Output Details

**Chart Features**:
- **Title**: "National Design Academy - International Enrolments by Month"
- **Years Shown**: Last 4 academic years (e.g., 2022-23, 2023-24, 2024-25, 2025-26)
- **Colors**: Blue, Orange, Green, Purple (distinct, professional palette)
- **Layering**: Current year on top layer for maximum visibility
- **Branding**: Roksys logo (bottom-right, 40% scale, 70% opacity)
- **Format**: PNG, 2700x1500 pixels, 150 DPI

**Key Insights Visible**:
- Seasonal patterns (e.g., January peaks)
- Year-over-year growth/decline
- Current year performance vs historical
- Monthly trends across academic cycles

### Dependencies

Installed in virtual environment (`.venv/`):
- `openpyxl` - Excel file reading
- `matplotlib` - Chart generation
- `Pillow` - Logo/image handling

### Configuration

To modify the chart:
- **Number of years**: Edit line 108 (`sorted_years[-4:]` → change 4 to desired number)
- **Colors**: Edit lines 90-95 (color hex codes)
- **Logo size**: Edit line 181 (`0.4` = 40% of original)
- **Chart dimensions**: Edit line 98 (`figsize=(18, 10)`)

### Files Created

- `../enrolments/nda-international-by-month-comparison.png` - The chart image

### Integration with Workflow

This script is part of the larger enrolment tracking system:
1. **Email arrives** from pk@nda.ac.uk with new data
2. **enrolment-file-manager.py** extracts and updates ACTIVE files
3. **create-monthly-comparison-chart.py** regenerates chart with latest data
4. **Chart** ready for client reports/presentations

---

## Future Scripts

Additional automation scripts for NDA will be documented here as they are created.
