import pandas as pd
import numpy as np
import fix_differences as diff
import useful_analysis_functions as fns

df = pd.read_csv(r'Project data/County_level_risk_FEMA_FSF_v1.1.csv', low_memory=False)

# split to state and county codes
df = fns.split_state_and_county_codes(df, 'countyfp')

#format
df = pd.concat([df.iloc[:, 34:36], df.iloc[:, 1:34]], axis=1) # reorder columns


df = diff.fix(df, 1, 1, 1)
df.to_csv(r'Parsed data/Flood Risk.csv', index=False)