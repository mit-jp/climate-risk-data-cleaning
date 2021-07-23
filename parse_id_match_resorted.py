import pandas as pd
df = pd.read_csv(r'Project data/Copy of name_ID_match.csv', low_memory=False)
df = df.sort_values(by=['STATEFP', 'county_State'])
pd.set_option('display.max_rows', None)
df = df.iloc[0:3142, :]
df['county_State'] = df['county_State'].str.lower()
df['county_State'] = df['county_State'].str.replace(' county', '')
df['county_State'] = df['county_State'].str.replace(' city', '')
print(df)
df.to_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/Cypress Output Python/Copy of name_ID_match_resorted.csv', index = False)