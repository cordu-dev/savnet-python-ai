"""
Step 02 — Load the data and show KPIs
=====================================

Business question:
    "How many wheels did we make, and what share ended up as scrap or rework?"

New concepts:
    - Importing our shared data layer (data_utils) so this script stays short.
    - @st.cache_data : load the Parquet files ONCE, not on every rerun.
    - st.columns : place several KPIs side by side.
    - st.metric with a delta.

Run it:
    streamlit run 02_load_and_kpis.py
"""

import streamlit as st

import data_utils as du

st.set_page_config(page_title="Step 02 — KPIs", page_icon="📊", layout="wide")


# --- Caching -------------------------------------------------------------
# Remember: Streamlit reruns the WHOLE script on every interaction. Reading
# Parquet files each time would be slow. @st.cache_data tells Streamlit:
# "run this function once, remember the result, and reuse it next time."
@st.cache_data
def get_data():
    """Load every station table (cached)."""
    return du.load_all()


frames = get_data()

st.title("📊 Production KPIs")
st.caption("Quality snapshot across all six stations")

# --- Compute the numbers -------------------------------------------------
# Total units = number of wheels that entered molding (every wheel starts here).
molding = frames["molding"]
total_units = len(molding)

# Scrap / rework rate at the molding station. Recall the boolean-mean trick:
# the mean of a True/False column is the proportion of True values.
scrap_rate = (molding["cycle_result"] == "SCRAP").mean() * 100
rework_rate = (molding["cycle_result"] == "REWORK").mean() * 100

# --- Display in a row of columns ----------------------------------------
# st.columns(3) returns three column objects. Writing into a column with the
# `with` keyword places the widget inside that column — instant layout.
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total units (molding)", f"{total_units:,}")

with col2:
    # delta_color="inverse" -> for scrap, going DOWN is good (shown green).
    st.metric("Scrap rate", f"{scrap_rate:.2f}%", delta=None, delta_color="inverse")

with col3:
    st.metric("Rework rate", f"{rework_rate:.2f}%", delta_color="inverse")

st.divider()

# --- A per-product-type breakdown ---------------------------------------
# groupby + value_counts gives us counts per product type. We show it as a
# plain table for now; charts come in the next step.
st.subheader("Units by product type")
by_type = molding["product_type"].value_counts().rename_axis("product_type")
st.dataframe(by_type.reset_index(name="units"), use_container_width=True)

# =========================================================================
# YOUR CHALLENGE (10 min)
# -------------------------------------------------------------------------
# 1. Add a FOURTH column showing First Pass Yield using the helper:
#        du.first_pass_yield(frames)
#    Display it as a percentage metric. Is it higher or lower than you expected?
# 2. Add a per-product-type SCRAP RATE table (hint: du.scrap_rate_by(molding,
#    "product_type", "cycle_result")). Which product type scraps most at molding?
# 3. Think like an engineer: total_units counts molding rows. Is that the same
#    as "finished wheels"? Why or why not? (Peek at the tapitat table.)
# =========================================================================
