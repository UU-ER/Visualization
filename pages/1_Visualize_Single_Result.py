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
        "Network Design",
        "Energy Balance at Node",
        "Technology Operation",
        "Network Operation",
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
    elif selected_page == "Network Design":
        if isinstance(st.session_state["NodeLocations"], pd.DataFrame):
            plot_network_design()
        else:
            st.markdown(
                "Node Locations not loaded. Please upload them first in 'Load Data'."
            )
    elif selected_page == "Energy Balance at Node":
        plot_energy_balance()
    elif selected_page == "Technology Operation":
        plot_technology_operation()
    elif selected_page == "Network Operation":
        if isinstance(st.session_state["NodeLocations"], pd.DataFrame):
            plot_network_operation()
        else:
            st.markdown(
                "Node Locations not loaded. Please upload them first in 'Load Data'."
            )

else:
    st.markdown("Please load in data first")
