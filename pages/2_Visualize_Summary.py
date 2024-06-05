import streamlit as st

from utilities import *

# Session States
manage_session_states()

# Page Setup
st.set_page_config(
    page_title="Visualize Summary",
)

# Show cash status
st.sidebar.markdown('**Cash Status**')
show_sidebar()
st.sidebar.markdown("---")

if st.session_state['Summary'] is not None:
    # Page to show
    data = st.session_state['Summary']
    plot_summary(data)
else:
    st.markdown("Please load in data first")





