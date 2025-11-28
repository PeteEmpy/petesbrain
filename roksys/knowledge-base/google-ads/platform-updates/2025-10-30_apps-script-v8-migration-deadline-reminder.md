---
title: Apps Script Rhino to V8 Runtime Migration Deadline - January 31, 2026
source: 2025-10-30_reminder-migrate-your-apps-script-projects-to-v8-r_1.md
date_added: 2025-11-12
last_updated: 2025-11-12
tags: [apps-script, v8-runtime, migration, javascript, technical-maintenance]
source_type: email
---

## Summary

- Final reminder for mandatory migration from Rhino to V8 runtime by January 31, 2026
- Scripts not migrated will cease to execute after deadline
- V8 runtime provides modern JavaScript features, enhanced security and stability
- Google provided CSV file identifying all domain scripts requiring migration

## Key Insights

- Legacy Apps Script projects pose operational risk if not migrated before hard deadline
- V8 runtime migration enables access to modern JavaScript ES6+ features for enhanced functionality
- Proactive identification and inventory of affected scripts critical for avoiding service disruption
- Migration may require developer resources and testing time - early planning essential

## Full Content

# [Reminder] Migrate your Apps Script projects to V8 runtime before January 31, 2026

## Email Details

- **From:** The Google Workspace Team <workspace-noreply@google.com>
- **To:** petere@roksys.co.uk
- **Date:** 2025-10-30 10:54:56
- **Gmail ID:** 19a364229d83ccd4

---

## Message

Google Workspace logo



Plan your transition from the Rhino runtime to the V8 runtime.



Dear administrator,

We're writing to remind you about an upcoming change to Apps Script that  
will affect how some of your users' scripts run. The Rhino runtime will be  
turned down on or after January 31, 2026.

This follows the communications we sent on February 18, 2025 and August 27,  
2025.

We have provided additional information below to guide you through this  
change.

What this means for your organization

Since February 2020, all new scripts created in Apps Script execute code in  
V8 runtime by default. We've determined that some of the older Apps Scripts  
in your organization still use the Rhino runtime and must be migrated to V8  
runtime by January 31, 2026.

Migrating to V8 offers significant advantages, including:


Access to modern JavaScript features: Supports the latest JavaScript  
standards, providing your developers access to powerful new language  
features.
Enhanced security and stability: Provides a more robust and secure runtime  
environment.

Apps Script projects that are not migrated to the V8 runtime before January  
31, 2026 will not execute or run after this date.

What you need to do

We encourage you to begin the migration process as soon as possible to  
ensure a smooth transition before we remove support for the Rhino runtime,  
which will happen no earlier than January 31, 2026.

To assist you with this transition, we've identified all the Apps Script  
projects in your domain that are currently using the Rhino runtime. Please  
review these PDF and CSV files, and then work with your script developers  
to migrate these projects to the V8 runtime:


PDF file: This contains the description of each required field in the  
accompanying CSV file. Save a copy of this file.
CSV file: This contains the details about your impacted scripts. This is  
the attachment in this message.

Refer to the Migrating scripts to the V8 runtime page to get started.

We're here to help

We understand that migrating scripts may require some effort, and we're  
committed to supporting you through this process.

If you need additional support after you follow the steps on the Migrating  
scripts to the V8 runtime page, please contact Google Workspace Developer  
Support and specify which steps you took and how they failed. Please be  
aware that Google Workspace Support doesn't provide assistance with general  
coding issues.

Thanks for choosing Google Workspace.

– The Google Workspace Team




Was this information helpful?

A smiling face A neutral face A sad face


© 2025 Google LLC 1600 Amphitheatre Parkway, Mountain View, CA 94043

You have received this important update about your Google Workspace account  
because you designated this email address as a primary or secondary contact  
for mandatory service communications in your Google Admin Console profile.


Twitter Facebook LinkedIn YouTube






---

## Attachments

- [roksys.co.uk_Rhino_Scripts.csv](attachments/2025-10-30/roksys.co.uk_Rhino_Scripts.csv) (530.0 bytes)

---

*Processed from inbox on 2025-11-12*
*Original file: 2025-10-30_reminder-migrate-your-apps-script-projects-to-v8-r_1.md*
