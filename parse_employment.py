import pandas as pd
import fix_differences as diff

# import
df = pd.read_csv(r'Project data/Employment.csv', nrows=3142, low_memory=False)

# format
df.columns = ['county_state' if x=='County Name/State Abbreviation' else x for x in df.columns] # rename column
df['county_state'] = df['county_state'].str.lower() # lower string names

df = diff.fix(df, 0, 2, 1)
df.to_csv(r'Parsed data/3Employment.csv', index = False)