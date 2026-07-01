"""
Step 01 — Hello, Streamlit
==========================

Business question: none yet — first we learn the tool.
    "A dashboard is just a Python script that draws itself in the browser."

Run it:
    streamlit run 01_hello_streamlit.py

Then edit this file and SAVE — Streamlit notices and offers to rerun. That is
the whole magic: you write plain Python, Streamlit turns it into a web page.

Mental model you MUST remember:
    Streamlit runs your script FROM TOP TO BOTTOM every time something changes
    (a button click, a slider move, a file save). There is no callback soup —
    it is just your script, re-executed. Simple and predictable.
"""

import streamlit as st

# st.set_page_config MUST be the first Streamlit command. It sets the browser
# tab title and how wide the page is ("wide" uses the full screen).
st.set_page_config(page_title="Step 01 — Hello", page_icon="👋", layout="centered")

# --- Text elements -------------------------------------------------------
# st.title  -> the biggest heading. Use once per page.
st.title("👋 Hello, Steering Wheel Factory")

# st.header / st.subheader -> smaller section headings.
st.header("My first Streamlit page")

# st.write is the "Swiss army knife": it prints text, numbers, DataFrames,
# charts... it figures out the type for you. Great for quick experiments.
st.write("This whole page is a Python script. No HTML, no CSS, no JavaScript.")

# Markdown works too — bold, bullet lists, links, emojis.
st.markdown(
    """
    **What we will build this session:**
    - A live KPI dashboard for our steering wheel factory
    - Charts with Seaborn, filters with Streamlit widgets
    - One interactive Plotly chart at the end
    """
)

# --- Your first metric ---------------------------------------------------
# st.metric shows a single big number with a label — perfect for KPIs.
# We will fill these with REAL numbers in the next step; for now, hard-coded.
st.metric(label="Units produced today", value="455")

st.divider()  # a horizontal rule to separate sections

# =========================================================================
# YOUR CHALLENGE (5 min)
# -------------------------------------------------------------------------
# 1. Add a st.subheader with your name, e.g. "Built by <you>".
# 2. Add a SECOND st.metric next to the idea of scrap — value "1.9%".
# 3. Bonus: give st.metric a `delta="-0.3%"` argument and watch what colour
#    Streamlit paints it. What does a green vs red delta imply for scrap?
# =========================================================================
