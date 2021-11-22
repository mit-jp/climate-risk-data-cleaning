import pandas as pd
import numpy as np
import fix_differences as diff
import useful_analysis_functions as fns
# pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/census_data4.csv')
df = df.iloc[:, 1:] # remove first row
df = df.sort_values(by=['state', 'county']) # sort by state then county
df = df.replace(-999999, np.nan) # replace empties with nan
# calculate percent of total
df = fns.percent_of_total(df, 3)
df = diff.fix(df, 1, 1, 1)
df.to_csv(r'Parsed data/Earnings by Industry.csv', index=False)