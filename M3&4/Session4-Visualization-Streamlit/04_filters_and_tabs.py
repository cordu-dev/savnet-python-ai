"""
Step 04 — Let the user explore (filters + tabs)
===============================================

Business question:
    "How does scrap differ by shift and by product type?"

New concepts:
    - st.sidebar : a side panel for controls, so filters don't clutter charts.
    - st.multiselect / st.selectbox : widgets that RETURN the user's choice.
    - Filtering a DataFrame from widget values.
    - st.tabs and st.expander : organise output without a wall of scrolling.

The key idea: a widget is just a function that returns a value. Because the
script reruns top-to-bottom, that value is always up to date. No callbacks.

Run it:
    streamlit run 04_filters_and_tabs.py
"""

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import data_utils as du

st.set_page_config(page_title="Step 04 — Filters", page_icon="🎛️", layout="wide")
sns.set_theme(style="whitegrid")


@st.cache_data
def get_data():
    return du.load_all()


frames = get_data()
molding = frames["molding"]

st.title("🎛️ Explore scrap by shift and product type")

# --- Sidebar filters -----------------------------------------------------
# Everything inside `st.sidebar` renders in the left panel.
st.sidebar.header("Filters")

# The options come from the data itself, so they always match reality.
product_options = sorted(molding["product_type"].unique())
shift_options = sorted(molding["shift"].unique())

# multiselect returns a LIST of the chosen values. `default` pre-selects all.
chosen_types = st.sidebar.multiselect(
    "Product type", options=product_options, default=product_options
)
chosen_shifts = st.sidebar.multiselect(
    "Shift", options=shift_options, default=shift_options
)

# --- Apply the filters ---------------------------------------------------
# Our shared helper keeps only rows matching the chosen values.
filtered = du.apply_filters(molding, chosen_types, chosen_shifts)

# Always tell the user how much data they are looking at.
st.caption(f"Showing **{len(filtered):,}** molding records after filtering.")

# --- Organise output with tabs ------------------------------------------
# st.tabs returns one object per tab label. Write into each with `with`.
tab_shift, tab_type = st.tabs(["By shift", "By product type"])

with tab_shift:
    st.subheader("Scrap rate by shift")
    by_shift = du.scrap_rate_by(filtered, "shift", "cycle_result")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=by_shift, x="shift", y="scrap_rate_pct", ax=ax, color="#2980b9")
    ax.set_ylabel("Scrap rate (%)")
    ax.set_xlabel("Shift")
    st.pyplot(fig)

with tab_type:
    st.subheader("Scrap rate by product type")
    by_type = du.scrap_rate_by(filtered, "product_type", "cycle_result")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=by_type, x="product_type", y="scrap_rate_pct", ax=ax, color="#8e44ad")
    ax.set_ylabel("Scrap rate (%)")
    ax.set_xlabel("Product type")
    st.pyplot(fig)

# An expander hides detail until the user wants it — keeps the page tidy.
with st.expander("Show the filtered raw data (first 100 rows)"):
    st.dataframe(filtered.head(100), use_container_width=True)

# =========================================================================
# YOUR CHALLENGE (10 min)
# -------------------------------------------------------------------------
# 1. Add a THIRD tab "By operator" using du.scrap_rate_by(filtered,
#    "operator_id", "cycle_result"). Sort it worst-first and rotate the x
#    labels (ax.tick_params(axis="x", rotation=90)) so they don't overlap.
# 2. Add a st.sidebar.selectbox to pick ONE mold_tool_id and filter by it too.
#    Does any single tool stand out as a scrap driver?
# 3. Engineer's question: if the "Night" shift scraps more, list two possible
#    causes you would investigate (people? machines? materials?).
# =========================================================================
