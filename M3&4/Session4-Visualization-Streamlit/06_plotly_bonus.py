"""
Step 06 — Interactive charts with Plotly (OPTIONAL BONUS)
=========================================================

Seaborn charts are STATIC images — great for reports. Plotly charts are
INTERACTIVE — you can hover for exact values, zoom, pan, and toggle series.
That interactivity is powerful for exploring anomalies.

Business question:
    "Do out-of-spec molding temperatures line up with SCRAP outcomes?"

New concepts:
    - plotly.express : one-line interactive charts from a DataFrame.
    - st.plotly_chart(fig) : embed the interactive figure in Streamlit.
    - Hover tooltips + colour encoding to add a third dimension to a 2D chart.

This step is OPTIONAL — the core session goal is Seaborn + Streamlit. Treat
Plotly as a "nice to have" for interactive exploration.

Run it:
    streamlit run 06_plotly_bonus.py
"""

import plotly.express as px
import streamlit as st

import data_utils as du

st.set_page_config(page_title="Step 06 — Plotly (bonus)", page_icon="✨", layout="wide")


@st.cache_data
def get_data():
    return du.load_all()


frames = get_data()
molding = frames["molding"]

st.title("✨ Interactive molding scatter (Plotly bonus)")
st.caption("Hover any point for details · drag to zoom · double-click to reset")

# We plot a sample so the browser stays snappy (10k points can lag).
# `.sample` picks random rows; random_state makes it reproducible.
sample = molding.sample(min(2000, len(molding)), random_state=42)

# plotly.express.scatter builds the whole interactive figure in one call.
#   x, y      : the two axes
#   color     : a THIRD variable encoded as colour (here the pass/fail result)
#   hover_data: extra fields shown in the tooltip on hover
fig = px.scatter(
    sample,
    x="temperature_c",
    y="pressure_bar",
    color="cycle_result",
    hover_data=["product_id", "product_type", "operator_id", "shift"],
    title="Molding temperature vs pressure, coloured by outcome",
    labels={"temperature_c": "Temperature (°C)", "pressure_bar": "Pressure (bar)"},
)

# Draw the SIC spec window (180-220 °C) as reference lines so out-of-spec
# points are obvious to the eye.
fig.add_vline(x=180, line_dash="dash", line_color="gray")
fig.add_vline(x=220, line_dash="dash", line_color="gray")

# use_container_width makes the chart fill the page width responsively.
st.plotly_chart(fig, use_container_width=True)

st.info(
    "Notice how SCRAP points cluster OUTSIDE the dashed 180-220 °C window. "
    "That visual pattern is exactly what an anomaly-detection agent will learn "
    "to flag automatically in later sessions."
)

# =========================================================================
# YOUR CHALLENGE (optional, 10 min)
# -------------------------------------------------------------------------
# 1. Change `color` to "product_type". Does PT77 (runs hotter, target 205 °C)
#    sit further right than PT55/PT66? Confirm it with hover tooltips.
# 2. Make an interactive LINE chart of daily throughput using px.line on
#    du.daily_throughput(molding). Zoom into one week.
# 3. Reflect: when would you prefer a STATIC Seaborn chart over an interactive
#    Plotly one? (Think: printed reports vs live exploration.)
# =========================================================================
