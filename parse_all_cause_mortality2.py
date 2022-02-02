import fix_differences as diff
import pandas as pd
import numpy as np

# Import all datasets
df_county = pd.read_csv(r'CDC Wonder Data/All-cause mortality at county level 2016.txt', sep='\t',
                        engine='python')
df_state = pd.read_csv(r'CDC Wonder Data/All-cause mortality at state level 2016.txt', sep='\t', engine='python')
df_national = pd.read_csv(r'CDC Wonder Data/All-cause mortality at national level 2016.txt', sep='\t',
                          engine='python')

# Organize the data
# drop unnecessary columns
df_county = df_county.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)
df_state = df_state.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)
df_national = df_national.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)

# drop rows full of nans
df_county = df_county.dropna(how='all')
df_state = df_state.dropna(how='all')
df_national = df_national.dropna(how='all')

df_county['State ANSI'] = (df_county['County Code'] / 1000).apply(np.floor)  # extract state code from fpis code
df_county['County ANSI'] = df_county['County Code'] - (df_county['County Code'] / 1000).apply(
    np.floor) * 1000  # extract county code from fpis code
df_county = df_county.drop(['County', 'County Code'], axis=1)  # drop county and dounty code rows
df_state = df_state.drop(['State'], axis=1)

'''# Group ages into specified ranges
df_county = df_county.replace({'Age Group Code': {'1': '0-5', '1-4': '0-5', '5-9': '5-25', '10-14': '5-25',
                                                  '15-19': '5-25', '20-24': '5-25', '25-34': '25+', '35-44': '25+',
                                                  '45-54': '25+', '55-64': '25+', '65-74': '25+', '75-84': '25+',
                                                  '85+': '25+'}})
df_state = df_state.replace({'Age Group Code': {'1': '0-5', '1-4': '0-5', '5-9': '5-25', '10-14': '5-25',
                                                '15-19': '5-25', '20-24': '5-25', '25-34': '25+', '35-44': '25+',
                                                '45-54': '25+', '55-64': '25+', '65-74': '25+', '75-84': '25+',
                                                '85+': '25+'}})
df_national = df_national.replace({'Age Group Code': {'1': '0-5', '1-4': '0-5', '5-9': '5-25', '10-14': '5-25',
                                                      '15-19': '5-25', '20-24': '5-25', '25-34': '25+',
                                                      '35-44': '25+', '45-54': '25+', '55-64': '25+',
                                                      '65-74': '25+', '75-84': '25+', '85+': '25+'}})'''

# Clean up data and reorder
# replace 'supprssed' and 'missing' with nans to allow for math operations
df_county = df_county.replace(
    {'Deaths': {'Suppressed': np.nan, 'Missing': np.nan}, 'Population': {'Suppressed': np.nan, 'Missing': np.nan}})
df_state = df_state.replace(
    {'Deaths': {'Suppressed': np.nan, 'Missing': np.nan}, 'Population': {'Suppressed': np.nan, 'Missing': np.nan}})

# set class of deaths and population to float
df_county['Deaths'] = df_county['Deaths'].astype(float)
df_county['Population'] = df_county['Population'].astype(float)
df_state['Deaths'] = df_state['Deaths'].astype(float)


# sum column values by state, then county, then age group code. needs to be done because multiple values for each combination due to higher granualrity in orginial data
df_county = df_county.groupby(['State ANSI', 'County ANSI', 'Age Group Code']).sum()
df_state = df_state.groupby(['State Code', 'Age Group Code']).sum()
df_national = df_national.groupby(['Age Group Code']).sum()

# unstack from multiindexing
df_county = df_county.unstack(level=2)
categories = df_county.columns.values
ages = set([col[1] for col in categories])
df_county.columns = ['_'.join(col) for col in df_county.columns.values]
df_county = df_county.reset_index()
df_county = df_county.sort_values(by=['State ANSI', 'County ANSI'])  # resort rows


df_state = df_state.unstack(level=1)
df_state.columns = ['_'.join(col) for col in df_state.columns.values]
df_state = df_state.reset_index()

for age in ages:
    df_county['Percent Deaths ' + age] = df_county['Deaths_' + age]/df_county['Population_' + age]



# Add columns for calculated deaths, calculated population, and calculated percent deaths in state table
    df_state[['CalD0-5', 'CalD25+', 'CalD5-25', 'CalP0-5', 'CalP25+', 'CalP5-25', 'Per0-5', 'Per25+', 'Per5-25']] = [
        np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

    # Calculate death and population sums for each state from county data
    # loop through all the state ids
    i = 0
    for i in range(df_state.shape[0]):
        lookat = df_county[df_county['State ANSI'] == df_state.iloc[i, 0]]  # extract a subtable for each state
        # print(lookat)
        j = 0
        for j in range(3):
            df_state.iloc[i, j + 7] = lookat.iloc[:,
                                      j + 2].sum()  # sum the deaths for each county in a state, for each age range, and put that calculated sum in the state table
        # extract only the counties in a state with suppressed death rates (done automatically in sum of deaths)
        lookatP0_5 = lookat[lookat['Deaths_0-5'] == 0]
        lookatP5_25 = lookat[lookat['Deaths_5-25'] == 0]
        lookatP25 = lookat[lookat['Deaths_25+'] == 0]
        # sum the populations for only those counties that have a supressed death, add that value to the state table
        df_state.iloc[i, 10] = lookatP0_5['Population_0-5'].sum()
        df_state.iloc[i, 11] = lookatP25['Population_25+'].sum()
        df_state.iloc[i, 12] = lookatP5_25['Population_5-25'].sum()

    # Calculate the percent deaths in a state for only those counties with suppressed death counts
    i = 0
    j = 0
    for i in range(df_state.shape[0]):
        for j in range(3):  # do this foreach age group
            if df_state.iloc[i, j + 10] != 0:
                df_state.iloc[i, j + 13] = (df_state.iloc[i, j + 1] - df_state.iloc[i, j + 7]) / df_state.iloc[
                    i, j + 10]
    return df_state, df_county







'''
# calculate percent deaths for each age group
df_county['Percent Deaths 0-5'] = df_county['Deaths_0-5'] / df_county['Population_0-5']
df_county['Percent Deaths 25+'] = df_county['Deaths_25+'] / df_county['Population_25+']
df_county['Percent Deaths 5-25'] = df_county['Deaths_5-25'] / df_county['Population_5-25']

# Calculate the national death rate
df_national['Percent Deaths'] = df_national['Deaths'] / df_national['Population']
'''