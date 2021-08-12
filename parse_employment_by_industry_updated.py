import pandas as pd
import numpy as np
from us import states
import fix_differences as diff
#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/CAEMP25N__ALL_AREAS_2001_2019.csv', nrows=104478, low_memory=False)
df = pd.pivot(df, index='GeoName', columns='Description', values=['2019']).reset_index()
df['County'] = np.nan
df['State'] = np.nan
df[['County', 'State']] = df['GeoName'].str.rsplit(', ', n=1, expand=True)
df = pd.concat([df.iloc[:, 34:37], df.iloc[:, 33], df.iloc[:, 1:33]], axis=1)
df['State'] = df['State'].str.replace('*', '')
df = df.sort_values(by=['State', 'County'])
df = df.iloc[0:3114, :]
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
df.columns = [x[1] for x in df.columns]
df.columns.values[0] = "county_state"
df = df.replace('(D)', np.nan)
df = df.replace('(NA)', np.nan)
for i in range(2, df.shape[1]):
    for j in range(df.shape[0]):
        if pd.notnull(df.iloc[j, i]):
            df.iloc[j, i] = (int(df.iloc[j, i]) / int(df.iloc[j, 1]))*100
df.iloc[:, 1:] = df.iloc[:, 1:].astype(float).round(2)
df = pd.concat([df[0:548], pd.DataFrame([], index=[548]), df[548:]])
df.iloc[548,:] = df.iloc[550,:]
df1=df.copy()
df1.iloc[429,:],df1.iloc[430,:]=df.iloc[430,:],df.iloc[429,:]
df1.iloc[643,:],df1.iloc[644,:]=df.iloc[644,:],df.iloc[643,:]
df1.iloc[711,:],df1.iloc[712,:], df1.iloc[713,:]=df.iloc[712,:],df1.iloc[713,:],df.iloc[711,:]
df1.iloc[740,:],df1.iloc[741,:], df1.iloc[742,:]=df.iloc[741,:],df1.iloc[742,:],df.iloc[740,:]
df1.iloc[1138,:],df1.iloc[1139,:]=df.iloc[1139,:],df.iloc[1138,:]
df1.iloc[1351,:],df1.iloc[1352,:]=df.iloc[1352,:],df.iloc[1351,:]
df1.iloc[1432,:],df1.iloc[1433,:]=df.iloc[1433,:],df.iloc[1432,:]
df1.iloc[2447,:],df1.iloc[2448,:]=df.iloc[2448,:],df.iloc[2447,:]
df1.iloc[2581,:],df1.iloc[2582,:], df1.iloc[2583,:], df1.iloc[2584,:]=df.iloc[2582,:],df1.iloc[2583,:],df.iloc[2584,:], df1.iloc[2581,:]
df = df1
del(df1)

ref = pd.read_csv(r'Parsed data/ID match resorted.csv')
ref_virginia = ref.loc[ref["county_State"].str.endswith("_virginia")]
df_virginia = df.loc[df["county_State"].str.endswith("_virginia")]
df_virginia = df_virginia.sort_values(by = ['county_State'], axis=0)
df_virginia[['STATEFP', 'COUNTYFP']] = [np.nan, np.nan]
df_copy = df_virginia.copy()
df_virginia.iloc[64,:],df_virginia.iloc[65,:], df_virginia.iloc[66,:]=df_copy.iloc[65,:],df_copy.iloc[66,:],df_copy.iloc[64,:]
df_virginia = pd.concat([df_virginia[0:69], pd.DataFrame([], index=[69]), df_virginia[69:]])
i = 0
while i < ref_virginia.shape[0] - 1:
    if ref_virginia.iat[i, 2] != (df_virginia.iat[i, 0]):
        print(i)
        print(ref_virginia.iat[i, 2])
        print(df_virginia.iat[i, 0])
    i = i + 1
    #print(df_virginia.iloc[i, 6])
i = 0
for i in range(df_virginia.shape[0]):
    df_virginia.iloc[i, 34] = ref_virginia.iloc[i, 0]
    df_virginia.iloc[i, 35] = ref_virginia.iloc[i, 1]
df_virginia = df_virginia.sort_values(by = ['STATEFP', 'COUNTYFP'], axis=0)
df_virginia = df_virginia.drop(['STATEFP', 'COUNTYFP'], axis=1)
df = pd.concat([df.iloc[0:2820], df_virginia, df.iloc[2952:,:]], axis=0, ignore_index=True)
#df = diff.fix(df, 0, 2, 2)
#df.to_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/Cypress Output Python/Employment by industry updated temp.csv', index = False)