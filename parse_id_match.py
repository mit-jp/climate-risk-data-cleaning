import pandas as pd
pd.set_option('display.max_rows', None)
df = pd.read_csv(r'Project data/Copy of name_ID_match.csv')
df = df.sort_values(by=['STATEFP', 'COUNTYFP'])
df = df[:3142]
df['county_State'] = df['county_State'].str.lower()
df['county_State'] = df['county_State'].str.replace(' county', '')
df['county_State'] = df['county_State'].str.replace(' city', '')
df.to_csv(r'Parsed data/ID match.csv', index = False)