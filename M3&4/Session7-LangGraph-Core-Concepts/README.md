# Session 7 · LangGraph Core Concepts
### Build Stateful Multi-Agent Orchestrations 🕸️🧠

Welcome to Session 7! In this session, you are going to transition from single-prompt linear chains to **stateful, cyclic multi-agent graphs** using **LangGraph**.

As agents grow in complexity, managing loops, routing decisions, and safety gates in raw Python code gets messy. LangGraph introduces a clean graph-based paradigm where you model your system as **nodes** (functions that perform actions) and **edges** (paths that define routing and execution flows), all driven by a shared, mutable **State**.

---

## 🎯 Learning Objectives

By the end of this lab, you will deeply understand:
1. **The Graph Paradigm:** How to initialize and compile a `StateGraph`.
2. **Shared State:** Using a `TypedDict` as the single source of truth that flows between nodes.
3. **Conditional Routing:** Designing classifier nodes and using `add_conditional_edges` to route execution dynamically.
4. **State Reducers:** Aggregating data (like logs or chat histories) using `Annotated` lists with `operator.add` instead of overwriting keys.
5. **Human-in-the-Loop Approval:** Pausing graph execution using checkpointing (`MemorySaver`) and `interrupt_before` to request supervisor clearance, then resuming execution.

---

## 🚀 3 Popular Production Use Cases for LangGraph

LangGraph is used in enterprise environments to orchestrate complex operations. The three most common success patterns are:

1. **Smart Routing & Triage (Classifier + Specialists)**
   * **What it does:** An incoming user query or task is triaged by an LLM classifier, which routes the request to specialized agents, sub-graphs, or toolchains.
   * **Why it works:** It prevents a single LLM from having to know too many tools, improving accuracy, reducing cost, and keeping prompts modular.
   * **Example:** Support triage (routing to billing agent vs. technical repair agent vs. refund agent).

2. **Self-Correction & Evaluation Loops (Coding & RAG)**
   * **What it does:** The graph loops back on itself. A generator node creates code or SQL, a validator node compiles and checks it for errors, and if it fails, it routes back to the generator along with the error logs to self-repair.
   * **Why it works:** Humans debug code by trying, inspecting errors, and fixing. This loop teaches the LLM to do the same autonomously before showing the output to a user.
   * **Example:** Code generation, Text-to-SQL self-correction.

3. **Human-in-the-Loop Approval Gates (Checkpoints)**
   * **What it does:** The graph saves its state at every step. Before performing an expensive, irreversible, or sensitive action, the graph halts and waits. A human reviews the action, approves/modifies it, and the graph resumes from where it left off.
   * **Why it works:** It brings peace of mind to enterprise teams deploying AI, maintaining a clear boundary of human accountability.
   * **Example:** Automatically drafting emails but pausing for review, trading stocks, or scheduling heavy machine maintenance.

*In this lab, we build a simplified hybrid of **Use Case 1 (Routing)** and **Use Case 3 (Human-in-the-Loop)** applied to our steering wheel manufacturing dataset!*

---

## 🛠️ Step 0: Setup and Environment

1. **Activate your virtual environment** in your terminal:
   ```bash
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```

2. **Install LangGraph**:
   We have added `langgraph` to the project's root `requirements.txt`. Navigate to the project root and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Copy your API Key**:
   Since you already configured Mistral in Session 6, copy your `.env` file to this folder:
   ```bash
   cp ../Session6-First-Agent-Text-to-SQL/.env .env
   ```

4. **Verify Session 3 Data:**
   Make sure the steering wheel manufacturing Parquet database is present. This lab's nodes will execute live queries on them. If they are missing, navigate to `Session3-SQL-DuckDB` and run `python generate_steering_wheel_data.py`.

---

## 📁 File Progression & Learning Path

Run these files step-by-step. Each file contains explanations and a hands-on **Challenge** to complete.

### [00_setup_check.py](00_setup_check.py)
* **Goal:** Verify that `langgraph` is successfully installed and a minimal graph compiles.
* **Run:** `python 00_setup_check.py`

### [01_state_and_nodes.py](01_state_and_nodes.py)
* **Goal:** Learn how state works, how nodes receive state, modify keys, and return updates.
* **Run:** `python 01_state_and_nodes.py`

### [02_conditional_routing.py](02_conditional_routing.py)
* **Goal:** Model conditional logic. Categorize queries with Mistral and route them to either production database query nodes or maintenance logging nodes.
* **Run:** `python 02_conditional_routing.py`

### [03_state_reducers.py](03_state_reducers.py)
* **Goal:** Learn how to aggregate execution logs and list records over time using state reducers (`operator.add`) instead of overwriting keys.
* **Run:** `python 03_state_reducers.py`

### [04_human_in_the_loop.py](04_human_in_the_loop.py)
* **Goal:** Implement human verification. Learn how checkpoints and interrupts allow pausing, updating state (e.g., approving an action), and resuming the graph.
* **Run:** `python 04_human_in_the_loop.py`

### [05_streamlit_app.py](05_streamlit_app.py)
* **Goal:** Assemble these blocks into an interactive supervisor dashboard. Render the compiled graph visually, run queries, stream node execution states live, and display approval gates for maintenance tasks!
* **Run:** `streamlit run 05_streamlit_app.py`

---

## ⚡ Pro-Tips for Success

* **Mermaid Graph Drawing:** If you see code instead of a PNG rendering of the graph in Streamlit's sidebar, it means your local machine lacks Python `pygraphviz` or graph drawing dependencies. The app automatically detects this and falls back to a web request to `mermaid.ink` to render the graphic!
* **Threads:** Remember, checkpoints require a `thread_id`. In Streamlit, each query uses a persistent thread ID. You can reset it in the sidebar to simulate starting a completely fresh user conversation.
