from utilities import *
import streamlit as st

# Session States
manage_session_states()

# Load Single Results
st.markdown("**Optimization Results (.H5)**")
load_result_data_in_cash()

# Show sidebar
show_sidebar()
