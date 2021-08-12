import pandas as pd
import fix_differences as diff
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/Copy of NASS_Census_Pastureland_2017.csv')
df = df.sort_values(by=['State ANSI', 'County ANSI']) # sort by ANSI codes
df = diff.fix(df, 1, 1, 1)
df.to_csv(r'/Parsed data/Pastureland.csv', index=False)