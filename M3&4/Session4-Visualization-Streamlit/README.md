# Session 4 — Visualization + Streamlit Dashboard
## Steering Wheel Manufacturing · Seaborn · Streamlit · (Plotly bonus)

We turn the Session 3 data into **charts you can read** and a **dashboard you can click**.
You already know Pandas (Session 1-2) and SQL (Session 3). Now you learn to *show* the
answers — the way an engineer presents findings to a plant manager.

---

## Learning goals

- **Seaborn** — bar, line, box, and heatmap charts, and how to *read* each one.
- **Streamlit** — build a web dashboard from a plain Python script (no HTML/CSS/JS).
- **Plotly (optional)** — one interactive chart for hover/zoom exploration.
- **Engineer's mindset** — every chart answers a real manufacturing business question.

---

## Prerequisites

- Project virtual environment active (from repo root):
  ```bash
  source .venv/bin/activate            # Windows: .venv\Scripts\activate
  pip install -r requirements.txt      # installs seaborn, matplotlib, plotly, streamlit
  ```
- **Data comes from Session 3.** This session reads
  `../Session3-SQL-DuckDB/data/*.parquet` directly. If that folder is empty, run
  the generator first:
  ```bash
  python ../Session3-SQL-DuckDB/generate_steering_wheel_data.py
  ```

---

## How to run

**Notebook (start here):**
```bash
jupyter notebook session4_seaborn_explore.ipynb
```

**Streamlit scripts (run one at a time):**
```bash
streamlit run 01_hello_streamlit.py
```
Streamlit opens a browser tab. Edit a file, hit **Save**, and it offers to rerun —
that live-reload loop is how you'll work all session.

> Tip: stop a running app with `Ctrl+C` in the terminal before launching the next one.

---

## The walkthrough — small steps, small wins

| File | Business question | New concepts |
|------|-------------------|--------------|
| `session4_seaborn_explore.ipynb` | How do I *read* a chart? | Seaborn bar / line / box / heatmap |
| `01_hello_streamlit.py` | (learn the tool) | `st.title`, `st.write`, `st.metric`, rerun model |
| `02_load_and_kpis.py` | How many units, how much scrap? | `@st.cache_data`, `st.columns`, KPI metrics |
| `03_seaborn_in_streamlit.py` | Which station scraps most? | `fig, ax` + `st.pyplot` |
| `04_filters_and_tabs.py` | Scrap by shift & product type? | `st.sidebar`, `st.multiselect`, `st.tabs` |
| `05_dashboard.py` | Full factory health snapshot | 6 KPIs + 4 charts, layered structure |
| `06_plotly_bonus.py` | Do out-of-spec temps cause scrap? | `plotly.express`, `st.plotly_chart` |

Every script ends with a **"Your Challenge"** block — do it before moving on.

---

## The 6 dashboard KPIs (in `05_dashboard.py`)

| KPI | Meaning | Good direction |
|-----|---------|----------------|
| Total units | Wheels that entered molding | — |
| Scrap rate | % scrapped at molding | ↓ lower |
| Rework rate | % sent to rework at molding | ↓ lower |
| **First Pass Yield** | % of wheels that passed **every** station on their route first try | ↑ higher |
| **Out-of-Spec rate** | % of readings breaching an SIC tolerance (temp / foam / resistance) | ↓ lower |
| **Avg daily throughput** | Average wheels finished per day | ↑ higher |

> **Why is First Pass Yield (~60%) so much lower than each station's ~2-3% scrap?**
> Because a wheel must survive *all* its stations. Small losses multiply along the route.
> That insight is the heart of manufacturing quality thinking.

---

## Shared data layer — `data_utils.py`

All loading and KPI math lives here so the display scripts stay short:

- `load_all()` — every station table as a dict of DataFrames.
- `scrap_rate_by(...)`, `scrap_rate_by_station(...)`, `weekly_scrap_trend(...)` — chart-ready tables.
- `apply_filters(...)` — filter by product type / shift.
- `first_pass_yield(...)`, `out_of_spec_rate(...)`, `daily_throughput(...)` — the headline KPIs.

Sanity-check the data layer any time:
```bash
python data_utils.py
```

---

## Homework options (pick one)

1. **KPI dashboard** — extend `05_dashboard.py` to at least **4 chart types and 2 filters**
   covering machines/tools, shifts, and defect types. Add an operator ranking.
2. **Red-flag view** — a Streamlit page that auto-highlights anomalous records with
   colour-coded tables and alert metrics (e.g. every molding row outside 180-220 °C).
3. **Reproduce a real report** — find a public manufacturing report online and recreate
   3 of its charts using our steering wheel data.

---

## Folder structure

```
Session4-Visualization-Streamlit/
├── data_utils.py                    ← shared loaders + KPI helpers
├── session4_seaborn_explore.ipynb   ← start here: read charts
├── 01_hello_streamlit.py
├── 02_load_and_kpis.py
├── 03_seaborn_in_streamlit.py
├── 04_filters_and_tabs.py
├── 05_dashboard.py                  ← the full dashboard
├── 06_plotly_bonus.py               ← optional interactive charts
└── README.md
```

Data is read from `../Session3-SQL-DuckDB/data/` — no duplicate files.

---

## Troubleshooting

- **`FileNotFoundError: station_*.parquet`** — run the Session 3 generator (see Prerequisites).
- **`ModuleNotFoundError: streamlit/seaborn/plotly`** — `pip install -r requirements.txt` with the venv active.
- **Blank/again-and-again reloading page** — make sure you launched with `streamlit run <file>.py`, not `python <file>.py`.
