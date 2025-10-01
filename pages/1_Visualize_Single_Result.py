import streamlit as st
from pathlib import Path

from utilities import *

# Session States
manage_session_states()

# Page Setup
st.set_page_config(
    page_title="Visualize Single Result",
)

if st.session_state["Result1"]:

    # Page to show
    st.sidebar.markdown("**Select a graph**")
    pages_available = [
        "Technology Design",
        "Technology Operation",
    ]
    selected_page = st.sidebar.selectbox("", pages_available)

# Show cash status
st.sidebar.markdown("**Cash Status**")
show_sidebar()
st.sidebar.markdown("---")

if st.session_state["Result1"]:
    # Individual pages
    if selected_page == "Technology Design":
        plot_technology_design()
    elif selected_page == "Technology Operation":
        plot_technology_operation()

else:
    st.markdown("Please load in data first")
