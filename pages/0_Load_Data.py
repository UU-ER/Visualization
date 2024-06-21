from utilities import *
import streamlit as st

# Session States
manage_session_states()

# Load Single Results
st.markdown("**Detailed Optimization Results (.H5)**")
load_result_data_in_cash()

# Load Summary
st.markdown("**Summary File (.XLSX)**")
load_summary_data_in_cash()

# Load Node Data
st.markdown("**Node Locations**")
load_node_data_in_cash()

# Show sidebar
show_sidebar()
