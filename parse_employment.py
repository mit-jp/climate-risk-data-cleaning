import pandas as pd
import fix_differences as diff
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/Employment.csv', nrows=3142, low_memory=False)
df.columns = ['county_state' if x=='County Name/State Abbreviation' else x for x in df.columns]
df['county_state'] = df['county_state'].str.lower()
df = diff.fix(df, 0, 2)
df.to_csv(r'/Users/ShelliOrzach/ShelliOrzach1/Documents/DOE MATLAB Updated/Cypress Output Python/Employment.csv', index = False)