import streamlit as st
from pathlib import Path

from utilities import *

# Page Setup
st.set_page_config(
    page_title="Visualize Single Result",
)

# Show cash status
st.sidebar.markdown('**Cash Status**')
show_sidebar()
st.sidebar.markdown("---")

# Page to show
st.sidebar.markdown('**Graph**')
pages_available = ["Technology Design", "Network Design",
                   "Energy Balance at Node",
                   "Technology Operation", "Network Operation"]
selected_page = st.sidebar.selectbox("Select graph", pages_available)

# Individual pages
if selected_page == "Technology Design":
    plot_technology_design()
elif selected_page == "Network Design":
    plot_network_design()
elif selected_page == "Energy Balance at Node":
    plot_energy_balance()
elif selected_page == "Technology Operation":
    plot_technology_operation()
elif selected_page == "Network Operation":
    plot_network_operation()





