# Quick Start - 5 Commands to Automated Reports

## First Time Setup (15 minutes)

```bash
# 1. Navigate to tool directory
cd /Users/administrator/Documents/PetesBrain/tools/monthly-report-generator

# 2. Run setup (follow prompts)
python3 setup_google_api.py

# 3. Test with October data
python3 generate_devonshire_slides.py --month 2025-10

# 4. Open the generated presentation link and verify formatting

# 5. Done! Use for all future months
```

## Monthly Usage (2 minutes)

```bash
# Generate report (wait 3-5 days after month end)
cd /Users/administrator/Documents/PetesBrain/tools/monthly-report-generator
python3 generate_devonshire_slides.py --month 2025-11
```

That's it! Open the link, review, copy into shared deck, send to client.

## What You Get

✅ **Estate Blue (#00333D) headers** with white text
✅ **Stone (#E5E3DB) backgrounds** for data cells
✅ **Editable tables** (not images)
✅ **Professional formatting** matching your brand
✅ **14 slides** ready to deliver

## Time Saved

- **Before**: 2-3 hours per month
- **After**: 5 minutes per month
- **Annual savings**: ~30 hours

## Need Help?

See `SETUP-GUIDE.md` for detailed instructions.

---

**Pro Tip**: After setup, bookmark this command:
```bash
python3 ~/Documents/PetesBrain/tools/monthly-report-generator/generate_devonshire_slides.py --month 2025-11
```

Run it from anywhere to generate reports instantly.
