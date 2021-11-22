import pandas as pd
import fix_differences as diff
import useful_analysis_functions as fns

df = pd.read_csv(r'Project data/population demographics.csv', nrows=3142, low_memory=False)
df['county_state'] = df[['county', 'state']].agg('_'.join, axis=1).str.lower() # rename to county_state
df = df.drop(['county', 'state'], axis=1)

# reformat county names
df = fns.remove_confusing_words(df, 'county_state')

df = diff.fix(df, 5, 2, 1)
df.to_csv(r'Parsed data/Population demographics.csv', index = False)