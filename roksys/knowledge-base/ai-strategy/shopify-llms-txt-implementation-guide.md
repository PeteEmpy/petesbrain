---
title: Implementing LLMS.txt and Agents.txt on Shopify for AI Discovery
source: 2025-10-31_collaber-ppc-chat-space-mention-hi-peter-empson-th.md
date_added: 2025-11-12
last_updated: 2025-11-12
tags: [llms-txt, shopify, ai-crawlers, brand-discovery, seo]
source_type: email
---

## Summary

- Instructions for implementing LLMS.txt format on Shopify store (Tree2Mydoor) to enable AI crawler discovery
- Workaround for Shopify's root directory restrictions using <link> tags in theme.liquid file
- Implementation includes both llms.txt and agents.txt files for comprehensive AI discoverability
- Task assigned to implement meta tags and link references in store theme for proper AI brand representation

## Key Insights

- LLMS.txt is emerging as new standard for AI system brand discovery, similar to robots.txt for search engines
- Platform limitations (like Shopify) require creative implementation approaches for new AI standards
- Proactive brand representation in AI systems becoming important for e-commerce visibility
- Early adoption of AI discovery standards may provide competitive advantage as AI systems become primary discovery channels

## Full Content

# 'Collaber PPC Chat' space mention – Hi @Peter Empson Thank...

## Email Details

- **From:** "Gareth Mitchell (via Google Chat)" <chat-noreply@google.com>
- **To:** petere@roksys.co.uk
- **Date:** 2025-10-31 17:37:27
- **Gmail ID:** 19a3cd90a7ddd6a8

---

## Message

Gareth Mitchell <gareth@collaber.co.uk> mentioned you in Collaber PPC Chat  
while you were away


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





Gareth Mitchell

Gareth Mitchell



Peter Empson



Big spike on this product  
https://tree2mydoor.com/products/olive-tree-gift?variant=32171711103034 And  
some weird behaviour elsewhere may indicate some competition dropping away.  
But all in all, CPCs have dropped 76% over the last few days, so I'm  
wondering whether this product has had a price change. Can you give me any  
more information?





Hi @Peter Empson Thanks fior the feedback. Sorry I had an impromptu  
afternoon at Manchester Eye Hospital with my son!! Yes I can confirm that  
Tree2mydoor has received very high profile press coverage for the Olive  
trees in large readership magazines and this will be driving direct traffic.




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
*Original file: 2025-10-31_collaber-ppc-chat-space-mention-hi-peter-empson-th.md*
