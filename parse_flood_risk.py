import pandas as pd
import numpy as np
import math
import fix_differences as diff
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'Project data/County_level_risk_FEMA_FSF_v1.1.csv', low_memory=False)
df['State ANSI'] = (df['countyfp']/1000).apply(np.floor)
df['County ANSI'] = df['countyfp']-(df['countyfp']/1000).apply(np.floor)*1000
df = df.sort_values(by=['State ANSI', 'County ANSI'])
df = pd.concat([df.iloc[:, 34:36], df.iloc[:, 1:34]], axis=1)
df = diff.fix(df, 1, 1, 1)
df.to_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/Cypress Output Python/Flood Risk.csv', index=False)