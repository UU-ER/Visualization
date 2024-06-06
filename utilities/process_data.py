import h5py
import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def aggregate_time(df, level, aggregation="sum"):
    if aggregation == "sum":
        df = df.groupby(level=level).sum()
    elif aggregation == "mean":
        df = df.groupby(level=level).mean()
    df.index.names = ["Timeslice"]
    return df


def add_time_steps_to_df(df):
    """
    Adds time index to a df
    """
    num_rows = len(df)
    hour = np.repeat(np.arange(1, num_rows + 1), 1)[0:num_rows]
    day = np.repeat(np.arange(1, num_rows + 1), 24)[0:num_rows]
    week = np.repeat(np.arange(1, num_rows + 1), 24 * 7)[0:num_rows]
    month = (
        pd.date_range(start="2008-01-01 00:00", end="2008-12-31 00:00", freq="1h")
        .month[0:num_rows]
        .to_list()
    )
    year = np.ones(num_rows)

    df.index = pd.MultiIndex.from_arrays(
        [hour, day, week, month, year], names=["Hour", "Day", "Week", "Month", "Year"]
    )

    return df
