import streamlit as st
import altair as alt
import pandas as pd
import folium
from folium.features import DivIcon
from branca.colormap import linear
from folium.plugins import PolyLineTextPath, PolyLineOffset
from streamlit_folium import st_folium

from .process_data import aggregate_time


def plot_chart(df):
    """
    Plots an altair area chart
    """
    df = df.reset_index()
    df = pd.melt(df, value_vars=df.columns, id_vars=["Timeslice"])

    if len(df["Timeslice"].unique()) == 1:
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(x="Timeslice:Q", y="sum(value):Q", color="Variable:N")
            .configure_legend(orient="bottom")
            .interactive()
        )
    else:
        chart = (
            alt.Chart(df)
            .mark_area()
            .encode(x="Timeslice:Q", y="sum(value):Q", color="Variable:N")
            .configure_legend(orient="bottom")
            .interactive()
        )

    return chart


def plot_summary(data):
    # Select graph
    all_graphs = ["Line Chart", "Scatter Plot"]
    selected_chart = st.selectbox("**Select a Chart**", all_graphs)

    # Select Var
    all_vars = data.columns
    selected_x = st.selectbox("**Select x value**", all_vars)
    selected_y = st.multiselect("**Select y values**", all_vars)

    plot_data = data.reset_index().melt(id_vars=["index", selected_x])
    plot_data = plot_data[plot_data["variable"].isin(selected_y)]

    if selected_chart == "Line Chart":
        chart = (
            alt.Chart(plot_data)
            .mark_line()
            .encode(
                x=alt.X(selected_x),
                y=alt.Y("value"),
                color=alt.Color("variable", legend=alt.Legend()),
            )
            .properties(width=800, height=400)
            .interactive()
        )
        st.altair_chart(chart)

    elif selected_chart == "Scatter Plot":
        chart = (
            alt.Chart(plot_data)
            .mark_point()
            .encode(
                x=alt.X(selected_x),
                y=alt.Y("value"),
                color=alt.Color("variable", legend=alt.Legend()),
            )
            .properties(width=800, height=400)
            .interactive()
        )
        st.altair_chart(chart)


def plot_nodes(map, node_data):
    for node_name, data in node_data.iterrows():
        folium.CircleMarker(
            location=[data["lat"], data["lon"]],
            radius=5,  # Adjust the radius as needed
            color="black",  # Marker color
            fill=True,
            fill_color="black",  # Fill color
            fill_opacity=0.7,
        ).add_to(map)
        folium.map.Marker(
            [data["lat"], data["lon"]],
            icon=DivIcon(
                icon_size=(150, 36),
                icon_anchor=(-5, 20),
                html='<div style="font-size: 9pt">' + node_name + "</div>",
            ),
        ).add_to(map)


def plot_technology_design():
    """
    Plots the technology design
    """
    data = st.session_state["Result1"]["technology_design"]
    data = data[data["Variable"] != "technology"]

    all_periods = data["Period"].unique()
    selected_period = st.selectbox("**Period Selection**", all_periods)

    all_vars = data["Variable"].unique()
    selected_var = st.selectbox("**Variable Selection**", all_vars)

    technologies = data["Technology"].unique()
    selected_technologies = st.multiselect(
        "**Technology Selection**", technologies, default=technologies
    )

    submitted = st.button("Plot")

    if submitted:
        data = data[data["Period"] == selected_period]
        data = data[data["Variable"] == selected_var]
        data = data[data["Technology"].isin(selected_technologies)]

        st.header(selected_var)

        chart = (
            alt.Chart(data)
            .mark_bar()
            .encode(
                y="Node:N", x=alt.X("Value:Q", title=selected_var), color="Technology:N"
            )
            .interactive()
        )
        st.altair_chart(chart, use_container_width=True)


def plot_energy_balance():
    """
    Plots the energy balance
    """
    all_periods = st.session_state["Result1"]["topology"]["periods"]
    selected_period = st.selectbox("**Period Selection**", all_periods)

    carriers = st.session_state["Result1"]["topology"]["carriers"]
    selected_carrier = st.selectbox("**Carrier Selection**", carriers)

    nodes = st.session_state["Result1"]["topology"]["nodes"]
    selected_node = st.selectbox("**Node Selection**", nodes)

    time_agg_options = {
        "Annual Totals": "Year",
        "Monthly Totals": "Month",
        "Weekly Totals": "Week",
        "Daily Totals": "Day",
        "Hourly Totals": "Hour",
    }
    time_agg = st.selectbox("**Time Aggregation**", time_agg_options.keys())

    data = st.session_state["Result1"]["energybalance"]

    data = data.loc[
        :, (selected_period, selected_node, selected_carrier, slice(None), slice(None))
    ]
    aggregated_data = aggregate_time(data, time_agg_options[time_agg])

    st.header("Supply")
    series_supply = [
        "generic_production",
        "technology_outputs",
        "network_inflow",
        "import",
    ]
    selected_supply_series = st.multiselect(
        "Select Series to Filter", series_supply, default=series_supply
    )

    plot_data = aggregated_data.loc[
        :,
        aggregated_data.columns.get_level_values("Variable").isin(
            selected_supply_series
        ),
    ]
    plot_data.columns = plot_data.columns.get_level_values("Variable")
    chart = plot_chart(plot_data)
    st.altair_chart(chart, theme="streamlit", use_container_width=True)

    st.header("Demand")
    # Multi-select box for filtering series
    series_demand = ["demand", "technology_inputs", "network_outflow", "export"]
    selected_demand_series = st.multiselect(
        "Select Series to Filter", series_demand, default=series_demand
    )
    plot_data = aggregated_data.loc[
        :,
        aggregated_data.columns.get_level_values("Variable").isin(
            selected_demand_series
        ),
    ]
    plot_data.columns = plot_data.columns.get_level_values("Variable")
    chart = plot_chart(plot_data)
    st.altair_chart(chart, theme="streamlit", use_container_width=True)


def plot_technology_operation():
    """
    Plots technology operation
    """
    all_periods = st.session_state["Result1"]["topology"]["periods"]
    selected_period = st.selectbox("**Period Selection**", all_periods)

    nodes = st.session_state["Result1"]["topology"]["nodes"]
    selected_node = st.selectbox("**Node Selection**", nodes)

    data = st.session_state["Result1"]["technology_operation"]

    data = data.loc[:, (selected_period, selected_node, slice(None), slice(None))]

    technologies = data.columns.get_level_values("Technology").unique()
    selected_technology = st.selectbox("**Technology Selection**", technologies)

    time_agg_options = {
        "Annual Totals": "Year",
        "Monthly Totals": "Month",
        "Weekly Totals": "Week",
        "Daily Totals": "Day",
        "Hourly Totals": "Hour",
    }
    time_agg = st.selectbox("**Time Aggregation**", time_agg_options.keys())

    data = data.loc[:, (selected_period, slice(None), selected_technology, slice(None))]
    aggregated_data_sum = aggregate_time(data, time_agg_options[time_agg])
    aggregated_data_mean = aggregate_time(
        data, time_agg_options[time_agg], aggregation="mean"
    )

    st.header("Input")
    variables_in = [
        col
        for col in aggregated_data_sum.columns.get_level_values("Variable")
        if col.endswith("input")
    ]
    plot_data = aggregated_data_sum.loc[
        :, (selected_period, slice(None), slice(None), variables_in)
    ]
    plot_data.columns = plot_data.columns.get_level_values("Variable")
    if not plot_data.empty:
        chart = plot_chart(plot_data)
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    else:
        st.markdown("Nothing to show")

    # Output
    st.header("Output")
    variables_out = [
        col
        for col in aggregated_data_sum.columns.get_level_values("Variable")
        if col.endswith("output")
    ]
    plot_data = aggregated_data_sum.loc[
        :, (selected_period, slice(None), slice(None), variables_out)
    ]
    plot_data.columns = plot_data.columns.get_level_values("Variable")
    if not plot_data.empty:
        chart = plot_chart(plot_data)
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    else:
        st.markdown("Nothing to show")

    st.header("Other Variables")
    variables_other = [
        x
        for x in aggregated_data_sum.columns.get_level_values("Variable")
        if ((x not in variables_in) & (x not in variables_out))
    ]
    selected_series = st.multiselect(
        "Select Series to Filter", variables_other, default=variables_other
    )
    plot_data = aggregated_data_sum.loc[
        :, (selected_period, slice(None), slice(None), selected_series)
    ]
    plot_data.columns = plot_data.columns.get_level_values("Variable")
    plot_data_mean = aggregated_data_mean.loc[
        :, (selected_period, slice(None), slice(None), selected_series)
    ]
    plot_data_mean.columns = plot_data_mean.columns.get_level_values("Variable")

    mask_sum = plot_data.columns.str.contains("level")
    mask_mean = plot_data_mean.columns.str.contains("level")
    plot_data.loc[:, mask_sum] = plot_data_mean.loc[:, mask_mean]

    if not plot_data.empty:
        chart = plot_chart(plot_data)
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    else:
        st.markdown("Nothing to show")


def plot_network_design():

    all_periods = st.session_state["Result1"]["topology"]["periods"]
    selected_period = st.selectbox("**Period Selection**", all_periods)
    data = st.session_state["Result1"]["network_design"]

    st.text(data)

    networks_available = list(data["Network"].unique())
    selected_netw = st.multiselect("Select a network:", networks_available)

    variables_available = list(data.columns)
    variables_available.remove("Arc_ID")
    variables_available.remove("Network")
    variables_available.remove("FromNode")
    variables_available.remove("ToNode")
    variables_available.remove("Period")

    selected_variable = st.selectbox("Select a variable:", variables_available)

    # Init map
    node_data = st.session_state["NodeLocations"]
    map_center = [node_data["lat"].mean(), node_data["lon"].mean()]
    map = folium.Map(location=map_center, zoom_start=5)

    # Plot nodes
    plot_nodes(map, node_data)

    data = data[data["Network"].isin(selected_netw)]
    data = data[data["Period"].isin([selected_period])]
    if not data.empty:

        arc_ids = data[["Arc_ID", "FromNode", "ToNode"]]
        data = data.groupby("Arc_ID").sum()
        data.drop(columns=["FromNode", "ToNode", "Network"], inplace=True)
        data = data.merge(arc_ids, on="Arc_ID")

        # Plot edges
        if selected_variable in ["size", "capex", "total_flow"]:
            # Determine color scale:
            max_value = max(data[selected_variable])
            if max_value > 0:
                color_scale = linear.OrRd_09.scale(0, 1)

                for _, edge_data in data.iterrows():
                    from_node_data = node_data.loc[edge_data.FromNode]
                    to_node_data = node_data.loc[edge_data.ToNode]

                    # Normalize edge value to be within [0, 1]
                    normalized_value = (edge_data[selected_variable]) / max_value

                    # Determine color based on the color scale
                    color = color_scale(normalized_value)
                    if normalized_value > 0.001:
                        line = folium.plugins.PolyLineOffset(
                            [
                                (from_node_data["lat"], from_node_data["lon"]),
                                (to_node_data["lat"], to_node_data["lon"]),
                            ],
                            color=color,
                            weight=3.5,  # Set a default weight
                            opacity=1,
                            offset=3,
                            tooltip=edge_data[selected_variable],
                        ).add_to(map)
                        attr = {"font-weight": "bold", "font-size": "13"}

                        folium.plugins.PolyLineTextPath(
                            line, "      >", repeat=True, offset=5, attributes=attr
                        ).add_to(map)

    st_folium(map, width=725)


def plot_network_operation():

    data = st.session_state["Result1"]["network_operation"]
    all_periods = st.session_state["Result1"]["topology"]["periods"]
    selected_period = st.selectbox("**Period Selection**", all_periods)
    networks = data.columns.get_level_values(1).unique()
    selected_network = st.multiselect("**Network Selection**", networks)

    time_agg_options = {
        "Annual Totals": "Year",
        "Monthly Totals": "Month",
        "Weekly Totals": "Week",
        "Daily Totals": "Day",
        "Hourly Totals": "Hour",
    }

    time_agg = st.selectbox("**Time Aggregation**", time_agg_options.keys())
    data = data.loc[
        :,
        (
            selected_period,
            selected_network,
            slice(None),
            "flow",
            slice(None),
            slice(None),
        ),
    ]
    aggregated_data = aggregate_time(data, time_agg_options[time_agg])

    if time_agg != "Annual Totals":
        selected_timeslice = st.slider(
            "Select a time slice: ",
            min_value=min(aggregated_data.index),
            max_value=max(aggregated_data.index),
        )
        aggregated_data = aggregated_data[aggregated_data.index == selected_timeslice]

    data = aggregated_data.T

    data.columns = ["Flow"]
    data = data.reset_index()

    arc_ids = data[["Arc_ID", "FromNode", "ToNode"]]
    data = data.groupby("Arc_ID").sum()
    data.drop(columns=["FromNode", "ToNode", "Network"], inplace=True)
    data = data.merge(arc_ids, on="Arc_ID")

    # Init map
    node_data = st.session_state["NodeLocations"]
    map_center = [node_data["lat"].mean(), node_data["lon"].mean()]
    map = folium.Map(location=map_center, zoom_start=5)

    # Plot nodes
    plot_nodes(map, node_data)

    # Plot edges
    if not data.empty:

        max_value = max(data["Flow"])
        color_scale = linear.OrRd_09.scale(0, 1)

        for _, edge_data in data.iterrows():
            from_node_data = node_data.loc[edge_data.FromNode]
            to_node_data = node_data.loc[edge_data.ToNode]

            # Normalize edge value to be within [0, 1]
            flow_this_direction = edge_data["Flow"]

            flow_other_direction = data[
                (data["FromNode"] == to_node_data.name)
                & (data["ToNode"] == from_node_data.name)
            ]

            uni_flow = (
                flow_this_direction - flow_other_direction.loc[:, "Flow"].values[0]
            )

            if uni_flow > 0.1:
                normalized_value = uni_flow / max_value

                # # Determine color based on the color scale
                color = color_scale(normalized_value)
                line = folium.plugins.PolyLineOffset(
                    [
                        (from_node_data["lat"], from_node_data["lon"]),
                        (to_node_data["lat"], to_node_data["lon"]),
                    ],
                    color=color,
                    weight=3.5,  # Set a default weight
                    opacity=1,
                    offset=0,
                    tooltip=str(uni_flow),
                ).add_to(map)
                attr = {"font-weight": "bold", "font-size": "13"}

                folium.plugins.PolyLineTextPath(
                    line, "      >", repeat=True, offset=5, attributes=attr
                ).add_to(map)

    st_folium(map, width=725)
