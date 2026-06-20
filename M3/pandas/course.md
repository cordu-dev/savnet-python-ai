# Course Title

**Pandas for Manufacturing Data Analysis: A 2-Hour Practical Launch**

## Course Positioning

This course is designed for students who have already completed Python 1 and Python 2 essentials and are ready to start working with real data.

The course focuses specifically on **Pandas**, using simple manufacturing datasets that gradually introduce students to practical data analysis tasks such as loading data, inspecting production records, cleaning missing values, calculating scrap rates, grouping by machines and shifts, and preparing results for a simple Streamlit app.

This is not a full data science course yet. It is a focused starter module that gives students enough confidence to continue individual study and later connect Pandas with SQL, dashboards, and AI-assisted root-cause analysis.

---

# Target Students

Students who already know basic Python, including:

* variables and data types
* lists and dictionaries
* loops and conditions
* functions
* files
* basic problem-solving in Python

The course starts directly with Pandas-specific thinking.

---

# Duration

**Live session: 2 hours**

Recommended individual follow-up study: **4–8 additional hours**

---

# Tools Used

* Python
* Pandas
* Jupyter Notebook
* Streamlit
* CSV manufacturing datasets
* Optional: Matplotlib or Seaborn for quick charts

---

# Course Theme

**Manufacturing Data Analysis**

Students work with simplified factory datasets such as:

* production records
* machine output
* shift performance
* defect counts
* scrap quantities
* inspection results

The examples start simple and gradually move toward real manufacturing questions.

---

# Learning Outcomes

By the end of the 2-hour session, students should be able to:

1. Understand what a Pandas DataFrame is and why it is useful.
2. Load a manufacturing CSV file into Pandas.
3. Inspect rows, columns, data types, and missing values.
4. Select, filter, and sort production data.
5. Create new calculated columns such as scrap rate.
6. Group data by machine, shift, or defect type.
7. Identify simple patterns in manufacturing data.
8. Use Jupyter Notebook for exploration.
9. Build a very small Streamlit app that displays a dataset and a simple summary.
10. Continue studying independently using structured practice tasks.

---

# Dataset 1: Simple Production Log

Students begin with a small CSV file like this:

| batch_id | date       | shift   | machine | units_produced | defective_units |
| -------- | ---------- | ------- | ------- | -------------: | --------------: |
| B001     | 2026-01-05 | Morning | M1      |            500 |              12 |
| B002     | 2026-01-05 | Morning | M2      |            460 |              18 |
| B003     | 2026-01-05 | Evening | M1      |            520 |               9 |
| B004     | 2026-01-06 | Night   | M3      |            430 |              25 |

Later datasets can add:

* operator
* material batch
* defect type
* temperature
* pressure
* cycle time
* inspection result

---

# 2-Hour Live Lesson Plan

## Lesson 1 — Why Pandas for Manufacturing Data?

**Time:** 10 minutes

### Goal

Help students understand why Pandas matters in real production and quality contexts.

### Instructor Talking Points

Manufacturing companies generate data from machines, inspections, operators, materials, shifts, and production lines. Pandas helps analysts answer practical questions such as:

* Which machine has the highest scrap rate?
* Which shift produces the most defects?
* Are defective units increasing over time?
* Which batches should be investigated?
* Is the data clean enough to trust?

### Student Activity

Students open a Jupyter Notebook and look at the first manufacturing CSV file.

### Learning Outcome

Students understand the role of Pandas as a practical tool for investigating tabular manufacturing data.

---

## Lesson 2 — Loading and Inspecting Data in Jupyter Notebook

**Time:** 20 minutes

### Concepts

* importing Pandas
* reading CSV files
* DataFrame basics
* previewing rows
* checking columns
* checking shape
* checking data types
* checking missing values

### Example Code

```python
import pandas as pd

df = pd.read_csv("production_log.csv")

df.head()
df.shape
df.columns
df.info()
df.isna().sum()
```

### Exercise

Students answer these questions:

1. How many production records are in the dataset?
2. How many columns does the dataset have?
3. Which columns are numeric?
4. Are there missing values?
5. What does one row represent?

### Learning Outcome

Students can load a CSV file and perform a first inspection of a manufacturing dataset.

---

## Lesson 3 — Selecting, Filtering, and Sorting Production Data

**Time:** 25 minutes

### Concepts

* selecting columns
* filtering rows
* multiple conditions
* sorting values
* basic comparison operators

### Example Code

```python
df["machine"]

df[["machine", "shift", "units_produced"]]

df[df["machine"] == "M1"]

df[df["defective_units"] > 15]

df[(df["machine"] == "M2") & (df["shift"] == "Morning")]

df.sort_values("defective_units", ascending=False)
```

### Manufacturing Questions

Students use Pandas to answer:

1. Which records belong to Machine M1?
2. Which batches had more than 15 defective units?
3. Which production record had the highest number of defects?
4. Which night-shift records should be reviewed?

### Learning Outcome

Students can extract relevant production records using filters and sorting.

---

## Lesson 4 — Creating Manufacturing Metrics

**Time:** 20 minutes

### Concepts

* creating new columns
* calculating scrap rate
* rounding values
* interpreting calculated metrics

### Example Code

```python
df["scrap_rate"] = df["defective_units"] / df["units_produced"]

df["scrap_rate_percent"] = df["scrap_rate"] * 100

df["scrap_rate_percent"] = df["scrap_rate_percent"].round(2)

df.head()
```

### Exercise

Students answer:

1. Which batch has the highest scrap rate?
2. Is the batch with the most defects always the batch with the worst scrap rate?
3. Why is percentage often more useful than raw defect count?

### Learning Outcome

Students understand how to create useful business metrics from raw manufacturing data.

---

## Lesson 5 — Grouping by Machine and Shift

**Time:** 25 minutes

### Concepts

* groupby
* aggregation
* mean
* sum
* count
* sorting grouped results

### Example Code

```python
machine_summary = df.groupby("machine").agg({
    "units_produced": "sum",
    "defective_units": "sum",
    "scrap_rate_percent": "mean"
})

machine_summary
```

```python
shift_summary = df.groupby("shift").agg({
    "units_produced": "sum",
    "defective_units": "sum",
    "scrap_rate_percent": "mean"
}).sort_values("scrap_rate_percent", ascending=False)

shift_summary
```

### Manufacturing Questions

Students answer:

1. Which machine produced the most units?
2. Which machine had the most defective units?
3. Which machine had the highest average scrap rate?
4. Which shift looks most suspicious?
5. What further data would we need before blaming a machine or shift?

### Learning Outcome

Students can summarize manufacturing performance by category and avoid jumping to unsupported conclusions.

---

## Lesson 6 — First Mini Streamlit App

**Time:** 15 minutes

### Goal

Students see how a notebook analysis can become a simple interactive data app.

### Streamlit App Example

```python
import streamlit as st
import pandas as pd

st.title("Manufacturing Production Dashboard")

df = pd.read_csv("production_log.csv")

st.subheader("Raw Production Data")
st.dataframe(df)

df["scrap_rate_percent"] = (
    df["defective_units"] / df["units_produced"] * 100
).round(2)

st.subheader("Machine Summary")
machine_summary = df.groupby("machine").agg({
    "units_produced": "sum",
    "defective_units": "sum",
    "scrap_rate_percent": "mean"
})

st.dataframe(machine_summary)

selected_machine = st.selectbox(
    "Select a machine",
    df["machine"].unique()
)

filtered_df = df[df["machine"] == selected_machine]

st.subheader(f"Records for Machine {selected_machine}")
st.dataframe(filtered_df)
```

### Student Activity

Students run the app locally:

```bash
streamlit run app.py
```

### Learning Outcome

Students understand that Pandas can power simple dashboards and interactive analysis tools.

---

## Lesson 7 — Mini-Project Brief

**Time:** 5 minutes introduction during live session
**Recommended completion time:** 2–4 hours individually

# Mini-Project: Simple Scrap Analysis Dashboard

## Scenario

A factory manager is worried that scrap is increasing in the production process. Students receive a simplified production dataset and must use Pandas to investigate machine and shift performance.

## Student Tasks

### Part 1 — Jupyter Notebook Analysis

Students must create a notebook that:

1. Loads the manufacturing dataset.
2. Shows the first rows.
3. Checks data types and missing values.
4. Calculates scrap rate percentage.
5. Finds the batch with the highest scrap rate.
6. Groups results by machine.
7. Groups results by shift.
8. Writes 3–5 observations in markdown.

### Part 2 — Streamlit Dashboard

Students must create a simple Streamlit app that includes:

1. A title and short project description.
2. The raw dataset.
3. A machine-level summary table.
4. A shift-level summary table.
5. A machine filter.
6. A short conclusion section.

### Part 3 — Business Interpretation

Students answer:

1. Which machine should be investigated first?
2. Which shift has the highest average scrap rate?
3. What additional data would help confirm the root cause?
4. Why should we avoid blaming an operator or machine based only on this small dataset?

---

# Suggested Mini-Project Dataset Columns

The mini-project dataset should include:

| Column          | Description                |
| --------------- | -------------------------- |
| batch_id        | Unique batch code          |
| date            | Production date            |
| shift           | Morning, Evening, or Night |
| machine         | Machine ID                 |
| operator        | Operator code              |
| units_produced  | Number of produced units   |
| defective_units | Number of defective units  |
| defect_type     | Main defect category       |
| material_batch  | Material batch code        |

Optional advanced columns:

| Column      | Description                 |
| ----------- | --------------------------- |
| temperature | Machine/process temperature |
| pressure    | Process pressure            |
| cycle_time  | Time per production cycle   |
| humidity    | Environmental humidity      |

---

# Exercises for Individual Study

## Practice Set 1 — Data Inspection

Students should practice:

1. Load a new CSV file.
2. Display the first 10 rows.
3. Show the number of rows and columns.
4. List all column names.
5. Check data types.
6. Find missing values.

## Practice Set 2 — Filtering

Students should answer:

1. Show only records from Machine M1.
2. Show only night-shift records.
3. Show records where defective units are greater than 20.
4. Show records where scrap rate is above 5%.
5. Show records for Machine M2 during the evening shift.

## Practice Set 3 — Metrics

Students should create:

1. `scrap_rate`
2. `scrap_rate_percent`
3. `good_units`
4. `is_high_scrap`, where scrap rate is greater than 5%

## Practice Set 4 — Grouping

Students should calculate:

1. Total units by machine.
2. Total defective units by machine.
3. Average scrap rate by machine.
4. Average scrap rate by shift.
5. Most common defect type by machine.

## Practice Set 5 — Streamlit Extension

Students should improve their app by adding:

1. A shift filter.
2. A defect type filter.
3. A chart showing defective units by machine.
4. A chart showing average scrap rate by shift.
5. A warning message when scrap rate is above a chosen threshold.

---

# Recommended Self-Study Path After the 2-Hour Session

## Step 1 — Pandas Core Skills

Students should study:

* selecting rows and columns
* filtering
* sorting
* missing values
* creating columns
* grouping and aggregation
* merging datasets
* working with dates

## Step 2 — Manufacturing Analysis Skills

Students should practice:

* scrap rate analysis
* defect type analysis
* machine comparison
* shift comparison
* production trend analysis
* suspicious batch detection

## Step 3 — Jupyter Notebook Reporting

Students should learn to:

* write markdown explanations
* organize notebooks clearly
* separate code, output, and interpretation
* present business conclusions

## Step 4 — Streamlit Apps

Students should learn to:

* display dataframes
* add filters
* add metrics
* add charts
* structure a simple dashboard

---

# Suggested Course Flow Beyond the First 2 Hours

This 2-hour starter can later grow into a longer Pandas module:

## Module 1 — Pandas Foundations

DataFrames, Series, loading CSV files, inspecting data.

## Module 2 — Cleaning Manufacturing Data

Missing values, duplicates, invalid values, inconsistent categories.

## Module 3 — Filtering and Investigating Production Records

Boolean filters, sorting, suspicious batches, high-scrap records.

## Module 4 — Grouping and Aggregation

Machine summaries, shift summaries, defect summaries.

## Module 5 — Joining Manufacturing Tables

Production table, inspection table, material table, machine table.

## Module 6 — Time-Based Analysis

Dates, trends, rolling averages, production drift.

## Module 7 — Visualization for Manufacturing Data

Bar charts, line charts, defect distribution, scrap trends.

## Module 8 — Streamlit Dashboard

Interactive filters, summary cards, charts, conclusions.

## Module 9 — Mini Root-Cause Analysis Project

Students combine Pandas, Jupyter, and Streamlit to investigate a simplified manufacturing problem.

---

# Instructor Notes

Keep the first session practical and fast. Students should write code early, inspect real data, and answer manufacturing questions instead of only learning Pandas syntax.

The most important mindset is:

> Pandas is not just for manipulating tables. It is a tool for asking better questions about production, quality, machines, shifts, defects, and business decisions.

Students should also learn not to overclaim. A high scrap rate can suggest where to investigate, but it does not prove the root cause by itself.

---

# Final Student Deliverables

Each student should submit:

1. A Jupyter Notebook with the analysis.
2. A Streamlit app file.
3. The dataset used.
4. A short written conclusion with 3–5 findings.
5. One recommendation for further investigation.

---

# Simple Evaluation Rubric

| Criteria                              | Points |
| ------------------------------------- | -----: |
| Loads and inspects dataset correctly  |     20 |
| Calculates scrap rate correctly       |     20 |
| Uses filtering and grouping correctly |     20 |
| Creates a working Streamlit app       |     20 |
| Provides clear business observations  |     20 |

Total: **100 points**
