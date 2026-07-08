# Session 6 · First Agent — Text-to-SQL
### Build a Self-Correcting Database Investigator Agent ⚙️🔍

Welcome to Session 6! In this session, you are going to take your first leap into the world of **AI Agents**.

Instead of writing static prompts that output text, you are going to build a system that **performs actions** (writing and running database queries), **inspects its own errors**, and **auto-corrects its logic** until it accomplishes the goal. 

Specifically, you will build a Text-to-SQL agent that connects to the 8 Parquet files of steering wheel manufacturing data you generated in Session 3, and lets factory supervisors ask complex, multi-table production questions in plain English.

---

## 🎯 Learning Objectives

By the end of this lab, you will deeply understand:
1. **Context Engineering:** How to extract a database schema catalog and inject it into an LLM prompt so the model writes valid table joins.
2. **LLM Guardrails & Security:** Why you never let an LLM run raw SQL directly, and how to build validators that block write/modify commands (`DROP`, `DELETE`) and restrict table access boundaries.
3. **The Self-Correction Loop:** How to catch database execution errors, package them up, send them back to the LLM, and prompt it to auto-repair its code.
4. **plain-English Explanations:** Bridging the gap between raw database tables and business decision-makers.
5. **Interactive UI Delivery:** Assembling the steps into a sleek, real-time Streamlit dashboard.

---

## 🛠️ Step 0: Setup and API Key

We will use **Mistral AI**'s specialized coding model, **Codestral**, for this lab. Mistral offers an exceptional developer platform with a generous free tier (no credit card required!).

1. **Activate your virtual environment** in your terminal:
   ```bash
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```
2. **Install the Mistral LangChain integration**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Get a free Mistral API key**:
   - Go to [Mistral Console](https://console.mistral.ai/) and sign up.
   - Create an API key.
4. **Configure your environment**:
   - In this folder, copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and paste your key:
     ```env
     MISTRAL_API_KEY=your-actual-api-key-here
     ```
   - Save the file. (Note: `.env` is git-ignored to keep your key secure).

---

## 📁 File Progression & Learning Path

Run these files step-by-step. Each file introduces a single concept, followed by a **Challenge** to test your understanding.

### [00_setup_check.py](00_setup_check.py)

* **Goal:** Verify that your virtual environment is active, packages are installed, and your Mistral key successfully communicates with the server.
* **Run:** `python 00_setup_check.py`

### [01_schema_extractor.py](01_schema_extractor.py)
* **Goal:** Understand context engineering. Learn how to extract database catalog parameters (tables, column names, data types) from DuckDB and format them into a clean string to guide the LLM.
* **Run:** `python 01_schema_extractor.py`

### [02_raw_text_to_sql.py](02_raw_text_to_sql.py)
* **Goal:** Build the raw Text-to-SQL translation pipeline. Send the schema and user question to Codestral, clean the output, and run it directly in DuckDB.
* **Run:** `python 02_raw_text_to_sql.py`

### [03_sql_validator.py](03_sql_validator.py)
* **Goal:** Implement safety guardrails. Build static analysis filters that reject unsafe queries containing modification keywords or unauthorized system catalog access.
* **Run:** `python 03_sql_validator.py`

### [04_retry_loop.py](04_retry_loop.py)
* **Goal:** Implement self-correction. If a query fails to validate or execute, catch the error, feed the failure history back to the LLM, and let it self-correct.
* **Run:** `python 04_retry_loop.py`

### [05_explanation.py](05_explanation.py)
* **Goal:** Humanize the database. Feed the SQL results and original question back to Mistral to generate a natural, structured plain-English answer for supervisors.
* **Run:** `python 05_explanation.py`

### [06_streamlit_app.py](06_streamlit_app.py)
* **Goal:** Build the complete dashboard. An interactive interface featuring a schema sidebar, text input, real-time agent execution logging (`st.status`), raw tables, and dynamic visual charting.
* **Run:** `streamlit run 06_streamlit_app.py`

---

## ⚡ Pro-Tips for Success

1. **Verify your Session 3 Data:** The scripts load Parquet data relative to the Session 3 folder. If you get a `FileNotFoundError`, go back to `M3&4/Session3-SQL-DuckDB` and run:
   ```bash
   python generate_steering_wheel_data.py
   ```
2. **Watch the logs:** As the agent executes in `06_streamlit_app.py`, expand the execution status steps. Watch the agent detect a column syntax error (like `resistance` instead of `resistance_ohm`) and repair it in real-time.
3. **API Rate Limits:** While Mistral's developer free trial is generous, avoid running rapid loops in multiple terminals to prevent rate limiting.
