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

def load_data_in_cash():
    """
    Loads results into cash
    :return:
    """
    load_path1 = Path(st.text_input("Enter path to result 1 h5 file:", key="folder_key1"))
    if st.button('Load data for results 1'):
        st.session_state['Result1'] = read_results_from_h5(load_path1)

    # st.markdown("---")
    #
    # load_path2 = Path(st.text_input("Optional: Enter path to result 2 h5 file (this is only required if you want to compare two results):", key="folder_key2"))
    # if st.button('Load data for results 2'):
    #     read_technology_operation(load_path2)

    st.markdown("**Node Locations**")
    node_location_path = Path(st.text_input("Enter file path to location keys of nodes:", key="network"))
    # node_location_path = Path(r'C:\Users\6574114\OneDrive - Universiteit Utrecht\PhD Jan\Papers\DOSTA - HydrogenOffshore\Node_Locations.csv')
    if st.button("Load Node Locations"):
        st.session_state['NodeLocations'] = pd.read_csv(node_location_path, sep=';', index_col=0)

    st.markdown("If you wish to plot networks, enter the node locations as a csv here. You can download a sample CSV"
                " file by clicking on the button below.")



    with open("./utilities/Node_Locations.csv", "rb") as file:
        btn = st.download_button(
            label="Download sample csv file",
            data=file,
            file_name="Node_Locations.csv",
        )


