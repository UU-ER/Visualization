from utilities import *
import streamlit as st

# Session States
manage_session_states()

# Load Summary
st.markdown("**Summary File**")
load_summary_data_in_cash()

# Load Single Results
st.markdown("**Detailed Optimization Results**")
load_result_data_in_cash()

# Load Node Data
st.markdown("**Node Locations**")
load_node_data_in_cash()

# Show sidebar
show_sidebar()
