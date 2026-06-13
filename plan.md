# AI-Powered Root-Cause Analysis with Python and LangGraph

## Course Vision

Students will move beyond traditional data analysis and build a cutting-edge agentic AI system for manufacturing intelligence.

The final project will simulate a team of specialized AI agents working together to analyze a large steering wheel manufacturing dataset, detect anomalies, investigate scrap causes, generate insights, and produce business-ready reports.

Instead of building only notebooks or dashboards, students will design an intelligent workflow where each agent has a specific role, similar to a modern AI data team.

## Final Project Goal

Build an agentic workflow using LangGraph where multiple specialized agents collaborate to help a manufacturing company answer questions like:

1. Why is scrap increasing?
2. Which machines, shifts, operators, or material batches are suspicious?
3. Are there abnormal production patterns?
4. What data cleaning issues exist?
5. What SQL queries are needed to investigate the problem?
6. What conclusions should be included in the final report?
7. What recommendations should be sent to factory managers?

## Main Course Modules

### 1. Modern Data Analysis Foundation

Students need a strong applied data foundation before adding agents.

Main points:

1. Pandas for loading, cleaning, filtering, joining, and grouping data
2. Jupyter notebooks for exploration and experimentation
3. Basic statistics for understanding variation, outliers, and trends
4. Seaborn for quick visual exploration
5. Streamlit for simple interactive data apps

### 2. Manufacturing Data Thinking

Students must learn how to think about real factory data.

Main points:

1. Production lines, machines, shifts, operators, batches, and timestamps
2. Scrap rate and defect type analysis
3. Good products vs defective products
4. Process parameters such as temperature, pressure, torque, humidity, and cycle time
5. Time-based patterns and production drift
6. Root-cause investigation mindset
7. Difference between correlation and causation

### 3. SQL for Data Investigation

The agentic system will need agents that can ask questions from data using SQL.

Main points:

1. Basic SQL queries
2. Filtering, sorting, grouping, and aggregation
3. Joins between production, inspection, machine, and material tables
4. Using SQLite or DuckDB locally
5. Translating business questions into SQL queries
6. Validating SQL results with Pandas

### 4. LLM Fundamentals for Developers

Before building agents, students need to understand what LLMs can and cannot do.

Main points:

1. What an LLM is
2. Prompts, messages, system instructions, and context
3. Structured outputs
4. Tool calling
5. Hallucinations and validation
6. Why AI agents need guardrails
7. Human-in-the-loop review

### 5. LangGraph Core Concepts

Students learn LangGraph as the main orchestration framework.

Main points:

1. Graph-based workflows
2. Nodes and edges
3. State management
4. Conditional routing
5. Cycles and iterative workflows
6. Human approval steps
7. Checkpointing and memory
8. Error handling and retries

### 6. Specialized Agent Design

Students design agents as specialized team members, not as one giant chatbot.

Main agent roles:

1. Data Understanding Agent
2. SQL Writer Agent
3. SQL Validator Agent
4. Data Cleaning Agent
5. Exploratory Data Analysis Agent
6. Anomaly Detection Agent
7. Root-Cause Investigation Agent
8. Visualization Agent
9. Report Writer Agent
10. Orchestrator Agent

### 7. Agentic Manufacturing Workflow

Students combine the agents into a complete production-style workflow.

Main points:

1. Receive a business question
2. Interpret the question
3. Select the required data sources
4. Generate SQL queries
5. Validate queries before execution
6. Load results into Pandas
7. Clean and prepare data
8. Run exploratory analysis
9. Detect anomalies
10. Investigate likely causes
11. Generate visualizations
12. Produce a final report
13. Ask for human review when confidence is low

### 8. Responsible and Reliable AI Systems

Because this system may influence business decisions, students must learn reliability.

Main points:

1. Never trust AI output blindly
2. Validate generated SQL
3. Validate statistical conclusions
4. Track assumptions
5. Separate facts from interpretations
6. Explain confidence levels
7. Keep humans involved in important decisions
8. Log every step of the workflow

### 9. Final Interface

Students build a simple interface for the agentic system.

Possible interface options:

1. Streamlit app
2. Chat-style interface
3. Dashboard with filters
4. Report generation page
5. Human approval panel

The interface should allow users to ask manufacturing questions and receive structured analysis from the agent workflow.

## Suggested Tech Stack

### Core Data Stack

1. Python
2. Pandas
3. NumPy
4. Jupyter Notebook
5. Seaborn
6. Matplotlib

### Database Stack

1. SQLite
2. DuckDB
3. SQLAlchemy, optional

### AI and Agentic Stack

1. LangGraph
2. LangChain
3. OpenAI API or another LLM provider
4. Pydantic for structured outputs
5. MCP concepts, optional bonus

### App Stack

1. Streamlit
2. Plotly, optional
3. Python-dotenv for environment variables

### Engineering Stack

1. Git and GitHub
2. Virtual environments
3. Requirements management
4. Logging
5. Basic testing

## Final Project: Agentic Scrap Intelligence System

Students will build a multi-agent AI system that behaves like a digital manufacturing investigation team.

The system should be able to:

1. Accept a business question from a user
2. Decide which agent should act next
3. Query manufacturing data
4. Clean and validate data
5. Analyze scrap patterns
6. Detect anomalies
7. Suggest possible root causes
8. Generate charts
9. Write a final business report
10. Ask for human review when needed

## Final Course Outcome

By the end of the course, students should understand how to combine:

1. Python data analysis
2. SQL-based investigation
3. Manufacturing domain thinking
4. LLM-powered reasoning
5. LangGraph orchestration
6. Specialized AI agents
7. Human-in-the-loop validation
8. Streamlit-based delivery

The goal is not just to use AI, but to build a reliable AI-assisted investigation workflow that can help a real manufacturing company reduce scrap and understand production problems.