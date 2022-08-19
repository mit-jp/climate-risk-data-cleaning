import pandas as pd
import re
import fix_differences as diff
import useful_analysis_functions as fns

# import
df = pd.read_csv(r'Project data/Invasive species trends.csv')

df = df.iloc[:, 0:12]
