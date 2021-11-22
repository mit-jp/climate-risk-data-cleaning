import pandas as pd
import numpy as np
import fix_differences as diff
import useful_analysis_functions as fns

# import
df = pd.read_csv(r'Project data/Population per square mile.csv')
df = df.iloc[1:, :]

# remove state rows
df = fns.remove_state_rows(df, 'Area_name')

# format
df['Area_name'] = df['Area_name'].str.replace('\,[^,]*$', '')
df = df.replace(-66666, np.nan)

df = diff.fix(df, 0, 0, 3)
df.to_csv(r'Parsed data/Population density.csv', index=False)