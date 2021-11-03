import pandas as pd
import numpy as np
import us
import fix_differences as diff
#pd.set_option('display.max_columns', None)

# Import all datasets
df_county = pd.read_csv(r'CDC Wonder Data/All-cause mortality at county level 2016.txt', sep='\t', engine='python')
df_state = pd.read_csv(r'CDC Wonder Data/All-cause mortality at state level 2016.txt', sep='\t', engine='python')
df_national = pd.read_csv(r'CDC Wonder Data/All-cause mortality at national level 2016.txt', sep='\t', engine='python')

# Organize the data
#drop unnecessary columns
df_county = df_county.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)
df_state = df_state.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)
df_national = df_national.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)

#drop rows full of nans
df_county = df_county.dropna(how='all')
df_state = df_state.dropna(how='all')
df_national = df_national.dropna(how='all')

df_county['State ANSI'] = (df_county['County Code']/1000).apply(np.floor) #extract state code from fpis code
df_county['County ANSI'] = df_county['County Code']-(df_county['County Code']/1000).apply(np.floor)*1000 #extract county code from fpis code
df_county = df_county.drop(['County', 'County Code'], axis=1) #drop county and dounty code rows
df_state = df_state.drop(['State'], axis=1)


# Group ages into specified ranges
df_county = df_county.replace({'Age Group Code':{'1': '0-5', '1-4':'0-5', '5-9':'5-25', '10-14':'5-25', '15-19':'5-25', '20-24':'5-25', '25-34':'25+', '35-44':'25+', '45-54':'25+', '55-64':'25+', '65-74':'25+', '75-84':'25+', '85+':'25+'}})
df_state = df_state.replace({'Age Group Code':{'1': '0-5', '1-4':'0-5', '5-9':'5-25', '10-14':'5-25', '15-19':'5-25', '20-24':'5-25', '25-34':'25+', '35-44':'25+', '45-54':'25+', '55-64':'25+', '65-74':'25+', '75-84':'25+', '85+':'25+'}})
df_national = df_national.replace({'Age Group Code':{'1': '0-5', '1-4':'0-5', '5-9':'5-25', '10-14':'5-25', '15-19':'5-25', '20-24':'5-25', '25-34':'25+', '35-44':'25+', '45-54':'25+', '55-64':'25+', '65-74':'25+', '75-84':'25+', '85+':'25+'}})

# Clean up data and reorder
# replace 'supprssed' and 'missing' with nans to allow for math operations
df_county= df_county.replace({'Deaths': {'Suppressed':np.nan, 'Missing':np.nan}, 'Population': {'Suppressed':np.nan, 'Missing':np.nan}})
df_state= df_state.replace({'Deaths': {'Suppressed':np.nan, 'Missing':np.nan}, 'Population': {'Suppressed':np.nan, 'Missing':np.nan}})

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
df_county.columns = ['_'.join(col) for col in df_county.columns.values]
df_county = df_county.reset_index()
df_state = df_state.unstack(level=1)
df_state.columns = ['_'.join(col) for col in df_state.columns.values]

# add columns for later use in filling in nans
df_state[['CalD0-5', 'CalD25+', 'CalD5-25', 'CalP0-5', 'CalP25+', 'CalP5-25', 'Per0-5', 'Per25+', 'Per5-25']] = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
df_state = df_state.reset_index()
df_county = df_county.sort_values(by=['State ANSI', 'County ANSI']) # resort rows

#calculate percent deaths for each age group
df_county['Percent Deaths 0-5'] = df_county['Deaths_0-5']/df_county['Population_0-5']
df_county['Percent Deaths 25+'] = df_county['Deaths_25+']/df_county['Population_25+']
df_county['Percent Deaths 5-25'] = df_county['Deaths_5-25']/df_county['Population_5-25']


# Get ready for export
df_county = diff.fix(df_county, 1, 1, 1) # fill in missing counties
df_county_no_estimates = df_county.round(5) # round data
df_county_no_estimates.to_csv(r'Parsed data/All Cause Mortality.csv', index = False) #export without estimates

# Add columns for calculated deaths, calculated population, and calculated percent deaths in state table
df_state[['CalD0-5', 'CalD25+', 'CalD5-25', 'CalP0-5', 'CalP25+', 'CalP5-25', 'Per0-5', 'Per25+', 'Per5-25']] = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

# Calculate death and population sums for each state from county data
# loop through all the state ids
i = 0
for i in range(df_state.shape[0]):
    lookat = df_county[df_county['State ANSI'] == df_state.iloc[i, 0]] # extract a subtable for each state
    j = 0
    for j in range(3):
        df_state.iloc[i, j+7] = lookat.iloc[:, j+2].sum() # sum the deaths for each county in a state, for each age range, and put that calculated sum in the state table
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
    for j in range(3): # do this foreach age group
        if df_state.iloc[i, j + 10] != 0:
            df_state.iloc[i, j + 13] = (df_state.iloc[i, j + 1] - df_state.iloc[i, j + 7]) / df_state.iloc[i, j + 10]

# Add calculated state death rate to those counties with suppressed percent rates
i = 0
j = 0
# loop through all counties in county table
for i in range(df_county.shape[0]):
    for j in range(3):
        if df_county.iloc[i, j + 8] == 0:
            state = df_state[df_state['State Code'] == df_county.iloc[i, 0]] # look up state code
            df_county.iloc[i, j + 8] = state.iloc[0, j + 13] # replace value with calculated value

# Calculate the national death rate
df_national['Percent Deaths'] = df_national['Deaths']/df_national['Population']

# Replace supressed state level death rates with national death rate
i = 0
j = 0
# loop through all counties
for i in range(df_county.shape[0]):
    for j in range(3):
        if df_county.iloc[i, j + 8] == 0: # if death rate still supressed
            df_county.iloc[i, j + 8] = df_national.iloc[j, 2] # replace with national rate

# Put all states into regions, dictionary of lists
regional_groupings = {'northeast': ['Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'Connecticut', 'New York',
'New Jersey', 'Pennsylvania'], 'midwest': ['Ohio', 'Indiana', 'Illinois', 'Michigan', 'Wisconsin', 'Minnesota', 'Iowa', 'Missouri', 'North Dakota',
'South Dakota', 'Nebraska', 'Kansas'], 'south': ['Delaware', 'Maryland', 'District of Columbia', 'Virginia', 'West Virginia', 'North Carolina', 'South Carolina', 'Georgia', 'Florida', 'Kentucky', 'Tennessee', 'Alabama', 'Mississippi', 'Arkansas',
'Louisiana', 'Oklahoma', 'Texas'], 'west': ['Montana', 'Idaho', 'Wyoming', 'Colorado', 'New Mexico', 'Arizona', 'Utah', 'Nevada', 'Washington',
'Oregon', 'California', 'Alaska', 'Hawaii']}

# Replace state names with state codes
for k in regional_groupings.keys():# loop through all keys
    i = 0
    for i in range(len(regional_groupings[k])): # loop through all the values
        state = regional_groupings[k][i].lower()
        regional_groupings[k][i] = int(us.states.lookup(state).fips) # replace by fips code

# Extract the counties, for each age group, with death counts between 0-20 (determined unreliable)
df_county_sub_20_0_5 = df_county[(df_county['Deaths_0-5'] < 20) & (df_county['Deaths_0-5'] > 0)]
df_county_sub_20_5_25 = df_county[(df_county['Deaths_5-25'] < 20) & (df_county['Deaths_5-25'] > 0)]
df_county_sub_20_25 = df_county[(df_county['Deaths_25+'] < 20) & (df_county['Deaths_25+'] > 0)]

# create tables for the regional groups
df_county_sub_20_regional0_5 = df_county_sub_20_0_5
df_county_sub_20_regional5_25 = df_county_sub_20_5_25
df_county_sub_20_regional25 = df_county_sub_20_25

# Remove all the states for which there is only one unreliable death, that means you would need a regional total
i = 0
for i in range(df_state.shape[0]):
    # create tables for each state among the table of unreliable deaths
    state0_5 = df_county_sub_20_regional0_5[df_county_sub_20_regional0_5['State ANSI'] == df_state.iloc[i, 0]]
    state5_25 = df_county_sub_20_regional5_25[df_county_sub_20_regional5_25['State ANSI'] == df_state.iloc[i, 0]]
    state25 = df_county_sub_20_regional25[df_county_sub_20_regional25['State ANSI'] == df_state.iloc[i, 0]]

    # if the sum of of the counties in a state is less than 20, take it out of the regional set, for each age group
    if state0_5.iloc[:, 2].sum() >= 20:
        df_county_sub_20_regional0_5 = df_county_sub_20_regional0_5[df_county_sub_20_regional0_5['State ANSI'] != df_state.iloc[i, 0]] # drop all counties with current state code
    if state5_25.iloc[:, 3].sum() >= 20:
        df_county_sub_20_regional5_25 = df_county_sub_20_regional5_25[
            df_county_sub_20_regional5_25['State ANSI'] != df_state.iloc[i, 0]]
    if state25.iloc[:, 4].sum() >= 20:
        df_county_sub_20_regional25 = df_county_sub_20_regional25[
            df_county_sub_20_regional25['State ANSI'] != df_state.iloc[i, 0]]

# Create a disjoint set from the original, with all the states with sums greater than 20
df_county_sub_20_state0_5 = df_county_sub_20_0_5.drop(df_county_sub_20_regional0_5.index)
df_county_sub_20_state5_25 = df_county_sub_20_5_25.drop(df_county_sub_20_regional5_25.index)
df_county_sub_20_state25 = df_county_sub_20_25.drop(df_county_sub_20_regional25.index)

# Replace unreliable values with estimates, determining if they need a state or regional average
i = 0
for i in range(df_county.shape[0]): #loop through all counties
    j = 0
    for j in range(3):
        if (df_county.iloc[i, j+2] < 20) & (df_county.iloc[i, j+2] > 0): # if county death count is unreliable
            if j == 0: # for each age group
                if df_county.iloc[i, 0] in list(df_county_sub_20_state0_5['State ANSI']): # if state code is in state table, use value in state table
                    df_county.iloc[i, j + 8] = df_county_sub_20_state0_5.iloc[:, j+2].sum() / df_county_sub_20_state0_5.iloc[:, j+5].sum() # replace death rate with sum of death rates in state table divided by population
                elif df_county.iloc[i, 0] in list(df_county_sub_20_regional0_5['State ANSI']): # use regional table
                    # check which region the state is in
                    region = ''
                    if df_county.iloc[i, 0] in regional_groupings['northeast']:
                        region = 'northeast'
                    elif df_county.iloc[i, 0] in regional_groupings['midwest']:
                        region = 'midwest'
                    elif df_county.iloc[i, 0] in regional_groupings['south']:
                        region = 'south'
                    elif df_county.iloc[i, 0] in regional_groupings['west']:
                        region = 'west'
                    # extract region from regional table
                    subregiontable = df_county_sub_20_regional0_5[df_county_sub_20_regional0_5['State ANSI'].isin(regional_groupings[region])]
                    df_county.iloc[i, j + 8] = subregiontable.iloc[:,
                                               j + 2].sum() / subregiontable.iloc[:, j + 5].sum()
            elif j == 1:
                if df_county.iloc[i, 0] in list(df_county_sub_20_state25['State ANSI']):
                    df_county.iloc[i, j + 8] = df_county_sub_20_state25.iloc[:, j + 2].sum() / df_county_sub_20_state25.iloc[:, j + 5].sum()
                elif df_county.iloc[i, 0] in list(df_county_sub_20_regional25['State ANSI']):
                    region = ''
                    if df_county.iloc[i, 0] in regional_groupings['northeast']:
                        region = 'northeast'
                    elif df_county.iloc[i, 0] in regional_groupings['midwest']:
                        region = 'midwest'
                    elif df_county.iloc[i, 0] in regional_groupings['south']:
                        region = 'south'
                    elif df_county.iloc[i, 0] in regional_groupings['west']:
                        region = 'west'
                    subregiontable = df_county_sub_20_regional25[df_county_sub_20_regional25['State ANSI'].isin(regional_groupings[region])]
                    df_county.iloc[i, j + 8] = subregiontable.iloc[:,
                                               j + 2].sum() / subregiontable.iloc[:, j + 5].sum()
            elif j == 2:
                if df_county.iloc[i, 0] in list(df_county_sub_20_state5_25['State ANSI']):
                    df_county.iloc[i, j + 8] = df_county_sub_20_state5_25.iloc[:, j + 2].sum() / df_county_sub_20_state5_25.iloc[:, j + 5].sum()
                elif df_county.iloc[i, 0] in list(df_county_sub_20_regional5_25['State ANSI']):
                    region = ''
                    if df_county.iloc[i, 0] in regional_groupings['northeast']:
                        region = 'northeast'
                    elif df_county.iloc[i, 0] in regional_groupings['midwest']:
                        region = 'midwest'
                    elif df_county.iloc[i, 0] in regional_groupings['south']:
                        region = 'south'
                    elif df_county.iloc[i, 0] in regional_groupings['west']:
                        region = 'west'
                    subregiontable = df_county_sub_20_regional5_25[df_county_sub_20_regional5_25['State ANSI'].isin(regional_groupings[region])]
                    df_county.iloc[i, j + 8] = subregiontable.iloc[:,
                                               j + 2].sum() / subregiontable.iloc[:, j + 5].sum()

# Round
df_county = df_county.round(5)
df_state = df_state.round(5)
df_national = df_national.round(5)

# Export
df_county.to_csv(r'Parsed data/All Cause Mortality with estimates.csv', index = False)
