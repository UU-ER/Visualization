import h5py
import pandas as pd
import streamlit as st

@st.cache_data
def aggregate_time(df, level, aggregation = 'sum'):
    if aggregation == 'sum':
        df = df.groupby(level=level).sum()
    elif aggregation == 'mean':
        df = df.groupby(level=level).mean()
    df.index.names = ['Timeslice']
    return df