from utilities import *

# Session States
manage_session_states()

# Page Setup
st.set_page_config(
    page_title="Home",
)

# Show cash status
show_sidebar()

st.write("Welcome to the visualization platform of the PyHub! 👋")
st.write("First load your data in 'Load data' and then select an option on the right.")
