import pandas as pd
import fix_differences as diff
df = pd.read_csv(r'Project data/2017 employment.csv')
df = df[:3141] # remove excess
df = diff.fix(df, 1, 1, 1)
df.to_csv(r'Parsed data/2017 employment.csv', index = False)
