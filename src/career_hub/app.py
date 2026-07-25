"""Career Hub — Streamlit entry point.

Run from the repo root:
    uv run streamlit run src/career_hub/app.py
"""

import streamlit as st

st.set_page_config(page_title="Career Hub", layout="centered")

st.title("Career Hub")
st.write(
    "Setup works. Pages for Today, Opportunities, Experience, People, "
    "and Settings arrive in the next increments."
)
