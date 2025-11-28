# Facebook Specifications Inbox

This directory is the staging area for manual inputs that will be automatically processed and added to the Facebook Specifications Knowledge Base.

## Structure

```
_inbox/
├── meta-rep-emails/      # Meta representative emails
├── meeting-notes/         # Meeting notes with Meta reps
├── manual-additions/      # Manual specification additions
└── processed/            # Files after processing (auto-created)
```

## How It Works

The **Facebook Specifications Processor** runs automatically every 2 hours and:

1. Scans all files in `meta-rep-emails/`, `meeting-notes/`, and `manual-additions/`
2. Extracts specifications and best practices using Claude AI
3. Categorizes content (facebook-ads or meta-business-suite)
4. Tags with source metadata (rep name, date, context)
5. Updates JSON specification files or creates best practice markdown
6. Moves processed files to `processed/` folder

## Adding Files

### Meta Rep Emails
- Copy email content to a `.md` or `.txt` file
- Include subject, sender, date, and full email body
- Place in `meta-rep-emails/` folder

### Meeting Notes
- Export meeting notes as `.md` or `.txt`
- Include meeting title, date, attendees, and full notes
- Place in `meeting-notes/` folder

### Manual Additions
- Create `.md` files with specifications or best practices
- Include source information (where it came from)
- Place in `manual-additions/` folder

## Processing

Files are processed automatically every 2 hours. You can also run manually:

```bash
python3 agents/facebook-specs-processor/facebook-specs-processor.py
```

## Output

Processed content is saved to:
- **Specifications**: `facebook-specifications/facebook-ads/specifications/` or `meta-business-suite/specifications/`
- **Best Practices**: `facebook-specifications/facebook-ads/best-practices/` or `meta-business-suite/best-practices/`

## Source Tagging

All content is automatically tagged with:
- Source type (meta_rep_recommendation, manual_addition)
- Source name (rep name, meeting title)
- Date
- Context
- Verification status

## Tips

- Use descriptive filenames (e.g., `2025-11-12-meta-rep-campaign-optimization.md`)
- Include as much context as possible
- The processor handles multiple files in batches efficiently
- Check logs: `~/.petesbrain-facebook-specs-processor.log`

