import pandas as pd
import numpy as np
import fix_differences as diff
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/Water Usage2.csv')
df = df.replace(-66666, np.nan)
df = diff.fix(df, 1, 1, 1)
df.to_csv(r'Parsed data/Water use.csv', index=False)