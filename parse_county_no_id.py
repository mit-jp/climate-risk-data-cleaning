import pandas as pd
pd.set_option('display.max_rows', None)
df = pd.read_csv(r'Project data/esri counties for comparison.csv')
df['County'] = df['County'].str.lower() # convert to lowercase
df['County'] = df['County'].str.replace(' county', '')
df['County'] = df['County'].str.replace(' city', '')
df.to_csv(r'Parsed data/County no id.csv', index = False)