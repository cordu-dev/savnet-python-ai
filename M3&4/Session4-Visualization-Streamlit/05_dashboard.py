"""
Step 05 — The full manufacturing KPI dashboard
===============================================

This is the payoff: everything from steps 01-04 assembled into one clean app,
structured in the three layers a professional dashboard uses:

    1. LOAD    -> read the data (cached)
    2. PROCESS -> filter + compute KPIs (mostly in data_utils)
    3. DISPLAY -> KPI header, then four charts in tabs

Business questions answered on one screen:
    - Are we healthy overall?            -> KPI header (6 metrics)
    - Is quality drifting over time?     -> scrap trend line
    - Which station is worst?            -> station comparison bars
    - What kinds of defects dominate?    -> defect breakdown
    - When do problems cluster?          -> shift x station heatmap

Run it:
    streamlit run 05_dashboard.py
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

import data_utils as du

# ---------------------------------------------------------------------------
# 1. LOAD
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Factory Dashboard", page_icon="🏭", layout="wide")
sns.set_theme(style="whitegrid")


@st.cache_data
def get_data():
    return du.load_all()


frames = get_data()

# ---------------------------------------------------------------------------
# 2. SIDEBAR FILTERS (drive every KPI and chart below)
# ---------------------------------------------------------------------------
st.sidebar.header("🎛️ Filters")
molding = frames["molding"]
product_options = sorted(molding["product_type"].unique())
shift_options = sorted(molding["shift"].unique())

chosen_types = st.sidebar.multiselect(
    "Product type", product_options, default=product_options
)
chosen_shifts = st.sidebar.multiselect(
    "Shift", shift_options, default=shift_options
)

# Guard against an empty selection (which would filter everything away).
if not chosen_types:
    chosen_types = product_options
if not chosen_shifts:
    chosen_shifts = shift_options

# Pre-filter the molding table once — reused by several KPIs/charts.
mol_f = du.apply_filters(molding, chosen_types, chosen_shifts)

# ---------------------------------------------------------------------------
# 3. DISPLAY — header
# ---------------------------------------------------------------------------
st.title("🏭 Steering Wheel Factory — Quality Dashboard")
st.caption("Live KPIs across Molding · QC · Foaming · Conductor · Laser · Tapitat")

# --- KPI header: two rows of three metrics -------------------------------
# Row 1: the classics.
total_units = len(mol_f)
scrap_rate = (mol_f["cycle_result"] == "SCRAP").mean() * 100 if total_units else 0
rework_rate = (mol_f["cycle_result"] == "REWORK").mean() * 100 if total_units else 0

r1c1, r1c2, r1c3 = st.columns(3)
r1c1.metric("Total units", f"{total_units:,}")
r1c2.metric("Scrap rate", f"{scrap_rate:.2f}%", delta_color="inverse")
r1c3.metric("Rework rate", f"{rework_rate:.2f}%", delta_color="inverse")

# Row 2: the three KPIs we added for this session.
fpy = du.first_pass_yield(frames, chosen_types)
oos = du.out_of_spec_rate(frames, chosen_types)
throughput_df = du.daily_throughput(molding, chosen_types, chosen_shifts)
avg_throughput = throughput_df["units"].mean() if not throughput_df.empty else 0

r2c1, r2c2, r2c3 = st.columns(3)
# First Pass Yield: higher is better -> normal delta colour.
r2c1.metric("First Pass Yield", f"{fpy:.1f}%")
# Out-of-Spec Rate: lower is better -> inverse colour.
r2c2.metric("Out-of-Spec rate", f"{oos:.2f}%", delta_color="inverse")
r2c3.metric("Avg daily throughput", f"{avg_throughput:,.0f} units/day")

st.divider()

# ---------------------------------------------------------------------------
# 3b. DISPLAY — four charts in tabs
# ---------------------------------------------------------------------------
tab_trend, tab_station, tab_defect, tab_heat = st.tabs(
    ["📉 Scrap trend", "🏭 By station", "🧩 Defect mix", "🔥 Shift heatmap"]
)

# --- Chart 1: weekly scrap trend (LINE) ----------------------------------
with tab_trend:
    st.subheader("Is quality drifting over time?")
    trend = du.weekly_scrap_trend(mol_f, "cycle_result")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=trend, x="timestamp", y="scrap_rate_pct", marker="o", ax=ax)
    ax.set_xlabel("Week")
    ax.set_ylabel("Scrap rate (%)")
    ax.set_title("Molding scrap rate per week")
    st.pyplot(fig)

# --- Chart 2: scrap rate by station (BAR) --------------------------------
with tab_station:
    st.subheader("Which station is worst?")
    station_scrap = du.scrap_rate_by_station(frames)
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(
        data=station_scrap, y="station", x="scrap_rate_pct",
        order=station_scrap["station"], ax=ax, color="#c0392b",
    )
    ax.set_xlabel("Scrap rate (%)")
    ax.set_ylabel("Station")
    st.pyplot(fig)

# --- Chart 3: defect / outcome breakdown at QC (BAR) ---------------------
with tab_defect:
    st.subheader("What kinds of QC outcomes dominate?")
    qc = du.apply_filters(frames["quality_check"], chosen_types)
    outcome_counts = (
        qc["overall_result"].value_counts().rename_axis("outcome").reset_index(name="count")
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    # hue="outcome" + legend=False lets us colour bars per category without the
    # seaborn "palette without hue" deprecation warning.
    sns.barplot(
        data=outcome_counts, x="outcome", y="count", ax=ax,
        hue="outcome", palette="flare", legend=False,
    )
    ax.set_xlabel("QC outcome")
    ax.set_ylabel("Number of wheels")
    st.pyplot(fig)

# --- Chart 4: shift x station scrap heatmap (HEATMAP) --------------------
with tab_heat:
    st.subheader("When and where do problems cluster?")
    # Build a matrix: rows = shift, columns = station, values = scrap rate %.
    # Only stations that carry a `shift` column can be broken down this way;
    # here we use the stations that record shift or share molding's timing.
    heat_rows = []
    for name in ["molding"]:  # molding carries the shift label directly
        df = du.apply_filters(frames[name], chosen_types, chosen_shifts)
        rc = du.RESULT_COLUMNS[name]
        grp = df.assign(is_scrap=df[rc] == "SCRAP").groupby("shift")["is_scrap"].mean() * 100
        for shift, val in grp.items():
            heat_rows.append({"shift": shift, "station": name, "scrap_rate_pct": round(val, 2)})

    heat_df = pd.DataFrame(heat_rows)
    # pivot turns the long table into a grid ready for a heatmap.
    matrix = heat_df.pivot(index="shift", columns="station", values="scrap_rate_pct")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(matrix, annot=True, fmt=".2f", cmap="Reds", ax=ax)
    ax.set_title("Scrap rate (%) — shift vs station")
    st.pyplot(fig)
    st.info(
        "Right now only molding records a shift. Your challenge: enrich other "
        "stations with a shift label (join on product_id) to fill this heatmap."
    )

# =========================================================================
# YOUR CHALLENGE (15-20 min)
# -------------------------------------------------------------------------
# 1. OPERATOR VIEW: add a fifth tab that ranks operators by scrap rate at
#    molding (du.scrap_rate_by). Highlight the worst 3 with st.warning.
# 2. WORST BATCH CALLOUT: compute scrap rate per batch_id and show the single
#    worst batch as a st.error banner at the top of the page.
# 3. FILL THE HEATMAP: the other stations lack a `shift` column. Join them to
#    molding on product_id to borrow the shift, then extend the heatmap to all
#    six stations. (This reuses your Session 3 JOIN skills!)
# 4. Engineer's question: if FPY is 60% but each station's scrap rate is only
#    ~2-3%, why is FPY so much lower? (Hint: a wheel must pass EVERY station.)
# =========================================================================
