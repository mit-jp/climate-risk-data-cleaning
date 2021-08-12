import pandas as pd
import numpy as np
import fix_differences as diff
# pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/census_data4.csv')
df = df.iloc[:, 1:] # remove first row
df = df.sort_values(by=['state', 'county']) # sort by state then county
df = df.replace(-999999, np.nan) # replace empties with nan
# calculate percent of total
cols = df.columns.tolist()
cols_pct = [i + ' pct' for i in cols]
sum = df.sum(axis=1, min_count=1)
for i in range(3, len(cols)):
    df[str(cols_pct[i])] = df[str(cols[i])]/sum
df = diff.fix(df, 1, 1, 1)
df.to_csv(r'Parsed data/Earnings by Industry.csv', index=False)