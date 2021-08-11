import pandas as pd
import numpy as np
import fix_differences as diff

pd.set_option('display.max_rows', None)
df = pd.read_csv(r'Project data/Per Capita Income.csv', low_memory=False, dtype={'GeoType': str})
df = df.iloc[1:3244, :]
df = df.replace(np.nan, '')
i = 1
start = 0
end = 0
while i < df.shape[0]:
    if df.iloc[i, 0] == '':
        end = i
        #print(df.iloc[start+1, 0])
        df.iloc[start+2:end, 0] = [x + '_' + df.iloc[start+1, 0] for x in df.iloc[start+2:end, 0]]
        #print(df.iloc[start:end, 0])
        start = i
        #df = df.drop(df.iloc[i:i+2, :])
    i = i + 1
df.iloc[3221:3244, 0] = [x + '_' + df.iloc[start+1, 0] for x in df.iloc[3221:3244, 0]]
df = df[df['GeoType '].str.contains(r'[_]')]
df['GeoType '] = df['GeoType '].str.lower()
df['GeoType '] = df['GeoType '].str.replace(' county', '')
df['GeoType '] = df['GeoType '].str.replace(' city and', '')
df['GeoType '] = df['GeoType '].str.replace(' borough', '')
df['GeoType '] = df['GeoType '].str.replace(' municipality', '')
df['GeoType '] = df['GeoType '].str.replace(' census area', '')
df['GeoType '] = df['GeoType '].str.replace(' parish', '')
df['GeoType '] = df['GeoType '].str.replace(' city', '')

ref = pd.read_csv(r'Parsed data/ID match resorted.csv')
ref_virginia = ref.loc[ref["county_State"].str.endswith("_virginia")]
df_virginia = df.loc[df["GeoType "].str.endswith("_virginia")]
df_virginia = df_virginia.sort_values(by = ['GeoType '], axis=0)
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
    df_virginia.iloc[i, 6] = ref_virginia.iloc[i, 0]
    df_virginia.iloc[i, 7] = ref_virginia.iloc[i, 1]
df_virginia = df_virginia.sort_values(by = ['STATEFP', 'COUNTYFP'], axis=0)
df_virginia = df_virginia.drop(['STATEFP', 'COUNTYFP'], axis=1)
df = pd.concat([df.iloc[0:2820], df_virginia, df.iloc[2952:,:]], axis=0, ignore_index=True)

df = diff.fix(df, 0, 2, 1)
#print(df)
df.to_csv(r'Parsed data/Per Capita Income.csv', index = False)