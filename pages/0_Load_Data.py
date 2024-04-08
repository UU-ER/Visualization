from utilities import *
import streamlit as st

# Load Results
st.markdown("**Load Data**")
st.markdown("On this page, you can load one or two h5 files to visualize. After sucessfully loading the data, "
          "you can select 'Visualize Single Result' or 'Compare Results' on the sidebar.")
load_result_data_in_cash()

# Load Node Data
st.markdown("**Node Locations**")
load_node_data_in_cash()

show_sidebar()



