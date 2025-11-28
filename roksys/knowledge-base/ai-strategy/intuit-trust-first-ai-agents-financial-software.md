---
title: Intuit's Trust-First Approach to Building AI Agents for Financial Software
source: 2025-10-29_ai_intuit-learned-to-build-ai-agents-for-finance-the.md
date_added: 2025-10-30
last_updated: 2025-10-30
tags: [ai-agents, enterprise-ai, trust-architecture, financial-software, explainable-ai, data-orchestration, user-experience]
source_type: article
---

## Summary

- Intuit built AI agents for QuickBooks that prioritize data querying over generative responses, reducing hallucination risks in financial contexts where accuracy is critical
- Despite improving transaction categorization accuracy by 20 percentage points, the company learned that 'trust is lost in buckets and earned back in spoonfuls' in finance applications
- The system integrates multiple data sources (native Intuit data, OAuth-connected third-party systems, and user-uploaded files) into a unified query layer accessible through natural language
- Explainability is designed as a core UX feature, showing users the reasoning behind AI decisions rather than just displaying results
- Intuit addresses the interface transition challenge by embedding AI agents within existing workflows rather than forcing users to adopt entirely new interaction patterns

## Key Insights

- Architecture choice is fundamental to trust: Using AI as a data query orchestration layer rather than a generative content system dramatically reduces hallucination risks in high-stakes domains like finance
- Explainability must be a designed feature, not an afterthought: Showing the 'why' behind AI decisions through actual UI elements is critical for building and maintaining user trust
- User control preserves trust during accuracy improvements: Even significant accuracy gains can generate complaints if users don't have visibility and control over AI decisions
- Shadow AI usage reveals unmet needs: 25% of accountants were already copying QuickBooks data into ChatGPT, indicating demand for AI-powered analysis within secure, integrated systems
- Incremental adoption strategies work better than replacement: Embedding AI agents into existing workflows allows users to experience benefits without abandoning familiar processes, managing the transition from forms to conversations

## Full Content

---
source: VentureBeat - AI
url: https://venturebeat.com/ai/intuit-learned-to-build-ai-agents-for-finance-the-hard-way-trust-lost-in
published: Tue, 28 Oct 2025 12:30:00 GMT
relevance_score: 6
primary_topic: Enterprise AI agent implementation and trust-building strategies in business automation
fetched: 2025-10-29T21:45:47.691763
category: AI News
---

# Intuit learned to build AI agents for finance the hard way: Trust lost in buckets, earned back in spoonfuls

**Source**: VentureBeat - AI
**URL**: https://venturebeat.com/ai/intuit-learned-to-build-ai-agents-for-finance-the-hard-way-trust-lost-in
**Published**: Tue, 28 Oct 2025 12:30:00 GMT
**Relevance Score**: 6/10

## Summary

<p>Building AI for financial software requires a different playbook than consumer AI, and <a href="https://www.intuit.com/"><u>Intuit&#x27;s</u></a> latest QuickBooks release provides an example.</p><p>The company has announced Intuit Intelligence, a system that orchestrates specialized AI agents across its QuickBooks platform to handle tasks including sales tax compliance and payroll processing. These new agents augment existing accounting and project management agents (which have also been updated) as well as a unified interface that lets users query data across QuickBooks, third-party systems and uploaded files using natural language. </p><p>The new development follow years of investment and improvement in Intuit&#x27;s<a href="https://venturebeat.com/ai/inside-intuits-genos-update-why-prompt-optimization-and-intelligent-data-cognition-are-critical-to-enterprise-agentic-ai-success"> <u>GenOS</u></a>, allowing the company to build AI capabilities that reduce<a href="https://venturebeat.com/ai/how-intuit-built-custom-financial-llms-that-cut-latency-50-while-boosting"> <u>latency and improve accuracy</u></a>.</p><p>But the real news isn&#x27;t what Intuit built — it&#x27;s how they built it and why their design decisions will make AI more usable. The company&#x27;s latest AI rollout represents an evolution built on hard-won lessons about what works and what doesn&#x27;t when deploying AI in financial contexts.</p><p>What the company learned is sobering: Even when its accounting agent improved transaction categorization accuracy by 20 percentage points on average, they still received complaints about errors.</p><p>&quot;The use cases that we&#x27;re trying to solve for customers include tax and finance; if you make a mistake in this world, you lose trust with customers in buckets and we only get it back in spoonfuls,&quot; Joe Preston, Intuit&#x27;s VP of product and design, told VentureBeat.</p><h2>The architecture of trust: Real data queries over generative responses</h2><p>Intuit&#x27;s technical strategy centers on a fundamental design decision. For financial queries and business intelligence, the system queries actual data, rather than generating responses through large language models (LLMs).</p><p>Also critically important: That data isn&#x27;t all in one place. Intuit&#x27;s technical implementation allows QuickBooks to ingest data from multiple distinct sources: native Intuit data, OAuth-connected third-party systems like Square for payments and user-uploaded files such as spreadsheets containing vendor pricing lists or marketing campaign data. This creates a unified data layer that AI agents can query reliably.</p><p>&quot;We&#x27;re actually querying your real data,&quot; Preston explained. &quot;That&#x27;s very different than if you were to just copy, paste out a spreadsheet or a PDF and paste into ChatGPT.&quot;</p><p>This architectural choice means that the Intuit Intelligence system functions more as an orchestration layer. It&#x27;s a natural language interface to structured data operations. When a user asks about projected profitability or wants to run payroll, the system translates the natural language query into database operations against verified financial data.</p><p>This matters because Intuit&#x27;s internal research has uncovered widespread shadow AI usage. When surveyed, 25% of accountants using QuickBooks admitted they were already copying and pasting data into ChatGPT or Google Gemini for analysis.</p><p>Intuit&#x27;s approach treats AI as a query translation and orchestration mechanism, not a content generator. This reduces the hallucination risk that has plagued AI deployments in financial contexts.</p><h2>Explainability as a design requirement, not an afterthought</h2><p>Beyond the technical architecture, Intuit has made explainability a core user experience across its AI agents. This goes beyond simply providing correct answers: It means showing users the reasoning behind automated decisions.</p><p>When Intuit&#x27;s accounting agent categorizes a transaction, it doesn&#x27;t just display the result; it shows the reasoning. This isn&#x27;t marketing copy about explainable AI, it&#x27;s actual UI displaying data points and logic.</p><p>&quot;It&#x27;s about closing that trust loop and making sure customers understand the why,&quot; Alastair Simpson, Intuit&#x27;s VP of design, told VentureBeat.</p><p>This becomes particularly critical when you consider Intuit&#x27;s user research: While half of small businesses describe AI as helpful, nearly a quarter haven&#x27;t used AI at all. The explanation layer serves both populations: Building confidence for newcomers, while giving experienced users the context to verify accuracy.</p><p>The design also enforces human control at critical decision points. This approach extends beyond the interface. Intuit connects users directly with human experts, embedded in the same workflows, when automation reaches its limits or when users want validation.</p><h2>Navigating the transition from forms to conversations</h2><p>One of Intuit&#x27;s more interesting challenges involves managing a fundamental shift in user interfaces. Preston described it as having one foot in the past and one foot in the future.</p><p>&quot;This isn&#x27;t just Intuit, this is the market as a whole,&quot; said Preston. &quot;Today we still have a lot of customers filling out forms and going through tables full of data. We&#x27;re investing a lot into leaning in and questioning the ways that we do it across our products today, where you&#x27;re basically just filling out, form after form, or table after table, because we see where the world is headed, which is really a different form of interacting with these products.&quot;</p><p>This creates a product design challenge: How do you serve users who are comfortable with traditional interfaces while gradually introducing conversational and agentic capabilities?</p><p>Intuit&#x27;s approach has been to embed AI agents directly into existing workflows. This means not forcing users to adopt entirely new interaction patterns. The payments agent appears alongside invoicing workflows; the accounting agent enhances the existing reconciliation process rather than replacing it. This incremental approach lets users experience AI benefits without abandoning familiar processes.</p><h2>What enterprise AI builders can learn from Intuit&#x27;s approach</h2><p>Intuit&#x27;s experience deploying AI in financial contexts surfaces several principles that apply broadly to enterprise AI initiatives. </p><p><b>Architecture matters for trust: </b>In domains where accuracy is critical, consider whether you need content generation or data query translation. Intuit&#x27;s decision to treat AI as an orchestration and natural language interface layer dramatically reduces hallucination risk and avoids using AI as a generative system.</p><p><b>Explainability must be designed in, not bolted on: </b>Showing users why the AI made a decision isn&#x27;t optional when trust is at stake. This requires deliberate UX design. It may constrain model choices.</p><p><b>User control preserves trust during accuracy improvements: </b>Intuit&#x27;s accounting agent improved categorization accuracy by 20 percentage points. Yet, maintaining user override capabilities was essential for adoption.</p><p><b>Transition gradually from familiar interfaces: </b>Don&#x27;t force users to abandon forms for conversations. Embed AI capabilities into existing workflows first. Let users experience benefits before asking them to change behavior.</p><p><b>Be honest about what&#x27;s reactive versus proactive: </b>Current AI agents primarily respond to prompts and automate defined tasks. True proactive intelligence that makes unprompted strategic recommendations remains an evolving capability. </p><p><b>Address workforce concerns with tooling, not just messaging: </b>If AI is meant to augment rather than replace workers, provide workers with AI tools. Show them how to leverage the technology.</p><p>For enterprises navigating AI adoption, Intuit&#x27;s journey offers a clear directive. The winning approach prioritizes trustworthiness over capability demonstrations. In domains where mistakes have real consequences, that means investing in accuracy, transparency and human oversight before pursuing conversational sophistication or autonomous action.</p><p>Simpson frames the challenge succinctly: &quot;We didn&#x27;t want it to be a bolted-on layer. We wanted customers to be in their natural workflow, and have agents doing work for customers, embedded in the workflow.&quot;</p>

## Scoring Analysis

**Primary Topic**: Enterprise AI agent implementation and trust-building strategies in business automation
**Reason**: While this article focuses on financial software rather than marketing tools, it provides highly valuable strategic guidance on AI agent deployment, user trust, and interface design that applies directly to marketing automation platforms. The lessons about explainability, gradual transition from traditional interfaces, and addressing accuracy concerns are relevant for marketers implementing AI tools, though the specific use cases are outside core marketing/advertising domains.

---

*Article fetched by AI news monitor*
*Full content will be processed by knowledge base system*

**Original URL**: https://venturebeat.com/ai/intuit-learned-to-build-ai-agents-for-finance-the-hard-way-trust-lost-in


---

*Processed from inbox on 2025-10-30*
*Original file: 2025-10-29_ai_intuit-learned-to-build-ai-agents-for-finance-the.md*
