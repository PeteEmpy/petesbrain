---
title: SAP RPT-1: Enterprise Tabular AI Model for Business Predictions Without Fine-Tuning
source: 2025-11-04_ai_forget-fine-tuning-saps-rpt-1-brings-ready-to-us.md
date_added: 2025-11-05
last_updated: 2025-11-05
tags: [enterprise-ai, predictive-analytics, tabular-models, vertical-ai, business-automation]
source_type: article
---

## Summary

- SAP introduces RPT-1, a pre-trained 'tabular' AI model that works with relational databases and spreadsheets without requiring fine-tuning, trained on decades of SAP business transaction data
- Unlike LLMs trained on text, RPT-1 is specifically designed for structured business data, offering precise predictions for enterprise tasks like customer behavior forecasting and financial analytics
- The model represents a shift toward industry-specific AI solutions that compete with general-purpose LLMs being adapted to spreadsheets (Microsoft Copilot in Excel, Anthropic's Claude for Finance)
- RPT-1 will be available in Q4 2025 via SAP's AI Foundation, with plans for open-source versions and a no-code playground environment
- The model uses ConTextTab architecture for semantic awareness, learning from table headers and column types to understand business context with minimal additional information

## Key Insights

- Vertical AI models trained on industry-specific data may outperform fine-tuned general LLMs for specialized business tasks requiring numerical precision and relational understanding
- For marketing operations, tabular models like RPT-1 could enable more accurate customer lifetime value predictions, purchase timing forecasts, and behavioral analytics without extensive data science resources
- The trend toward pre-trained, domain-specific models suggests marketers should evaluate purpose-built AI tools alongside general LLMs when selecting solutions for data-heavy analytics tasks
- SAP's approach of embedding business knowledge from decades of enterprise data offers a competitive advantage over models that require extensive company-specific training

## Full Content

---
source: VentureBeat - AI
url: https://venturebeat.com/ai/forget-fine-tuning-saps-rpt-1-brings-ready-to-use-ai-for-business-tasks
published: Tue, 04 Nov 2025 05:00:00 GMT
relevance_score: 6
primary_topic: SAP's tabular AI model for enterprise business automation and predictive analytics
fetched: 2025-11-04T21:01:51.999156
category: AI News
---

# Forget Fine-Tuning: SAP’s RPT-1 Brings Ready-to-Use AI for Business Tasks

**Source**: VentureBeat - AI
**URL**: https://venturebeat.com/ai/forget-fine-tuning-saps-rpt-1-brings-ready-to-use-ai-for-business-tasks
**Published**: Tue, 04 Nov 2025 05:00:00 GMT
**Relevance Score**: 6/10

## Summary

<p>SAP aims to displace more general large language models with the release of its own foundational “tabular” model, which the company claims will reduce training requirements for enterprises. </p><p>The model, called SAP RPT-1, is a pre-trained model with business and enterprise knowledge out of the box. SAP calls it a Relational Foundation Model, meaning it can do predictions based on relational databases even without fine-tuning or additional training.</p><p>Walter Sun, SAP&#x27;s global head of AI, told VentureBeat in an interview that the value of the new model lies in its ability to perform various enterprise tasks, such as predictive analytics, out of the box. </p><p>“Everyone knows about language models, and there’s a bunch of good ones that already exist,” Sun said. “But we trained the model on data on business transactions, basically Excel spreadsheets, and so we have a model that can do predictive analytics where the value is that it’s out of the box, meaning you don’t need to have specifics of a company to do tasks analogous to a language model.” </p><p>Sun said that right out of the gate, RPT-1 can essentially build out a business model for enterprises based on its knowledge gained from data from SAP’s decades of information. Organizations can plug the model directly into applications, even without additional fine-tuning.</p><p>RPT-1, SAP’s first large family of AI models, will be generally available in “Q4 of 2025” and be deployed via SAP’s AI Foundation. While RPT-1 is currently available, the company stated that additional models will be made available soon, including an open-source, state-of-the-art model. </p><p>SAP will also release a no-code playground environment to experiment with the model. 
</p><h2>Tabular models vs LLMs
</h2><p>Tabular or relational AI models learned from spreadsheets, unlike LLMs, which learned from text and code. RPT-1 not only understands numbers and the relationships between different cells, but it’s also able to provide more structured and precise answers. </p><p>When enterprises decide to use RPT-1, they can add more direction to the model through a bit of context engineering, since the model is semantically aware and learns based on how it is being used. </p><p>SAP researchers first proposed the idea that tabular models can both exhibit semantic awareness and learn from content through a paper <a href="https://arxiv.org/pdf/2506.10707"><u>published in June</u></a>. It proposed ConTextTab introduced context-aware pretraining. It utilizes semantic signals, such as table headers or column types, to guide model training, enabling the model to build a relational structure with the data. It’s this architecture that makes the model work best for tasks with precise answers, such as for financial or enterprise use cases.</p><p>The RPT models build on the ConTextTab work that lets it learn structured business data, say from SAP’s knowledge graph, and then be able to add more context through usage. </p><p>SAP researchers did test ConTextTab against benchmarks, saying it “is competitive” against similar models like TabPFN and TabIFL. </p><h2>Industry-specific models continue to grow</h2><p>
Many enterprises prefer to fine-tune general LLMs like GPT-5 or Claude, to basically retrain the model to answer only questions relevant to their business. However, a shift towards <a href="https://venturebeat.com/ai/microsoft-brings-ai-to-the-farm-and-factory-floor-partnering-with-industry-giants"><u>industry-specific models has begun to take root</u></a>. </p><p>Sun said that his experience at a previous company, building a very narrow, highly customized AI model for sentiment analysis, influenced a lot of what makes RPT-1 different. </p><p>“It was a very customized model, a narrow model that takes specific feedback for specific products but it wasn’t scalable,” Sun said. “When LLMs came about, that one model measures sentiment. But there are use cases that we can do that LLMs cannot do.”</p><p>He said these use cases include predictions, such as determining when a shopper will return to a grocery store, which may involve numerical analysis along with an understanding of the shopper’s buying habits. However, some LLMs have begun integrating into spreadsheets, and AI model providers encourage users to upload similar data to teach them context. <a href="https://www.microsoft.com/"><u>Microsoft</u></a> added new <a href="https://venturebeat.com/ai/microsofts-copilot-can-now-build-apps-and-automate-your-job-heres-how-it"><u>capabilities to Copilot</u></a>, including the ability to work in Excel. <a href="https://www.anthropic.com/"><u>Anthropic</u></a> <a href="https://venturebeat.com/ai/anthropic-rolls-out-claude-ai-for-finance-integrates-with-excel-to-rival"><u>integrated its Claude</u></a> model with Excel, complementing its <a href="https://venturebeat.com/ai/financial-firms-get-a-purpose-built-claude-as-anthropic-bets-on-vertical-ai-platforms"><u>Claude for Finance service</u></a>. Chinese startup <a href="https://manus.im/"><u>Manus</u></a> also offers a <a href="https://venturebeat.com/data-infrastructure/chinese-startup-manus-challenges-chatgpt-in-data-visualization-which-should-enterprises-use"><u>data visualization tool</u></a> that understands spreadsheets, and ChatGPT can create charts from uploaded spreadsheets and other data sources. </p><p>However, SAP noted that it is more than just reading a spreadsheet; RPT-1 should stand out amongst its competitors because it requires fewer additional pieces of information about a business to provide its responses. </p><p>
</p>

## Scoring Analysis

**Primary Topic**: SAP's tabular AI model for enterprise business automation and predictive analytics
**Reason**: While this article focuses on business automation and predictive analytics rather than marketing-specific applications, it has moderate relevance for understanding AI tools that could support marketing operations. The predictive capabilities (like determining when shoppers return) and business automation features have indirect applications to customer behavior analysis and marketing strategy, though the article doesn't deeply explore marketing use cases.

---

*Article fetched by AI news monitor*
*Full content will be processed by knowledge base system*

**Original URL**: https://venturebeat.com/ai/forget-fine-tuning-saps-rpt-1-brings-ready-to-use-ai-for-business-tasks


---

*Processed from inbox on 2025-11-05*
*Original file: 2025-11-04_ai_forget-fine-tuning-saps-rpt-1-brings-ready-to-us.md*
