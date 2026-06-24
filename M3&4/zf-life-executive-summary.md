# Executive Summary: AI-Powered Manufacturing Intelligence
## A Research Proposal for ZF Life

**Prepared by:** Savnet AI Training Programme  
**Date:** June 2026  
**Classification:** Confidential, For Internal Review Only

## 1. Introduction

Dear ZF Life team,

We are reaching out on behalf of the **Savnet AI Training Programme**, a professional development initiative that trains engineers and developers in modern Python, data analysis, and applied artificial intelligence.

As part of our most advanced module, students are building a real-world, production-inspired project that combines data engineering, SQL analysis, and multi-agent AI workflows. We believe this project aligns strongly with the challenges faced on your production floor, and we would be honored to propose a collaboration that is **mutually beneficial**: one that offers ZF Life an early look at AI-assisted manufacturing analysis, while giving our students the opportunity to work with authentic industrial data.

This document outlines the problem we believe you face, the solution we are proposing to research and prototype, the data and resources we would require from your side, and the scope and boundaries of this collaboration.

We hope this sparks a productive conversation.

## 2. The Problem

Modern manufacturing facilities like ZF Life generate an enormous volume of data every day, across machines, stations, operators, shifts, and material batches. For a product as precision-critical as the **steering wheel**, quality control is not optional. Even small deviations in any step of the production process can lead to scrap, rework, customer returns, or in the worst case, safety incidents downstream.

The challenge most manufacturers face is not a lack of data. It is a lack of **actionable intelligence** derived from that data.

Specifically, the problems we aim to address are:

- **Scrap rates are difficult to diagnose.** When scrap increases, identifying the root cause (whether it is a machine, an operator, a material batch, a shift pattern, or an upstream station) requires manual investigation that is time-consuming and often incomplete.
- **Knowledge is siloed.** Operators know their station. Quality teams know their metrics. But connecting the dots across the full production journey of a single part, from the magnesium skeleton moulding stage where the part receives its unique ID through to the final shipped product, is rarely done in a systematic way.
- **Manual inputs are underutilised.** Operators record observations directly into the system, but these textual entries are rarely analysed at scale. They contain valuable early signals that often go unread until a problem has already grown.
- **Guides and procedures exist, but are static.** Procedural documents define what a defect is and how an operator should act, but they are not connected to live production data in a way that enables automatic reasoning.
- **Reactive rather than proactive quality control.** Most analysis happens after a problem has accumulated, rather than detecting drift or early warning signals in real time.

## 3. The Proposed Solution

We propose to research and prototype an **AI-Powered Root-Cause Analysis System**: an agentic workflow built in Python using **LangGraph**, designed to behave like a digital investigation team embedded in your production data.

Rather than building a static dashboard or a single model, the system is composed of **multiple specialised AI agents**, each with a distinct responsibility:

| Agent | Role |
|---|---|
| **Data Understanding Agent** | Profiles incoming data, detects anomalies and schema issues |
| **SQL Writer Agent** | Translates business questions into structured queries |
| **SQL Validator Agent** | Reviews and validates queries before execution |
| **Data Cleaning Agent** | Standardises, deduplicates, and prepares data |
| **Exploratory Analysis Agent** | Identifies patterns, trends, and outliers |
| **Anomaly Detection Agent** | Flags statistically unusual events across stations and shifts |
| **Root-Cause Investigation Agent** | Correlates findings across agents to suggest likely causes |
| **Visualisation Agent** | Produces charts and graphical summaries |
| **Report Writer Agent** | Drafts structured, human-readable business reports |
| **Orchestrator Agent** | Coordinates the full workflow and decides what happens next |

A human review step is integrated at critical decision points, ensuring that AI-generated conclusions are always reviewed before being acted upon.

The system will be interactive. A user (e.g. a quality engineer or plant manager) types a business question in plain language and receives a structured investigation report, supported by data, charts, and documented reasoning.

## 4. Example Business Questions the System Could Answer

The following are representative questions the system is designed to investigate. These are not exhaustive, as the system is built to handle natural language queries:

1. *"Why has the scrap rate at Station 4 increased over the last 3 weeks?"*
2. *"Which operators are statistically associated with the highest defect rates on the spline pressing station?"*
3. *"Are there patterns in defect types that correlate with specific material batch numbers?"*
4. *"Has there been any measurable production drift on the torque assembly station since the last maintenance cycle?"*
5. *"Which shift (morning, afternoon, or night) consistently produces the most rework events?"*
6. *"Are there any early warning signals in operator manual input logs that precede a defect spike?"*
7. *"What is the average cycle time per station, and which stations show the most variance?"*
8. *"Are there correlated anomalies between power consumption data and defect rates at any station?"*
9. *"What percentage of scrapped parts had a clean record up to Station 6 before failing at Station 7?"*
10. *"Which combination of factors (machine, shift, material batch, and operator) is most predictive of a defective final product?"*

## 5. Data We Would Need From ZF Life

To build and validate the prototype, we would request access to the following data, under full NDA protection:

### 5.1 Production Telemetry and Operator Input Data

Historical, time-series data covering the full lifecycle of each steering wheel, beginning at the magnesium skeleton moulding stage where the part receives its unique ID, continuing through each subsequent station, and ending at the final quality check and shipment approval. This includes:

- Station-by-station process parameters (e.g. torque values, pressing force, temperatures, cycle times)
- Operator manual input records (free text fields, defect flags, observation codes)
- Part tracking identifiers (to trace a single unit across all stations)
- Timestamps for every event and transition
- Final quality decision per unit (pass / fail / rework / scrap)
- Defect type classifications per station

### 5.2 Procedural and Quality Documentation

- Standard Operating Procedures (SOPs) for each station
- Defect type definitions and visual reference guides per station
- Operator instruction manuals or training materials
- Any image or video guides that illustrate what constitutes a defect

> These documents are critical. They allow our AI agents to reason about process intent, not just raw numbers. The richer this documentation, the higher the quality of root-cause analysis the system can produce.

### 5.3 Auxiliary Data Sources (Optional but High Value)

- Power quality or energy consumption data per station (time-series)
- Machine maintenance logs and downtime records
- Environmental data (temperature, humidity) if recorded
- Material supplier or batch traceability data

## 6. What We Would Need From ZF Life

Beyond data access, successful execution of this prototype requires the following:

### 6.1 A Sandboxed AI API Account

We will need API access to a Large Language Model provider to power the AI agents. We request one of the following options, with a usage cap agreed in advance:

- **Azure OpenAI Service** (preferred for enterprise environments, as data stays within Azure)
- **OpenAI API** with a pre-agreed spending limit
- **Anthropic Claude API**
- **Google Gemini API** (via Google Cloud)
- Alternatively, we are open to any LLM provider ZF Life already has a relationship with

A modest budget cap (e.g. €50–€200 for the research phase) is sufficient. We will build cost-conscious workflows.

### 6.2 A Point of Contact at ZF Life

We would benefit from occasional access to a domain expert, such as a quality engineer or production supervisor, who can validate our assumptions and help us understand the manufacturing process more deeply.

### 6.3 Non-Disclosure Agreements (NDAs)

To protect ZF Life's intellectual property and sensitive operational data, we require:

- An NDA signed by **each student participant** in the programme
- An NDA signed by the **programme coach**
- An NDA signed by the **Savnet representative**

We are happy to work with your legal team on the appropriate NDA format or to provide a draft for review.

## 7. What ZF Life Would Receive

At the conclusion of the research phase, ZF Life will receive:

- A fully documented prototype of the agentic root-cause analysis system
- Source code in a private Git repository
- A final project report covering methodology, findings, and limitations
- A demonstration session with the student team
- Honest feedback on what the system can and cannot yet do in a production context

## 8. Research Disclaimer

> **Important Notice: Please Read Carefully**

This project is conducted as a **structured research and educational initiative**. While we are committed to building a rigorous, well-engineered prototype, the following must be clearly understood before any collaboration begins:

- This system is **built by students** under the supervision of a professional coach. It is **not a production-ready commercial product**.
- The AI agents use **Large Language Models (LLMs)**, which are probabilistic by nature. They can and do make mistakes, misinterpret data, or generate plausible-sounding but incorrect conclusions. **All outputs must be reviewed by a human expert before any business decision is made.**
- We **do not guarantee** accuracy, completeness, or fitness for purpose of any analysis, recommendation, or report generated by the system.
- This prototype should be treated as a **proof of concept and a learning artefact**, not as a replacement for certified quality management systems, certified statistical tools, or qualified engineering judgement.
- Any data shared with us will be used **strictly for educational and research purposes** and will not be shared with any third party.
- The system will not be deployed to any production environment without ZF Life's explicit written consent and a separate commercial agreement.

We believe that being transparent about these boundaries is the foundation of a trustworthy collaboration. We are excited about what we can explore together, and we want to set honest expectations from the start.

## 9. Proposed Next Steps

If this proposal is of interest, we suggest the following as immediate next steps:

1. **Introductory call:** a 30-minute conversation between ZF Life stakeholders, the Savnet representative, and the programme coach to align on scope and feasibility.
2. **NDA review and signing:** legal review and execution of NDAs for all participants.
3. **Data access agreement:** agree on the scope, format, and anonymisation level of the data to be shared.
4. **API account setup:** provision a sandboxed LLM API account with agreed usage limits.
5. **Kick-off:** the student team begins the research and build phase.

We are flexible on timing and happy to adapt the scope to what is practical and comfortable for your team.

## 10. Contact

For questions, feedback, or to schedule an introductory call, please reach out through the Savnet programme representative.

We look forward to hearing from you.

**Warm regards,**  
The Savnet AI Training Programme Team

*This document is confidential and intended solely for the named recipient. Unauthorised distribution is not permitted.*
