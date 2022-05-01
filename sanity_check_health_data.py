import pandas as pd
import numpy as np
import us

df_ne = pd.read_csv(r'Parsed data/All Cause Mortality without Estimates.csv')
df_r1e = pd.read_csv(r'Parsed data/All Cause Mortality with r1 Estimates.csv')
df_r2e = pd.read_csv(r'Parsed data/All Cause Mortality with r2 Estimates.csv')
df_we = pd.read_csv(r'Parsed data/All Cause Mortality with Estimates.csv')

# make sure aggregation without estimates is working as intended
current = df_ne[(df_ne['State ANSI'] == 1) & (df_ne['County ANSI'] == 17)]
# data point 1
if np.isnan(current.iloc[0, 2]):
    print("All good woe 1/12")
else:
    print("Theres a problem woe")
# data point 2
if np.isnan(current.iloc[0, 3]):
    print("All good woe 2/12")
else:
    print("Theres a problem woe")
# data point 3
if np.isnan(current.iloc[0, 4]):
    print("All good woe 3/12")
else:
    print("Theres a problem woe")


# make sure filling in nans with averages is working as intended
current = df_r1e[(df_r1e['State ANSI'] == 4) & (df_r1e['County ANSI'] == 9)]
# data point 1
#print(current['Percent Deaths 1-4'] == .0004)
if current['Percent Deaths 1-4'].iloc[0] == .0004:
    print("All good r1e 4/12")
else:
    print("Theres a problem r1e")
# data point 2
current = df_r1e[(df_r1e['State ANSI'] == 9) & (df_r1e['County ANSI'] == 15)]
if current['Percent Deaths 20-24'].iloc[0] == .00055:
    print("All good r1e 5/12")
else:
    print("Theres a problem r1e")
# data point 3
current = df_r1e[(df_r1e['State ANSI'] == 15) & (df_r1e['County ANSI'] == 5)]
if current['Percent Deaths 5-9'].iloc[0] == .00015:
    print("All good r1e 6/12")
else:
    print("Theres a problem r1e")


# make sure filling in unreliable values with averages is working as intended
# data point 1
current = df_r2e[(df_r2e['State ANSI'] == 44) & (df_r2e['County ANSI'] == 9)]
if current['Percent Deaths 25-34'].iloc[0] == .00120:
    print("All good re2-s 7/12")
else:
    print("Theres a problem r2e-s")
# data point 2
current = df_r2e[(df_r2e['State ANSI'] == 25) & (df_r2e['County ANSI'] == 19)]
if current['Percent Deaths 55-64'].iloc[0] == .00742:
    print("All good r2e-s 8/12")
else:
    print("Theres a problem r2e-s")
# data point 3
current = df_r2e[(df_r2e['State ANSI'] == 25) & (df_r2e['County ANSI'] == 11)]
if current['Percent Deaths 25-34'].iloc[0] == .00116:
    print("All good r2e-h 9/12")
else:
    print("Theres a problem r2e-h")

# make sure aggregation with estimates is working as intended
# data point 1
current = df_we[(df_we['State ANSI'] == 2) & (df_we['County ANSI'] == 282)]
if np.isnan(current['Percent Deaths_25+'].iloc[0]):
    print("All good we-nan 10/12")
else:
    print("Theres a problem we-nan")
# data point 2
current = df_we[(df_we['State ANSI'] == 6) & (df_we['County ANSI'] == 75)]
if current['Percent Deaths_0-5'].iloc[0] == .00061:
    print("All good we-cal 11/12")
else:
    print("Theres a problem we-cal")
# data point 3
current = df_we[(df_we['State ANSI'] == 48) & (df_we['County ANSI'] == 439)]
if current['Percent Deaths_5-25'].iloc[0] == .00042:
    print("All good we-cal 12/12")
else:
    print("Theres a problem we-cal")