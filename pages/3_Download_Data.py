import streamlit as st
from pathlib import Path

from utilities import *

# Page Setup
st.set_page_config(
    page_title="Visualize Single Result",
)

# Show cash status
st.sidebar.markdown('Cash Status')
show_sidebar()
st.sidebar.markdown("---")

def export_csv(df, label, filename):
    """
    Makes a button that allows for csv export
    :param df: dataframe to export
    :param label: label of button
    :param filename: filename to export
    :return:
    """
    excel_buffer = df.to_csv(index=False)
    st.download_button(
        label=label,
        data=excel_buffer,
        file_name=filename,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

st.markdown("This page allows to download data as csv files. Note that always data from the first result is used.")

st.header("Technologies")
st.subheader("Technology Design")
export_csv(st.session_state['Result1']['technology_design'], 'Download Technology Design as CSV', 'technology_design.csv')

st.subheader("Technology Operation")
tec_operation = st.session_state['Result1']['technology_operation']
nodes = list(tec_operation.columns.get_level_values('Node').unique())
nodes.insert(0, 'All')
selected_node = st.selectbox('Node Selection', nodes)

if selected_node != 'All':
    tec_operation = tec_operation.loc[:, (selected_node, slice(None), slice(None))]
technologies = list(tec_operation.columns.get_level_values('Technology').unique())
technologies.insert(0, 'All')
selected_technology = st.selectbox('Technology Selection', technologies)

if selected_technology != 'All':
    tec_operation = tec_operation.loc[:, (slice(None), selected_technology, slice(None))]
export_csv(tec_operation, 'Download Technology Operation as CSV', 'technology_operation.csv')

st.header("Networks")
st.subheader("Network Design")
export_csv(st.session_state['Result1']['network_design'], 'Download Network Design as CSV', 'technology_design.csv')
st.subheader("Network Operation")
net_operation = st.session_state['Result1']['network_operation']
networks = list(net_operation.columns.get_level_values('Network').unique())
networks.insert(0, 'All')
selected_network = st.selectbox('Network Selection', networks)
if selected_network != 'All':
    net_operation = net_operation.loc[:, (selected_network)]
export_csv(net_operation, 'Download Network Operation as CSV', 'network_operation.csv')

st.header("Energybalance")
e_balance = st.session_state['Result1']['energybalance']
carriers = list(e_balance.columns.get_level_values('Carrier').unique())
carriers.insert(0, 'All')
selected_carrier = st.selectbox('Carrier Selection', carriers)
if selected_carrier != 'All':
    e_balance = e_balance.loc[:, (slice(None), selected_carrier, slice(None), slice(None))]

nodes = list(e_balance.columns.get_level_values('Node').unique())
nodes.insert(0, 'All')
selected_node = st.selectbox('Node Selection ', nodes)
if selected_node != 'All':
    e_balance = e_balance.loc[:, (selected_node, slice(None), slice(None), slice(None))]
export_csv(e_balance, 'Download Energybalance as CSV', 'energy_balance.csv')


