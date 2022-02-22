import fix_differences as diff
import pandas as pd
import numpy as np
import cdc_estimation_functions as rg

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

df_national['Percent Deaths'] = df_national['Deaths']/df_national['Population']

'''
for age in ages:
    ep = 0
    excp = 0
    for i in range(df_county.shape[0]):
            if df_county.loc[i, 'Population_' + age] == 0:
                ep += 1
            if df_county.loc[i, 'Population_' + age] == 0 and df_county.loc[i, 'Deaths_' + age] != 0:
                excp += 1
    print(age + ': ' + str(ep))
    print("\\")
    print(age + ': ' + str(excp))
'''

for age in ages:
    df_county['Percent Deaths ' + age] = df_county['Deaths_' + age]/df_county['Population_' + age]
    df_state[['CalDt' + age, 'CalPop' + age, 'CalPer' + age]] = [np.nan, np.nan, np.nan]

i = 0
for i in range(df_state.shape[0]):
    lookat = df_county[df_county['State ANSI'] == df_state.loc[i, 'State Code']]  # extract a subtable for each state
    for age in ages:
        df_state.loc[i, 'CalDt' + age] = lookat.loc[:, 'Deaths_' + age].sum()
        df_state.loc[i, 'CalPop' + age] = lookat[lookat['Deaths_' + age] == 0]['Population_' + age].sum()

for age in ages:
    df_state['CalPer' + age] = df_state['CalDt' + age]/df_state['CalPop' + age][~(df_state['CalPop' + age] == 0)]
    i = 0
    # loop through all counties in county table
    for i in range(df_county.shape[0]):
        if df_county.loc[i, 'Deaths_' + age] == 0:
            state = df_state[df_state['State Code'] == df_county.loc[i, 'State ANSI']].reset_index()
            if state.loc[0, 'CalPer' + age] != 0:
                df_county.loc[i, 'Percent Deaths ' + age] = state.loc[0, 'CalPer' + age]
            else:
                df_county.loc[i, 'Percent Deaths ' + age] = df_national.loc[age, 'Percent Deaths']


regional_groupings = rg.create_regional_hashmap()


for age in ages:
    df_county_sub_20 = df_county[(df_county['Deaths_' + age] < 20) & (df_county['Deaths_' + age] > 0)]
    df_county_sub_20_regional = df_county_sub_20
    i = 0
    for i in range(df_state.shape[0]):
        state = df_county_sub_20_regional[df_county_sub_20_regional['State ANSI'] == df_state.iloc[i, 0]]
        if state.loc[:, 'Deaths_' + age].sum() >= 20:
            df_county_sub_20_regional = df_county_sub_20_regional[df_county_sub_20_regional['State ANSI'] != df_state.iloc[i, 0]]  # drop all counties with current state code
    df_county_sub_20_state = df_county_sub_20.drop(df_county_sub_20_regional.index)
    i = 0
    for i in range(df_county.shape[0]):  # loop through all counties
        if (df_county.loc[i, 'Deaths_' + age] < 20) & (df_county.loc[i, 'Deaths_' + age] > 0):  # if county death count is unreliable
            if df_county.loc[i, 'State ANSI'] in list(df_county_sub_20_state['State ANSI']):  # if state code is in state table, use value in state table
                current = df_county_sub_20_state[df_county_sub_20_state['State ANSI'] == df_county.loc[i, 'State ANSI']]
                df_county.loc[i, 'Percent Deaths ' + age] = current.loc[:, 'Deaths_' + age].sum()/current.loc[:, 'Population_' + age].sum()  # replace death rate with sum of death rates in state table divided by population
            else:
                region = rg.get_region_from_state(df_county.loc[i, 'State ANSI'], regional_groupings)
                current = df_county_sub_20_regional[df_county_sub_20_regional['State ANSI'].isin(regional_groupings[region])]
                df_county.loc[i, 'Percent Deaths ' + age] = current.loc[:, 'Deaths_' + age].sum() / current.loc[:, 'Population_' + age].sum()


for age in ages:
    i = 0
    for i in range(df_county.shape[0]):
        if df_county.loc[i, 'Deaths_' + age] == 0:
            df_county.loc[i, 'Deaths_' + age] = df_county.loc[i, 'Population_' + age] * df_county.loc[i, 'Percent Deaths ' + age]


'''
# Group ages into specified ranges
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
                                                      '65-74': '25+', '75-84': '25+', '85+': '25+'}})


df_county = diff.fix(df_county, 1, 1, 1) # fill in missing counties
df_county_no_estimates = df_county.round(5) # round data
df_county_no_estimates.to_csv(r'Parsed data/All Cause Mortality.csv', index = False) #export without estimates
'''

df_county_test = df_county.round(5) # round data
df_county_test.to_csv(r'Parsed data/All Cause Mortality.csv', index = False) #export without estimates