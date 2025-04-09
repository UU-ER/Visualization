from utilities import *

# Session States
st.logo("./utilities/Adopt_nosubtext.svg", size="large", link=None, icon_image=None)
manage_session_states()

# Page Setup
st.set_page_config(
    page_title="Home",
)

# Show cash status
show_sidebar()

st.markdown("**Visualization Website**")
st.write("Welcome to the visualization platform of the AdOpT-NET0! 👋")
st.write("First load your data in 'Load data' and then select an option on the right.")
