import pandas as pd
import numpy as np
from us import states
import fix_differences as diff
#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/CAEMP25N__ALL_AREAS_2001_2019.csv', nrows=105270, low_memory=False)
df = pd.pivot(df, index='GeoName', columns='Description', values=['2019']).reset_index()
df['County'] = np.nan
df['State'] = np.nan
df[['County', 'State']] = df['GeoName'].str.rsplit(', ', n=1, expand=True)
df = pd.concat([df.iloc[:, 34:37], df.iloc[:, 33], df.iloc[:, 1:33]], axis=1)
df['State'] = df['State'].str.replace('*', '')
df = df.sort_values(by=['State', 'County'])
df = df.iloc[0:3138, :]
df['State'] = df['State'].apply(lambda x: states.lookup(str(x)).fips)
df = df.sort_values(by=['State', 'County'])
i = 0
for i in range(len(df)):
    df.iloc[i, 0] = str(df.iloc[i, 0]) + '_' + str(states.lookup(df.iloc[i, 1]))
df = df.drop(['State'], axis=1)
df['County'] = df['County'].str.lower()
df['County'] = df['County'].str.replace(' county', '')
df['County'] = df['County'].str.replace(' city and', '')
df['County'] = df['County'].str.replace(' borough', '')
df['County'] = df['County'].str.replace(' municipality', '')
df['County'] = df['County'].str.replace(' census area', '')
df['County'] = df['County'].str.replace(' parish', '')
df['County'] = df['County'].str.replace(' city', '')
#df = diff.fix(df, 0, 2)
#df['County'] = df['County'].apply(lambda x: x + states.lookup(str(df['State'])))
df.to_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/Cypress Output Python/Employment by industry updated pt 1.csv', index = False)