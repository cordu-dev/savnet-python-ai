# M3 Curriculum: Agentic Scrap Intelligence System
## 15 Sessions x 3 Hours — Coach Planning Document

**Goal:** By Session 15, students ship a working multi-agent AI system that can investigate manufacturing data, detect anomalies, find root causes, and produce a business report — built with Python, LangGraph, and real industrial thinking.

**Culture:** This is a startup, not a university. Students use AI aggressively to write code, debug, learn, and move fast. The coach's job is to point at the right problems, not to hand out solutions. Mistakes ship early and get fixed. Every session produces something runnable.

**Status of Session 1:** Done. Pandas foundations, manufacturing CSV, Streamlit mini-app.

---

## Phase 1: Data Foundation
### Sessions 1-4 — Learn to work with real manufacturing data before touching any AI

---

### Session 1: Pandas First Contact ✅ Done

**Why:** Students need to see real data before anything else. A DataFrame full of machine IDs, scrap counts, and shift timestamps is more motivating than any textbook example. This session anchors the whole course in the factory floor.

**Covered:**
- DataFrames, Series, loading CSV
- Inspecting, filtering, sorting, grouping
- Calculating scrap rate
- Mini Streamlit app with machine filter

**Homework options:**
- Build a shift-level scrap summary dashboard in Streamlit with a working filter
- Extend the dataset with 3 new calculated columns and write 5 business observations in a Jupyter notebook
- Find a public manufacturing CSV dataset, load it, and answer 5 self-generated questions

---

### Session 2: Pandas Deeper + Real Data is Messy

**Why:** The ZF Life dataset will not be clean. If students only know how to work with tidy CSVs they will be stuck on day one of the real project. This session also introduces multi-table data, which is the actual shape of manufacturing systems.

**Topics and activities:**
- Handling missing values: `fillna`, `dropna`, `isna` patterns
- Fixing data types: strings to dates, numeric coercion
- Removing duplicates and dealing with inconsistent categories
- Merging tables: production log + inspection table + material batch table
- Datetime columns: extracting week, shift blocks, rolling windows
- Chaining operations cleanly

**Homework options:**
- Given a deliberately broken dataset, clean it and document every decision you made and why
- Join three manufacturing tables and answer 5 cross-table business questions (e.g. "do defect rates differ by material supplier?")
- Build a data quality report: a Jupyter notebook that automatically flags problems in any manufacturing CSV you give it

---

### Session 3: SQL for Data Investigators

**Why:** The AI agents will generate and execute SQL queries. If students cannot read SQL, they cannot validate what the agents produce, and they will not be able to debug failures. SQL also forces precision: you cannot write a vague query.

**Topics and activities:**
- DuckDB: query Pandas DataFrames directly with SQL, no setup needed
- `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, `HAVING`, `JOIN`
- Translating business questions into SQL: practice with manufacturing scenarios
- Running SQL results back into Pandas for further analysis
- Common SQL mistakes and how to catch them
- Build a small "question bank": 20 business questions mapped to their SQL queries

**Homework options:**
- Write SQL queries for 15 manufacturing business questions across at least 3 joined tables
- Build a Jupyter notebook where every cell is a business question + its SQL + an interpretation of the result
- Take the Streamlit dashboard from Session 1-2 and power it with DuckDB queries instead of Pandas filters

---

### Session 4: Visualization + Streamlit Dashboard

**Why:** Students need to be fluent in Streamlit before they build the final UI for the agent system. And visual exploration is often how anomalies are spotted before any AI is involved. Learning to read charts is as important as generating them.

**Topics and activities:**
- Seaborn: bar charts, line charts, box plots, heatmaps for correlation
- Plotly for interactive charts (hover, zoom, filter)
- Choosing the right chart for the right question
- Streamlit: `st.metric`, `st.chart`, `st.tabs`, `st.expander`, layout columns
- Building a full manufacturing KPI dashboard: scrap trend, machine comparison, defect type breakdown, shift heatmap
- Structuring a Streamlit app properly: data loading, processing, display layers

**Homework options:**
- Build a KPI dashboard with at least 4 chart types and 2 interactive filters, covering machines, shifts, and defect types
- Create a "red flag" view: a Streamlit page that automatically highlights anomalous records using color-coded tables and alert metrics
- Reproduce 3 charts from a real manufacturing report you find online, using your dataset

---

## Phase 2: LLM and Agent Thinking
### Sessions 5-7 — Understand what LLMs are, how they fail, and how to orchestrate them

---

### Session 5: LLM Fundamentals for Builders

**Why:** Students who skip this session will misuse LLMs throughout the project. They need to understand that LLMs are probabilistic text predictors, not reasoning engines. The mental model of "very confident autocomplete" prevents most hallucination surprises. They also need to see token costs early so they build cost-conscious habits.

**Topics and activities:**
- What an LLM actually does: next token prediction, not reasoning
- Prompts, system instructions, message history, and context windows
- Structured output: getting JSON back reliably using `response_format`
- Tool calling: giving the LLM access to functions
- Hallucinations: causes, detection patterns, mitigation strategies
- Temperature, top-p, and when to tune them
- Token costs: how to estimate, how to avoid waste
- Live demo: same prompt, different results — why determinism matters in production

**Homework options:**
- Write a Python script that calls an LLM API with 10 different manufacturing questions and parses the structured JSON responses — test what breaks
- Prompt-engineer an LLM to extract structured defect records from unstructured operator notes — evaluate accuracy manually
- Find 3 examples where an LLM confidently gives a wrong answer in a manufacturing context and document how you would catch each one

---

### Session 6: First Agent — Text-to-SQL

**Why:** The fastest way to understand agents is to build one that does something immediately useful. A Text-to-SQL agent answers real business questions from natural language. Students see the full loop: question in, SQL generated, query executed, result shown. This is motivating and sets the pattern for every agent that follows.

**Topics and activities:**
- LangChain basics: `ChatOpenAI`, `ChatPromptTemplate`, `StrOutputParser`
- Building the Text-to-SQL agent step by step
- Injecting schema context into the prompt so the LLM generates valid SQL
- Running the generated SQL with DuckDB
- Handling SQL errors: retry logic, validation before execution
- Displaying results cleanly in a Streamlit page
- First taste of the agent loop: question -> prompt -> LLM -> SQL -> execute -> answer

**Homework options:**
- Extend the Text-to-SQL agent to handle 10 question types and log every failure with the broken SQL and the error message
- Add a "did this answer your question?" feedback loop to the Streamlit interface, and track how often the agent needs a retry
- Write a prompt that makes the SQL agent explain its query in plain English after generating it — evaluate if the explanation matches what the SQL actually does

---

### Session 7: LangGraph Core Concepts

**Why:** LangGraph is the orchestration backbone of the final system. Before building complex agent networks, students need to understand the graph paradigm deeply: what a node is, what state is, and how routing decisions happen. Getting this wrong means building a system that is impossible to debug.

**Topics and activities:**
- `StateGraph`, `TypedDict` state, `add_node`, `add_edge`, `add_conditional_edges`
- Building a 3-node pipeline: classifier node, two specialist nodes, one output node
- Passing state between nodes: what goes in, what comes out
- Conditional routing: how the graph decides where to go next
- Checkpointing: saving and resuming state mid-workflow
- Visualizing the graph with `draw_mermaid`
- Debugging: how to log every state transition

**Homework options:**
- Build a LangGraph workflow with at least 4 nodes that routes a manufacturing question to one of three different analysis strategies and produces a short text summary
- Add error handling: if a node fails, the graph should route to a fallback node instead of crashing — demonstrate it breaking and recovering
- Draw the architecture of the final 10-agent system by hand or in a diagram tool, label every node, edge, and state key — bring it to Session 8 for discussion

---

## Phase 3: Building the System
### Sessions 8-13 — Build each agent, then wire them together

---

### Session 8: System Design Session — Architecture Before Code

**Why:** Teams that skip architecture end up with spaghetti agents that share no state and cannot communicate. One session spent designing the full system before writing it saves three sessions of refactoring later. This is also where the team divides ownership.

**Topics and activities:**
- Review Session 7 homework diagrams as a team — argue about them
- Define the full agent list, responsibilities, and interfaces
- Define the shared state schema: what fields every agent reads and writes
- Define the data contracts: what format does each agent's output take?
- Assign agent ownership to students or pairs
- Set up the shared Git repository, branch strategy, and file structure
- Define "done" for each agent: what does a working agent look like?

**Homework options:**
- Write a one-page spec for your assigned agent: inputs, outputs, prompt design, failure modes, and how you will test it
- Implement the skeleton of your agent: a node function that accepts state and returns updated state, even if the logic inside is a placeholder
- Write 5 test cases for your agent: input state, expected output state, edge cases

---

### Session 9: Data Understanding + SQL Writer + SQL Validator Agents

**Why:** These three agents are the entry point of the system. Every other agent depends on clean, queryable data and validated SQL. They also happen to combine everything students learned in Sessions 2-6, making them a great starting point for the build phase.

**Topics and activities:**
- Data Understanding Agent: schema inspection, statistical profiling, data quality flags, output as structured state
- SQL Writer Agent: schema-aware prompt, business question as input, SQL as output
- SQL Validator Agent: parse the SQL, check table and column names exist, check syntax, approve or reject with reason
- Chaining all three in a LangGraph sub-graph
- Testing with intentionally bad inputs: missing columns, ambiguous questions, unknown tables

**Homework options:**
- Run the three-agent chain against 15 business questions, log every failure, and fix at least 5 of them before next session
- Add a confidence score to the SQL Validator: low confidence triggers a re-generation loop, high confidence passes through — test the threshold
- Stress test the Data Understanding Agent with a messy ZF-inspired dataset and evaluate how well it describes the problems it finds

---

### Session 10: Data Cleaning Agent + EDA Agent

**Why:** The system cannot reason about data it has not understood and cleaned. The EDA Agent is also where the first human-readable insights are generated — students see the system "thinking" about data for the first time. It is a motivating milestone.

**Topics and activities:**
- Data Cleaning Agent: missing value strategy, type coercion, deduplication, outlier flagging, writing cleaned output back to state
- EDA Agent: distributions, outlier detection, correlation matrix, trend detection per station, summary statistics
- Structuring agent output as a findings dictionary the Root-Cause agent can read later
- Using the LLM to narrate EDA findings in plain language
- Debugging state: how to inspect what each agent added

**Homework options:**
- Feed both agents a dataset with 7 planted data quality problems and evaluate how many each agent catches and how many it misses
- Extend the EDA Agent to produce a Markdown summary of its top 5 findings automatically — test it on 3 different datasets
- Write a unit test for the Data Cleaning Agent that verifies it handles each problem type correctly

---

### Session 11: Anomaly Detection Agent + Root-Cause Investigation Agent

**Why:** This is the core intelligence of the system. Everything so far has been preparation for this moment. Students go from describing data to explaining it. The Root-Cause Agent is also the most challenging prompt engineering task in the project — it requires combining findings from multiple upstream agents.

**Topics and activities:**
- Anomaly Detection Agent: z-score, IQR method, rolling standard deviation, flagging unusual events per station/shift/operator/batch
- Writing anomalies into state as structured records with severity and context
- Root-Cause Investigation Agent: reading anomaly records + EDA findings + SQL results, correlating across dimensions, generating hypotheses
- Prompt engineering for root-cause reasoning: separating facts from interpretations
- Confidence levels: how to make the agent express uncertainty rather than overclaim
- Testing: planting real anomalies in the dataset and evaluating the hypothesis quality

**Homework options:**
- Create a benchmark dataset with 5 known root causes (e.g. one bad material batch, one failing machine) and evaluate how well the agent identifies each one
- Extend the Root-Cause Agent to ask clarifying questions when it lacks enough evidence — design the follow-up loop in LangGraph
- Compare the agent's root-cause hypotheses against a manual investigation of the same dataset — write a short honest evaluation

---

### Session 12: Visualization Agent + Report Writer Agent

**Why:** Raw findings are invisible to business stakeholders. These two agents turn the system's internal analysis into something a plant manager can read and a quality engineer can act on. Report quality is also a proxy for the quality of the whole pipeline — if the report is weak, something upstream is weak.

**Topics and activities:**
- Visualization Agent: auto-selecting chart types based on finding type, generating Plotly figures, saving chart objects to state
- Report Writer Agent: structured Markdown output, sections for method, findings, anomalies, root-cause hypotheses, recommendations, confidence levels, caveats
- Prompt design for the report: clear separation of "what the data shows" vs "what we think it means"
- Displaying the report and charts in Streamlit
- Iterating on report quality: what makes a manufacturing report trustworthy vs vague?

**Homework options:**
- Run the full pipeline end-to-end and evaluate the generated report against the rubric: clarity, accuracy, supported claims, appropriate caveats
- Design a report template and enforce it via structured output — the agent must populate every section or flag it as insufficient data
- Have a non-technical person read the generated report and give feedback — bring their comments to Session 13

---

## Phase 4: Integration and Delivery
### Sessions 13-15 — Wire the system together, ship the interface, present to ZF Life

---

### Session 13: Orchestrator Agent + Human-in-the-Loop

**Why:** Individual agents working in isolation are not a system. The Orchestrator is what makes the whole thing behave intelligently as a unit. Human-in-the-loop is what makes it trustworthy enough to present to ZF Life. These two elements elevate the project from a demo to a responsible AI system.

**Topics and activities:**
- Orchestrator Agent: receives the user question, decides which agents to invoke and in what order, handles routing failures
- Conditional orchestration: when does the system need more data vs proceed to report?
- LangGraph `interrupt`: pausing the graph and waiting for human input
- Human approval gate: before the report is finalised, a human reviews the root-cause hypotheses
- Resume after approval: the graph picks up from where it paused
- Logging every agent action with timestamps and state snapshots

**Homework options:**
- Simulate an adversarial run: feed the system a question it was not designed for and document how the Orchestrator handles it
- Add a human correction step: the reviewer can edit the root-cause hypothesis before the Report Writer generates the final report
- Build a simple admin panel in Streamlit that shows the full agent execution trace for any given run

---

### Session 14: Full System Integration + Streamlit Interface

**Why:** Students have all the agents built. This session is pure assembly. It is also where the reality of integration sets in — interfaces that looked clean in isolation start to conflict. Debugging a live multi-agent system under time pressure is the best possible preparation for professional AI development.

**Topics and activities:**
- Connecting all agents in the main LangGraph StateGraph
- End-to-end run: user types a question, system produces a full report
- Streamlit interface: question input, live agent status display, chart panel, report view, human approval panel
- Error handling: agent failures should not crash the whole system
- Environment variables and API key management
- Basic performance: where is the system slow, and why?
- Final polish: README, requirements.txt, demo data bundle

**Homework options:**
- Run the complete system 10 times with different questions, log every failure and every surprising output, fix the top 3 issues before demo day
- Write the README as if you are handing the project to a new developer who has never seen it — include setup, usage, known limitations
- Prepare your 5-minute demo script: one real question, live run, walk through the results — practice it twice

---

### Session 15: Demo Day

**Why:** There is no better teacher than a live demo in front of a real audience. Students defend their work, explain their architectural decisions, and receive honest feedback. If ZF Life attends, the students experience what it means to present AI-assisted analysis to an industrial sponsor. This session does not exist just to evaluate — it exists to launch the next thing.

**Format:**
- Each student or pair presents their assigned agent: design decisions, what worked, what failed, what they would do differently
- Full system demo: one live question run end-to-end in front of the group
- Open Q&A: the audience tries to break it with edge-case questions
- Honest retrospective: what the system can do, what it cannot, what would be needed to move it toward production
- If ZF Life is present: demo with real questions from their domain

**Homework options (post-course reflection):**
- Write a one-page technical post-mortem: biggest mistake made, how it was caught, how it was fixed
- Write a one-page proposal for what version 2 of this system would look like if the team had three more months
- Open source the project on GitHub with a clean README, architecture diagram, and demo video

---

## Session Map Summary

| Session | Theme | Phase |
|---|---|---|
| 1 | Pandas First Contact | Data Foundation |
| 2 | Pandas Deeper + Data Cleaning | Data Foundation |
| 3 | SQL for Data Investigators | Data Foundation |
| 4 | Visualization + Streamlit Dashboard | Data Foundation |
| 5 | LLM Fundamentals for Builders | LLM and Agents |
| 6 | First Agent: Text-to-SQL | LLM and Agents |
| 7 | LangGraph Core Concepts | LLM and Agents |
| 8 | System Design Session | Build Phase |
| 9 | Data Understanding + SQL Agents | Build Phase |
| 10 | Data Cleaning + EDA Agents | Build Phase |
| 11 | Anomaly Detection + Root-Cause Agents | Build Phase |
| 12 | Visualization + Report Writer Agents | Build Phase |
| 13 | Orchestrator + Human-in-the-Loop | Integration |
| 14 | Full Integration + Streamlit Interface | Integration |
| 15 | Demo Day | Delivery |

---

## Coaching Notes

**On using AI during sessions:** Encourage it aggressively. The goal is not to memorize Pandas or LangGraph syntax. The goal is to know enough to direct AI tools, evaluate their output, and fix what breaks. Students who use AI well build faster and understand more.

**On homework:** Homework options are deliberately varied in difficulty. Let students choose. The student who does the hardest option and struggles learns more than the student who does the easy option perfectly. Do not equalize outcomes — identify and amplify outliers.

**On the ZF Life angle:** Reference the real project in every session. When teaching SQL joins, use steering wheel station tables. When teaching anomaly detection, use scrap rate time series. Students who see the destination from Session 1 build differently than students who are working through abstract exercises.

**On team dynamics:** By Session 8, teams are forming. Watch for students who hide behind group work and students who take over. The system needs every agent to work, which means every student must own something real.

**On time pressure:** 15 sessions is tight. If a session runs over on fundamentals, cut the exercise and move the homework. Never sacrifice architecture discussions to finish a code example. The system design in Sessions 7 and 8 determines the quality of everything in Sessions 9-14.
