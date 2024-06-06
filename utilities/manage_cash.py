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


def manage_session_states():
    """
    Initilize all required session states
    """
    if "Summary" not in st.session_state:
        st.session_state["Summary"] = None
    if "Result1" not in st.session_state:
        st.session_state["Result1"] = {}
    if "NodeLocations" not in st.session_state:
        st.session_state["NodeLocations"] = None


def show_cash_status():
    """
    Displays that cash status
    :return:
    """

    if isinstance(st.session_state["Summary"], pd.DataFrame):
        st.sidebar.success("Summary file successfully loaded")
    else:
        st.sidebar.error("Summary file not loaded")

    if st.session_state["Result1"]:
        st.sidebar.success("Results 1 successfully loaded")
    else:
        st.sidebar.error("Results 1 not loaded")

    if isinstance(st.session_state["NodeLocations"], pd.DataFrame):
        st.sidebar.success("Node locations successfully loaded")
    else:
        st.sidebar.error("Node locations not loaded")


def clear_cash():
    """
    Clears cash
    :return:
    """
    if st.sidebar.button("Reset data"):
        st.session_state["Result1"] = {}
        st.session_state["NodeLocations"] = None
        st.session_state["Summary"] = None


def load_summary_data_in_cash():
    """
    Loads summary file in cash
    :return:
    """
    st.markdown(
        "In this section, you can load a summary csv file for visualization. "
        "After sucessfully loading the data, you can select 'Visualize "
        "Summary' on the sidebar."
    )
    uploaded_summary = st.file_uploader("Load a summary xlsx")
    if uploaded_summary is not None:
        st.session_state["Summary"] = pd.read_excel(uploaded_summary)


def load_result_data_in_cash():
    """
    Loads results into cash
    :return:
    """
    st.markdown(
        "In this section, you can load a h5 files to visualize. After "
        "sucessfully loading the data, "
        "you can select 'Visualize Single Result'"
    )

    uploaded_h5 = st.file_uploader("Load a result h5 file (case 1)")
    if uploaded_h5 is not None:
        st.session_state["Result1"] = read_results_from_h5(uploaded_h5)


def load_node_data_in_cash():
    """
    Loads results into cash
    :return:
    """
    uploaded_csv = st.file_uploader("Load Node Locations")
    if uploaded_csv is not None:
        st.session_state["NodeLocations"] = pd.read_csv(
            uploaded_csv, sep=";", index_col=0
        )

    st.markdown(
        "If you wish to plot networks, enter the node locations as a csv here. You can download a sample CSV"
        " file by clicking on the button below."
    )

    with open("./utilities/Node_Locations.csv", "rb") as file:
        btn = st.download_button(
            label="Download sample csv file",
            data=file,
            file_name="Node_Locations.csv",
        )
