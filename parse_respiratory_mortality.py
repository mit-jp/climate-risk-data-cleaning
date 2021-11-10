import pandas as pd
import numpy as np
import us
import fix_differences as diff
import cdc_estimation as rg
import organize_cdc_data as org
#pd.set_option('display.max_columns', None)

df = org.organize(r'CDC Wonder Data/Respiratory mortality at county level 2016.txt', r'CDC Wonder Data/Respiratory mortality at state level 2016.txt', r'CDC Wonder Data/Respiratory mortality at national level 2016.txt')
df_county, df_state, df_national = df[0], df[1], df[2]

#df_county = diff.fix(df_county, 1, 1, 1) # fill in missing counties
df_county_no_estimates = df_county.round(5) # round data
df_county_no_estimates.to_csv(r'Parsed data/Respiratory Mortality.csv', index = False) #export without estimates

# Add columns for calculated deaths, calculated population, and calculated percent deaths in state table
df_state[['CalD0-5', 'CalD25+', 'CalD5-25', 'CalP0-5', 'CalP25+', 'CalP5-25', 'Per0-5', 'Per25+', 'Per5-25']] = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

# Calculate death and population sums for each state from county data
# loop through all the state ids
i = 0
for i in range(df_state.shape[0]):
    lookat = df_county[df_county['State ANSI'] == df_state.iloc[i, 0]] # extract a subtable for each state
    #print(lookat)
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

regional_groupings = rg.create_regional_hashmap()

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
df_county.to_csv(r'Parsed data/Respiratory Mortality with estimates.csv', index = False)
