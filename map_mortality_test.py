import seaborn as sns
import pandas as pd
import altair as alt
import numpy as np
from vega_datasets import data

sns.set_theme(style="whitegrid")
pd.options.mode.chained_assignment = None


def convert_ids(df):
    df = df[df["State ANSI"].notnull()]
    df["State ANSI"] = df["State ANSI"].astype(int)
    df["County ANSI"] = df["County ANSI"].astype(int)
    df["id"] = df["State ANSI"] * 1000 + df["County ANSI"]
    return df


def plot(df, variable):
    """Plot a map of variable 'variable' in dataframe 'df'"""
    counties = alt.topo_feature(data.us_10m.url, "counties")

    df.replace({0: np.nan}, inplace=True)
    df = convert_ids(df)

    map_chart = (
        alt.Chart(counties)
        .mark_geoshape()
        .encode(
            color=alt.Color(
                variable + ":Q",
                scale=alt.Scale(
                    scheme="blueorange",
                ),
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


# # Estimated data
#
# In this example, the estimated data falls far outside the distribution of the true data, indicating it may not be based on their mean.

estimated_data = pd.read_csv("Parsed data/Respiratory Mortality with estimates.csv")

estimated_plot = plot(estimated_data, "Percent Deaths 25+")
estimated_plot.save("Plots/estimated_mortality.html")
estimated_plot

# # Measured data
#
# In this example, the measured data fall within a smooth distribution.

measured_data = pd.read_csv("Parsed data/All Cause Mortality.csv")

measured_plot = plot(measured_data, "Percent Deaths 25+")
measured_plot.save("Plots/measured_mortality.html")
measured_plot
