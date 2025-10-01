import h5py
import numpy as np
import pandas as pd
import streamlit as st

from .process_data import add_time_steps_to_df


@st.cache_data
def load_nodes_from_h5_results(path):
    """
    Loads all nodes contained in a results file as a list
    """
    with h5py.File(path) as hdf_file:
        nodes = extract_data_from_h5_dataset(hdf_file["topology/nodes"])

    return nodes


@st.cache_data
def load_carriers_from_h5_results(path):
    """
    Loads all carriers contained in a results file as a list
    """
    with h5py.File(path) as hdf_file:
        carriers = extract_data_from_h5_dataset(hdf_file["topology/carriers"])

    return carriers


@st.cache_data
def load_periods_from_h5_results(path):
    """
    Loads all carriers contained in a results file as a list
    """
    with h5py.File(path) as hdf_file:
        periods = extract_data_from_h5_dataset(hdf_file["topology/periods"])

    return periods


def extract_datasets_from_h5_group(group, prefix=()):
    """
    Gets all datasets from a group of an h5 file and writes it to a multi-index dataframe

    :param group: group of h5 file
    :return: dataframe containing all datasets in group
    """
    data = {}
    for key, value in group.items():
        if isinstance(value, h5py.Group):
            data.update(extract_datasets_from_h5_group(value, prefix + (key,)))
        elif isinstance(value, h5py.Dataset):
            if value.shape == ():
                data[prefix + (key,)] = [value[()]]
            else:
                data[prefix + (key,)] = value[:]

    return data


def extract_data_from_h5_dataset(dataset):
    """
    Gets dataset from an h5 file

    :param group: group of h5 file
    :return: dataframe containing all datasets in group
    """
    data = [item.decode("utf-8") for item in dataset]

    return data


def export_csv(df, label, filename):
    """
    Makes a button on the side bar that allows for csv export
    :param df: dataframe to export
    :param label: label of button
    :param filename: filename to export
    :return:
    """
    excel_buffer = df.to_csv(index=False, sep=";")
    st.sidebar.download_button(
        label=label,
        data=excel_buffer,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def read_results_from_h5(path_h5):
    """
    Reads the energybalance, technology operation, design and network operation, design into a dict
    """

    res = {}

    res["technology_operation"] = read_technology_operation(path_h5)
    res["technology_design"] = read_technology_design(path_h5)

    return res


def read_technology_operation(path_h5):
    """
    Reads technology operation
    """
    with h5py.File(path_h5, "r") as hdf_file:
        op = extract_datasets_from_h5_group(hdf_file["operation"])

    return pd.DataFrame(op)


def read_technology_design(path_h5):
    """
    Reads technology design
    """
    with h5py.File(path_h5, "r") as hdf_file:
        de = extract_datasets_from_h5_group(hdf_file["design"])

    technology_design = pd.DataFrame(de)
    technology_design = pd.melt(technology_design)
    technology_design.columns = ["Variable", "Value"]

    return technology_design
