---
title: Product Feed Issue Analysis: Click Spike Investigation for Tree2Mydoor
source: 2025-10-30_collaber-ppc-chat-space-mention-thank-you-peter-em_1.md
date_added: 2025-11-12
last_updated: 2025-11-12
tags: [merchant-center, product-feed, shopping-campaigns, feed-optimization, tree2mydoor, troubleshooting]
source_type: email
---

## Summary

- 316% click increase identified on October 27-28 for Tree2Mydoor account
- Single product (Olive Tree Gift - £28.99, ID 01090) generated 1,465 clicks on October 28
- Root cause: Product flickering in/out of Google Merchant Center feed multiple times daily
- Product removed and re-added 4 times on October 29 alone
- Google algorithm treats repeatedly re-added products as 'new inventory' with auction priority
- Additional discussion about implementing llms.txt format in Shopify theme

## Key Insights

- Product feed stability critical for maintaining consistent Shopping campaign performance
- Feed flickering can trigger Google's 'new inventory' algorithm, causing unexpected cost spikes
- Stock synchronization issues between inventory systems and Merchant Center create feed instability
- Enhanced monitoring needed to catch feed disapprovals and product status changes in real-time
- AI crawler optimization (llms.txt) becoming relevant for e-commerce SEO strategy

## Full Content

# 'Collaber PPC Chat' space mention – Thank you @Peter Empson

## Email Details

- **From:** "Qamar Gulraiz (via Google Chat)" <chat-noreply@google.com>
- **To:** petere@roksys.co.uk
- **Date:** 2025-10-30 17:36:39
- **Gmail ID:** 19a37b1f34d7cb54

---

## Message

Qamar Gulraiz <qamar@collaber.agency> mentioned you in Collaber PPC Chat  
while you were away


Peter Empson

Peter Empson



I've identified the cause of the click spike on October 27-28. **What  
Happened:** Your campaigns saw a 316% click increase, with one product (The  
Olive Tree Gift - £28.99, Product ID 01090) accounting for 1,465 clicks on  
October 28th alone. **Root Cause:** Product 01090 has been flickering in  
and out of your Google Merchant Center feed multiple times per day since  
October 25th. The product was removed and re-added 4 times on October 29th  
alone. **Why This Matters:** When a product is repeatedly removed and  
re-added, Google's algorithm treats it as "new inventory" each time and  
gives it priority in auctions. This caused the massive click surge.  
**Likely Cause:** This flickering typically indicates stock synchronization  
issues - the product is likely going in/out of stock rapidly in your  
inventory system. **Next Steps:** 1. Check your stock levels for product  
01090 2. Review your Merchant Center feed for any disapproval warnings 3.  
Ensure consistent stock availability for this high-performer The product is  
currently active at £28.99 and clearly performs well when stable. I've now  
enabled enhanced tracking to catch these issues immediately going forward.  
Let me know if you'd like me to investigate further.





Peter Empson

Peter Empson



@Qamar Gulraiz The LLMS.txt format is a very new thing, which has been  
quite difficult to find somewhere to give me a definitive answer for this.  
But I finally managed to get some instructions. Please take a look at the  
following, implement it, and let me know what you think. Overview ---------  
Because Shopify does not allow uploading arbitrary files to the root  
directory (eg https://example.com/llms.txt), the correct approach is to  
reference the files explicitly within your store's theme code using <link>  
tags in the HTML <head>. This allows AI systems and crawlers to discover  
these files correctly. --- Step-by-Step Instructions  
------------------------- 1. Log in to your Shopify Admin. • Go to: Online  
Store → Themes. 2. Edit your live theme's code. • Click “⋯” next to your  
active theme and choose “Edit code”. • In the left-hand sidebar, open the  
folder: layout/ • Click to open the file: theme.liquid 3. Locate the <head>  
section of the document. • Scroll down until you find this part: <head> {{  
content_for_header }} <meta charset="utf-8"> ... 4. Insert the following  
lines just before the closing </head> tag: <!-- LLM and AI crawler  
references --> <link rel="llms"  
href="https://tree2mydoor.com/cdn/shop/files/llms.txt"> <link rel="agents"  
href="https://tree2mydoor.com/cdn/shop/files/agents.txt"> <!-- Optional  
meta fallbacks for wider crawler compatibility --> <meta  
name="llms:description" content="Reference to Tree2Mydoor llms.txt for AI  
discovery"> <meta name="agents:description" content="Reference to  
Tree2Mydoor agents.txt for AI discovery"> Example placement: <head> {{  
content_for_header }} <meta charset="utf-8"> <meta name="viewport"  
content="width=device-width,initial-scale=1"> <link rel="canonical"  
href="{{ canonical_url }}"> <link rel="llms"  
href="https://tree2mydoor.com/cdn/shop/files/llms.txt"> <link rel="agents"  
href="https://tree2mydoor.com/cdn/shop/files/agents.txt"> <meta  
name="llms:description" content="Reference to Tree2Mydoor llms.txt for AI  
discovery"> <meta name="agents:description" content="Reference to  
Tree2Mydoor agents.txt for AI discovery"> </head> 5. Click Save. 6. Test  
the setup: • Visit your live store homepage, right-click and choose “View  
Page Source”. • Search for “llms” and “agents” – you should see the new  
<link> and <meta> tags. • Test the file links directly in your browser:  
https://tree2mydoor.com/cdn/shop/files/llms.txt  
https://tree2mydoor.com/cdn/shop/files/agents.txt --- Result ------ Your  
Shopify store will now correctly signal the locations of your llms.txt and  
agents.txt files to AI crawlers, ensuring accurate brand representation and  
discoverability despite root-directory restrictions.





Qamar Gulraiz (via Tasks)

Qamar Gulraiz (via Tasks)



Created a task for @Qamar Gulraiz


@Qamar Gulraiz The LLMS.txt format is a very new thing, which has been  
quite difficult to find somewhere to give me a definitive answer for

this. But I finally managed to get some instructions. Please take a look at  
the following, implement it, and let me know what you think. Overview  
--------- Because Shopify does not allow uploading arbitrary files to the  
root directory (eg https://example.com/llms.txt), the correct approach is  
to reference the files explicitly within your store's theme code using  
<link> tags in the HTML <head>. This allows AI systems and crawlers to  
discover these files correctly. --- Step-by-Step Instructions  
------------------------- 1. Log in to your Shopify Admin. • Go to: Online  
Store → Themes. 2. Edit your live theme's code. • Click “⋯” next to your  
active theme and choose “Edit code”. • In the left-hand sidebar, open the  
folder: layout/ • Click to open the file: theme.liquid 3. Locate the <head>  
section of the document. • Scroll down until you find this part: <head> {{  
content_for_header }} <meta charset="utf-8"> ... 4. Insert the following  
lines just before the...





Qamar Gulraiz (via Tasks)

Qamar Gulraiz (via Tasks)



Completed a task


@Qamar Gulraiz The LLMS.txt format is a very new thing, which has been  
quite difficult to find somewhere to give me a definitive answer for

this. But I finally managed to get some instructions. Please take a look at  
the following, implement it, and let me know what you think. Overview  
--------- Because Shopify does not allow uploading arbitrary files to the  
root directory (eg https://example.com/llms.txt), the correct approach is  
to reference the files explicitly within your store's theme code using  
<link> tags in the HTML <head>. This allows AI systems and crawlers to  
discover these files correctly. --- Step-by-Step Instructions  
------------------------- 1. Log in to your Shopify Admin. • Go to: Online  
Store → Themes. 2. Edit your live theme's code. • Click “⋯” next to your  
active theme and choose “Edit code”. • In the left-hand sidebar, open the  
folder: layout/ • Click to open the file: theme.liquid 3. Locate the <head>  
section of the document. • Scroll down until you find this part: <head> {{  
content_for_header }} <meta charset="utf-8"> ... 4. Insert the following  
lines just before the...





Peter Empson

Peter Empson



Thanks for doing this. I'll keep an eye on it. There is some ambiguity at  
the moment about these two files and where to actually place them. What  
I've given you is the latest info, but I will keep an eye on things and see  
whether there are any changes to this over time.





Qamar Gulraiz

Qamar Gulraiz



Peter Empson



Thanks for doing this. I'll keep an eye on it. There is some ambiguity at  
the moment about these two files and where to actually place them. What  
I've given you is the latest info, but I will keep an eye on things and see  
whether there are any changes to this over time.





Thank you @Peter Empson




Open in Google Chat


Google Chat: An intelligent messaging app, built for teams.
Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
You have received this email because you have been mentioned in this  
conversation by a Google Chat user. You cannot reply to this email.
Unsubscribe from these emails by changing your email reminder preferences  
for Google Chat. Email reminder preferences cannot be set on mobile  
devices. Learn more
Logo for Google





---

*Processed from inbox on 2025-11-12*
*Original file: 2025-10-30_collaber-ppc-chat-space-mention-thank-you-peter-em_1.md*
