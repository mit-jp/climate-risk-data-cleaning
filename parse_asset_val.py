import pandas as pd
import fix_differences as diff
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/Copy of NASS_Census_Asset Value incl bldg_2017.csv')
df = df.sort_values(by=['State ANSI', 'County ANSI'])
df = diff.fix(df, 1, 1, 1)
df.to_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/Cypress Output Python/NASS Asset Val.csv', index = False)