import pandas as pd
import numpy as np
import re
from us import states
import useful_analysis_functions as fns
import fix_differences as diff
#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.read_csv(r'Project data/CAEMP25N__ALL_AREAS_2001_2019.csv', nrows=104478, low_memory=False) #read data in

# Format file according to standard specs
df = pd.pivot(df, index='GeoName', columns='Description', values=['2019']).reset_index() #pivot columns and rows
df = fns.split_county_state_names(df, ', ', 33, 'GeoName') #split name into county and state columns
df = pd.concat([df.iloc[:, 0:2], df.iloc[:, 34], df.iloc[:, 2:34]], axis=1) #move total employment to 3rd column
df['State'] = df['State'].str.replace('*', '') # remove all stars in state name
df = df.sort_values(by=['State', 'County']) # sort
df = df.iloc[0:3114, :] #remove excess
df['State'] = df['State'].apply(lambda x: states.lookup(str(x)).fips) # replace state name with state code for sorting
df = df.sort_values(by=['State', 'County']) #resort

# combine county and state columns with underscore between, replacing the state code with state name
i = 0
for i in range(len(df)):
    df.iloc[i, 0] = str(df.iloc[i, 0]) + '_' + str(states.lookup(df.iloc[i, 1]))
df = df.drop(['State'], axis=1)

df = fns.remove_confusing_words(df, 'County') # remove excess words in county names
df.columns = [x[1] for x in df.columns] # transform dual index column names to single index
df.columns.values[0] = "county_state" # rename column

# replace empty values with nans
df = df.replace('(D)', np.nan)
df = df.replace('(NA)', np.nan)

#Replace absolute value with percent of total
for i in range(2, df.shape[1]):
    for j in range(df.shape[0]):
        if pd.notnull(df.iloc[j, i]):
            df.iloc[j, i] = (int(df.iloc[j, i]) / int(df.iloc[j, 1]))*100
df.iloc[:, 1:] = df.iloc[:, 1:].astype(float).round(2) # round

# split maui and kalawao
df = pd.concat([df[0:548], pd.DataFrame([], index=[548]), df[548:]])
df.iloc[548,:] = df.iloc[550,:]
df.iloc[548, 0] = 'kalawao_hawaii'
df.iloc[550, 0] = 'maui_hawaii'

df = fns.switch_two_rows(df, [740, 1138, 1351, 1432], [741, 1139, 1352, 1433]) # switch rows that are missorted

# Fix all the issues with Virginia

# extract a virginia from reference and current table
ref = pd.read_csv(r'Parsed data/ID match resorted.csv')
ref_virginia = ref.loc[ref["county_State"].str.endswith("_virginia")]
df_virginia = df.loc[df["county_state"].str.endswith("_virginia")]
df_virginia = df_virginia.reset_index()
df_virginia = df_virginia.drop(['index'], axis=1)

i = 0
while i < 133:
    df_virginia['county_state'] = df_virginia['county_state'].str.replace('\(independent\)', '')
    df_virginia['county_state'] = df_virginia['county_state'].str.replace('+', ',')
    m = df_virginia.iloc[i,0].split(',')
    if len(m) == 2:
        df_virginia.iloc[i, 0] = m[0] + '_virginia'
        df_virginia = df_virginia.append(df_virginia.iloc[i, :], ignore_index=True)
        df_virginia.iloc[-1, 0] = m[1]
    elif len(m) == 3:
        df_virginia = df_virginia.append(df_virginia.iloc[i, :], ignore_index=True)
        df_virginia = df_virginia.append(df_virginia.iloc[i, :], ignore_index=True)
        df_virginia.iloc[-2, 0] = m[1] + '_virginia'
        df_virginia.iloc[-1, 0] = m[2]
        df_virginia.iloc[i, 0] = m[0] + '_virginia'
    i += 1

df_virginia['county_state'] = df_virginia['county_state'].str.strip()
df_virginia['county_state'] = df_virginia['county_state'].str.replace(' _', '_')
df_virginia = df_virginia.sort_values(by = ['county_state'], axis=0)
df_virginia[['STATEFP', 'COUNTYFP']] = [np.nan, np.nan]
df_copy = df_virginia.copy()
df_virginia.iloc[64,:],df_virginia.iloc[65,:], df_virginia.iloc[66,:]=df_copy.iloc[65,:],df_copy.iloc[66,:],df_copy.iloc[64,:]
#df_virginia = pd.concat([df_virginia[0:69], pd.DataFrame([], index=[69]), df_virginia[69:]])
i = 0
while i < ref_virginia.shape[0] - 1:
    if ref_virginia.iat[i, 2] != (df_virginia.iat[i, 0]):
        print(i)
        print(ref_virginia.iat[i, 2])
        print(df_virginia.iat[i, 0])
    i = i + 1

i = 0
for i in range(df_virginia.shape[0]):
    df_virginia.iloc[i, 34] = ref_virginia.iloc[i, 0]
    df_virginia.iloc[i, 35] = ref_virginia.iloc[i, 1]
df_virginia = df_virginia.drop(['STATEFP', 'COUNTYFP'], axis=1)
df = pd.concat([df.iloc[0:2820, :], df_virginia, df.iloc[2925:,:]], axis=0, ignore_index=True)

df1=df.copy()
df1.iloc[3069,:],df1.iloc[3070,:]=df.iloc[3070,:],df.iloc[3069,:]
df = df1
del(df1)

df = diff.fix(df, 0, 2, 2)

df = df.reset_index()
ref= ref.reset_index()
df = pd.concat([ref.iloc[:, 1:3], df.iloc[:, 1:]], axis=1)
df = df.sort_values(['STATEFP', 'COUNTYFP'])

df = diff.fix(df, 1, 1, 1)

df.to_csv(r'Parsed data/Employment by Industry.csv', index = False)