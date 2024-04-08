import streamlit as st
from pathlib import Path
import pandas as pd

from .read_data import read_results_from_h5

def show_sidebar():
    """
    Shows cash status and button in sidebar
    """
    clear_cash()
    show_cash_status()

def show_cash_status():
    """
    Displays that cash status
    :return:
    """
    if st.session_state['Result1']:
        st.sidebar.success("Results 1 successfully loaded")
    else:
        st.sidebar.error("Results 1 not loaded")

    # if st.session_state['Result2']:
    #     st.sidebar.success("Results 2 successfully loaded")
    # else:
    #     st.sidebar.error("Results 2 not loaded")

    if  isinstance(st.session_state['NodeLocations'], pd.DataFrame):
        st.sidebar.success("Node locations successfully loaded")
    else:
        st.sidebar.error("Node locations not loaded")

def clear_cash():
    """
    Clears cash
    :return:
    """
    if st.sidebar.button('Reset data'):
        st.session_state['Result1'] = {}
        # st.session_state['Result2'] = {}
        st.session_state['NodeLocations'] = None

def load_result_data_in_cash():
    """
    Loads results into cash
    :return:
    """
    uploaded_h5 = st.file_uploader("Load a result h5 file (case 1)")
    if uploaded_h5 is not None:
        st.session_state['Result1'] = read_results_from_h5(uploaded_h5)

    uploaded_h5 = st.file_uploader("Load a result h5 file (case 2)")
    if uploaded_h5 is not None:
        st.session_state['Result2'] = read_results_from_h5(uploaded_h5)

def load_node_data_in_cash():
    """
    Loads results into cash
    :return:
    """
    uploaded_csv = st.file_uploader("Load Node Locations")
    if uploaded_csv is not None:
        st.session_state['NodeLocations'] = pd.read_csv(uploaded_csv, sep=';', index_col=0)

    st.markdown("If you wish to plot networks, enter the node locations as a csv here. You can download a sample CSV"
                " file by clicking on the button below.")

    with open("./utilities/Node_Locations.csv", "rb") as file:
        btn = st.download_button(
            label="Download sample csv file",
            data=file,
            file_name="Node_Locations.csv",
        )


