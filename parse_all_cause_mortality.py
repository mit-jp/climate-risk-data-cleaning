import pandas as pd
import numpy as np
import fix_differences as diff
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
df_national = df_county.dropna(how='all')
df_national = df_national.replace({'Age Group Code':{'1': '0-5', '1-4':'0-5', '5-9':'5-25', '10-14':'5-25', '15-19':'5-25', '20-24':'5-25', '25-34':'25+', '35-44':'25+', '45-54':'25+', '55-64':'25+', '65-74':'25+', '75-84':'25+', '85+':'25+'}})
df_county= df_county.replace({'Deaths': {'Suppressed':np.nan, 'Missing':np.nan}, 'Population': {'Suppressed':np.nan, 'Missing':np.nan}})
df_county['Deaths'] = df_county['Deaths'].astype(float)
df_county['Population'] = df_county['Population'].astype(float)
df_county = df_county.groupby(['State ANSI', 'County ANSI', 'Age Group Code']).sum()
df_state= df_state.replace({'Deaths': {'Suppressed':np.nan, 'Missing':np.nan}, 'Population': {'Suppressed':np.nan, 'Missing':np.nan}})
df_state['Deaths'] = df_state['Deaths'].astype(float)
df_state = df_state.groupby(['State Code', 'Age Group Code'])['Deaths'].sum()
i = 0
for i in range(df_county.shape[0]):
    if df_county.iloc[i, 0] == 0.0:
        print(df_county.iloc[i, 0])

#df_county.loc[1.0, :, '0-5'].sum()
