import pandas as pd
import altair as alt
import numpy as np
from vega_datasets import data

pd.options.mode.chained_assignment = None


def convert_ids(df):
    df = df[df["State ANSI"].notnull()]
    df["State ANSI"] = df["State ANSI"].astype(int)
    df["County ANSI"] = df["County ANSI"].astype(int)
    df["id"] = df["State ANSI"] * 1000 + df["County ANSI"]
    return df


def plot_counties(df, variable, color_scheme="blueorange", domain=None):
    """Plot a map of variable 'variable' in dataframe 'df'"""
    counties = alt.topo_feature(data.us_10m.url, "counties")

    df.replace({0: np.nan}, inplace=True)
    df = convert_ids(df)

    if domain:
        scale = alt.Scale(scheme=color_scheme, domain=domain, clamp=True)
    else:
        scale = alt.Scale(scheme=color_scheme)

    map_chart = (
        alt.Chart(counties)
        .mark_geoshape()
        .encode(
            color=alt.Color(
                variable + ":Q",
                scale=scale,
            ),
            tooltip=["id:O", variable + ":Q"],
        )
        .transform_lookup(lookup="id", from_=alt.LookupData(df, "id", [variable]))
        .project(type="albersUsa")
        .properties(width=800, height=400)
    )
    pdf_chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            y="count()",
            x=alt.X(variable + ":Q", bin=alt.Bin(maxbins=40)),
        )
        .transform_lookup(lookup="id", from_=alt.LookupData(df, "id", [variable]))
    )
    return map_chart | pdf_chart


def plot_states(df, variable, color_scheme="blueorange", domain=None):
    id_col = "State Code"
    states = alt.topo_feature(data.us_10m.url, "states")
    if domain:
        scale = alt.Scale(scheme=color_scheme, domain=domain, clamp=True)
    else:
        scale = alt.Scale(scheme=color_scheme)

    chart = (
        alt.Chart(states)
        .mark_geoshape()
        .encode(
            color=alt.Color(
                variable + ":Q",
                scale=scale,
            ),
            tooltip=["id:O", variable + ":Q"],
        )
        .transform_lookup(lookup="id", from_=alt.LookupData(df, id_col, [variable]))
        .project(type="albersUsa")
        .properties(width=800, height=400)
    )
    return chart
