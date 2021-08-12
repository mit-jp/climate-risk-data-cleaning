import pandas as pd
import fix_differences as diff
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/population demographics.csv', nrows=3142, low_memory=False)
df['county_state'] = df[['county', 'state']].agg('_'.join, axis=1).str.lower() # rename to county_state
df = df.drop(['county', 'state'], axis=1)
#reformat county names
df['county_state'] = df['county_state'].str.replace(' county', '')
df['county_state'] = df['county_state'].str.replace(' city and', '')
df['county_state'] = df['county_state'].str.replace(' borough', '')
df['county_state'] = df['county_state'].str.replace(' municipality', '')
df['county_state'] = df['county_state'].str.replace(' census area', '')
df['county_state'] = df['county_state'].str.replace(' parish', '')
df['county_state'] = df['county_state'].str.replace(' city', '')
df = diff.fix(df, 5, 2, 1)
df.to_csv(r'Parsed data/Population demographics.csv', index = False)