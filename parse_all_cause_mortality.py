import pandas as pd
import numpy as np
import us
import fix_differences as diff
pd.set_option('display.max_columns', None)
df_county = pd.read_csv(r'CDC Wonder Data/All-cause mortality at county level 2016.txt', sep='\t', engine='python')
df_state = pd.read_csv(r'CDC Wonder Data/All-cause mortality at state level 2016.txt', sep='\t', engine='python')
df_national = pd.read_csv(r'CDC Wonder Data/All-cause mortality at national level 2016.txt', sep='\t', engine='python')
df_county = df_county.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)
df_county = df_county.dropna(how='all')
df_county['State ANSI'] = (df_county['County Code']/1000).apply(np.floor)
df_county['County ANSI'] = df_county['County Code']-(df_county['County Code']/1000).apply(np.floor)*1000
df_county = df_county.drop(['County', 'County Code'], axis=1)
df_county = df_county.replace({'Age Group Code':{'1': '0-5', '1-4':'0-5', '5-9':'5-25', '10-14':'5-25', '15-19':'5-25', '20-24':'5-25', '25-34':'25+', '35-44':'25+', '45-54':'25+', '55-64':'25+', '65-74':'25+', '75-84':'25+', '85+':'25+'}})
df_state = df_state.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)
df_state = df_state.dropna(how='all')
df_state = df_state.drop(['State'], axis=1)
df_state = df_state.replace({'Age Group Code':{'1': '0-5', '1-4':'0-5', '5-9':'5-25', '10-14':'5-25', '15-19':'5-25', '20-24':'5-25', '25-34':'25+', '35-44':'25+', '45-54':'25+', '55-64':'25+', '65-74':'25+', '75-84':'25+', '85+':'25+'}})
df_national = df_national.drop(['Notes', 'Age Group', 'Crude Rate'], axis=1)
df_national = df_national.dropna(how='all')
df_national = df_national.replace({'Age Group Code':{'1': '0-5', '1-4':'0-5', '5-9':'5-25', '10-14':'5-25', '15-19':'5-25', '20-24':'5-25', '25-34':'25+', '35-44':'25+', '45-54':'25+', '55-64':'25+', '65-74':'25+', '75-84':'25+', '85+':'25+'}})
df_county= df_county.replace({'Deaths': {'Suppressed':np.nan, 'Missing':np.nan}, 'Population': {'Suppressed':np.nan, 'Missing':np.nan}})
df_county['Deaths'] = df_county['Deaths'].astype(float)
df_county['Population'] = df_county['Population'].astype(float)
df_county = df_county.groupby(['State ANSI', 'County ANSI', 'Age Group Code']).sum()
df_state= df_state.replace({'Deaths': {'Suppressed':np.nan, 'Missing':np.nan}, 'Population': {'Suppressed':np.nan, 'Missing':np.nan}})
df_state['Deaths'] = df_state['Deaths'].astype(float)
df_state = df_state.groupby(['State Code', 'Age Group Code']).sum()
df_national = df_national.groupby(['Age Group Code']).sum()
df_county = df_county.unstack(level=2)
df_county.columns = ['_'.join(col) for col in df_county.columns.values]
df_county = df_county.reset_index()
df_state = df_state.unstack(level=1)
df_state.columns = ['_'.join(col) for col in df_state.columns.values]
df_state[['CalD0-5', 'CalD5-25', 'CalD25+', 'CalP0-5', 'CalP5-25', 'CalP25+', 'Per0-5', 'Per5-25', 'Per25+']] = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
df_state = df_state.reset_index()
df_county = df_county.sort_values(by=['State ANSI', 'County ANSI'])
df_county['Percent Deaths 0-5'] = df_county['Deaths_0-5']/df_county['Population_0-5']
df_county['Percent Deaths 5-25'] = df_county['Deaths_5-25']/df_county['Population_5-25']
df_county['Percent Deaths 25+'] = df_county['Deaths_25+']/df_county['Population_25+']
df_county = diff.fix(df_county, 1, 1, 1)
df_county.to_csv(r'Parsed data/All Cause Mortality.csv', index = False)

i = 0
for i in range(df_state.shape[0]):
    lookatD = df_county[df_county['State ANSI'] == df_state.iloc[i, 0]]
    j = 0
    for j in range(3):
        df_state.iloc[i, j+7] = lookatD.iloc[:, j+2].sum()
    lookP0_5 = df_county[df_county['State ANSI'] == df_state.iloc[i, 0]]
    lookatP0_5 = lookP0_5[lookP0_5['Deaths_0-5'] == 0]
    lookP5_25 = df_county[df_county['State ANSI'] == df_state.iloc[i, 0]]
    lookatP5_25 = lookP5_25[lookP5_25['Deaths_5-25'] == 0]
    lookP25 = df_county[df_county['State ANSI'] == df_state.iloc[i, 0]]
    lookatP25 = lookP25[lookP25['Deaths_25+'] == 0]
    df_state.iloc[i, 10] = lookatP0_5['Population_0-5'].sum()
    df_state.iloc[i, 11] = lookatP5_25['Population_5-25'].sum()
    df_state.iloc[i, 12] = lookatP25['Population_25+'].sum()
i = 0
j = 0
for i in range(df_state.shape[0]):
    for j in range(3):
        if df_state.iloc[i, j + 10] != 0:
            df_state.iloc[i, j + 13] = (df_state.iloc[i, j + 1] - df_state.iloc[i, j + 7]) / df_state.iloc[i, j + 10]

i = 0
j = 0
for i in range(df_county.shape[0]):
    for j in range(3):
        if df_county.iloc[i, j + 8] == 0:
            state = df_state[df_state['State Code'] == df_county.iloc[i, 0]]
            df_county.iloc[i, j + 8] = state.iloc[0, j + 13]

df_national['Percent Deaths'] = df_national['Deaths']/df_national['Population']
i = 0
j = 0
for i in range(df_county.shape[0]):
    for j in range(3):
        if df_county.iloc[i, j + 8] == 0:
            df_county.iloc[i, j + 8] = df_national.iloc[j, 2]


'''
regional_groupings = {'northeast': ['Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'Connecticut', 'New York',
'New Jersey', 'Pennsylvania'], 'midwest': ['Ohio', 'Indiana', 'Illinois', 'Michigan', 'Wisconsin', 'Minnesota', 'Iowa', 'Missouri', 'North Dakota',
'South Dakota', 'Nebraska', 'Kansas'], 'south': ['Delaware', 'Maryland', 'District of Columbia', 'Virginia', 'West Virginia', 'North Carolina', 'South Carolina', 'Georgia', 'Florida', 'Kentucky', 'Tennessee', 'Alabama', 'Mississippi', 'Arkansas',
'Louisiana', 'Oklahoma', 'Texas'], 'west': ['Montana', 'Idaho', 'Wyoming', 'Colorado', 'New Mexico', 'Arizona', 'Utah', 'Nevada', 'Washington',
'Oregon', 'California', 'Alaska', 'Hawaii']}

for k in regional_groupings.keys():
    i = 0
    for i in range(len(regional_groupings[k])):
        state = regional_groupings[k][i].lower()
        regional_groupings[k][i] = int(us.states.lookup(state).fips)

'''

df_county.round(5)
df_state.round(5)
df_national.round(5)

df_county.to_csv(r'Parsed data/All Cause Mortality with estimates.csv', index = False)