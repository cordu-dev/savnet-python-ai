"""
Step 03 — First chart on the wall (Seaborn + Streamlit)
=======================================================

Business question:
    "Which station is bleeding the most scrap?"

New concepts:
    - Seaborn sits on top of Matplotlib and speaks DataFrame natively.
    - The Matplotlib pattern: create a `fig, ax`, draw onto `ax`.
    - st.pyplot(fig) : hand the FIGURE object to Streamlit to render it.

Why pass `fig` (not just call plt.show())?
    In a web app there is no pop-up window. Streamlit needs the figure OBJECT
    so it can turn it into an image on the page. Always build an explicit
    fig/ax and give the fig to st.pyplot.

Run it:
    streamlit run 03_seaborn_in_streamlit.py
"""

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import data_utils as du

st.set_page_config(page_title="Step 03 — First chart", page_icon="📈", layout="wide")

# A Seaborn theme applies nice defaults (grid, colours, fonts) in one line.
sns.set_theme(style="whitegrid")


@st.cache_data
def get_data():
    return du.load_all()


frames = get_data()

st.title("📈 Scrap rate by station")
st.caption("Each station has its own pass/fail column — the data layer unifies them.")

# --- Shape the data ------------------------------------------------------
# This helper loops over all stations and returns a tidy table with two
# columns: station + scrap_rate_pct, already sorted worst-first.
station_scrap = du.scrap_rate_by_station(frames)

# --- Build the chart -----------------------------------------------------
# fig  = the whole canvas.  ax = the single plot area we draw on.
# figsize is in inches (width, height).
fig, ax = plt.subplots(figsize=(8, 4))

# seaborn.barplot: x = category, y = value. We pass the DataFrame via `data=`
# and reference columns by NAME — much cleaner than raw Matplotlib.
sns.barplot(data=station_scrap, x="station", y="scrap_rate_pct", ax=ax, color="#c0392b")

# Label everything — an unlabelled chart is a bug, not a feature.
ax.set_title("Scrap rate per station (%)")
ax.set_xlabel("Station")
ax.set_ylabel("Scrap rate (%)")

# Render the figure in the browser.
st.pyplot(fig)

# Show the raw numbers underneath so students can verify the chart.
with st.expander("See the underlying numbers"):
    st.dataframe(station_scrap, use_container_width=True)

# =========================================================================
# YOUR CHALLENGE (10 min)
# -------------------------------------------------------------------------
# 1. Flip the chart to HORIZONTAL bars (hint: swap x and y in barplot). Which
#    orientation reads more easily when station names are long?
# 2. The table is already sorted worst-first. Add the sorted order to the chart
#    by passing `order=station_scrap["station"]` to sns.barplot.
# 3. Engineer's question: the QC station shows a high scrap rate. Is that BAD,
#    or is that QC doing its job (catching defects before we waste more material
#    downstream)? Write a one-line answer as a st.info() message.
# =========================================================================
